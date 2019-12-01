import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import (
    LinearRegression, TheilSenRegressor, Ridge)

from sklearn import metrics
import matplotlib.pyplot as plt
from collections import defaultdict

conn = sqlite3.connect('project.db')
conn.text_factory = lambda x: str(x, 'iso-8859-1')
cur = conn.cursor()

### Total freshwater Withdrawal
get_TFW = """
SELECT Year, AreaId, Area, Value from parameter
WHERE VariableId = 4263
ORDER BY AreaId ASC
"""

get_area_exclude = """
SELECT AreaId from
	(
		SELECT Year, AreaId, Value, Area, count(Year) as count from parameter
		where VariableId=4263
		GROUP By AreaId
		)
	Where count <= 1
"""
df_TFW = pd.read_sql(sql=get_TFW, con=conn)
df_area_exclude = pd.read_sql(sql=get_area_exclude, con=conn)
list_area_exclude = df_area_exclude['AreaId'].values.tolist()

df_TFW = df_TFW[~df_TFW['AreaId'].isin(list_area_exclude)]

# Year where TFW values are estimated
# from 1980 to 2015 withh 5-year gap
Year = list(range(1980, 2016, 5))
Year = np.asarray(Year).reshape(-1, 1)

# Obtain Unique AreaId
unique_areaId = df_TFW.AreaId.unique().tolist()
linear_model_dict = {key: None for key in unique_areaId}
Theil_model_dict = {key: None for key in unique_areaId}
Ridge_model_dict = {key: None for key in unique_areaId}
a_alpha = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

######################################## Ridge regression
Ridge_vary_alpha = {key: [] for key in a_alpha}
# Tunning alpha value
for k in a_alpha:

    for areaId in unique_areaId:

        temp_df = df_TFW.loc[df_TFW['AreaId'] == areaId]
        temp_x = temp_df['Year'].values.reshape(-1, 1)
        temp_y = temp_df['Value'].values.reshape(-1, 1)

        # Detect outliers and remove it
        test_Q1 = np.quantile(temp_y, 0.25)
        test_Q3 = np.quantile(temp_y, 0.75)
        IQR = test_Q3 - test_Q1
        exist_outlier = [str(x[0]) for x in (temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR))]
        if 'True' in exist_outlier:
            temp_x = temp_x[~((temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR)))].reshape(-1, 1)
            temp_y = temp_y[~((temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR)))].reshape(-1, 1)


         # Build a Ridge Regressor
        temp_Ridge = Ridge(alpha=k, normalize=True)
        temp_Ridge.fit(temp_x, temp_y)
        temp_y_pred = temp_Ridge.predict(temp_x)
        Ridge_predict = temp_Ridge.predict(Year).reshape(len(Year), ).tolist()
        incor_pred = sum(1 for pred in Ridge_predict if pred < 0)
        Ridge_vary_alpha[k].append({'areaId': areaId,
                                'mse': metrics.mean_squared_error(temp_y, temp_y_pred),
                               'r2': metrics.r2_score(temp_y, temp_y_pred),
                                    'num_incor':incor_pred})

num_incor_alpha = defaultdict(int)
alpha_r2 = {key: [] for key in a_alpha}
alpha_mse = {key: [] for key in a_alpha}
for key in Ridge_vary_alpha.keys():
    for i in range(len(Ridge_vary_alpha[key])):
        if Ridge_vary_alpha[key][i]['num_incor'] >= 1:
            num_incor_alpha[key] += 1

        alpha_r2[key].append(Ridge_vary_alpha[key][i]['r2'])
        alpha_mse[key].append(Ridge_vary_alpha[key][i]['mse'])

avg_r2_alpha=[sum(element) / len(element) for element in alpha_r2.values()]
avg_mse_alpha=[sum(element) / len(element) for element in alpha_mse.values()]
num_incorrect_alpha= [v for k,v in zip(num_incor_alpha.keys(), num_incor_alpha.values())]

## Plot
# R-squared vs. alpha
plt.figure()
plt.title("R-squared value vs. alpha")
plt.scatter(a_alpha, avg_r2_alpha)
plt.xlabel("alpha")
plt.ylabel("Averaged R-squared")
plt.xlim(0,1)
plt.ylim(0,1)
plt.show()

# MSE vs. alpha
plt.figure()
plt.title("MSE vs. alpha")
plt.scatter(a_alpha, avg_mse_alpha)
plt.xlabel("alpha")
plt.ylabel("Averaged MSE")
plt.xlim(0,1)
plt.ylim(0,35)
plt.show()

# num_incorrect models vs. alpha
plt.figure()
plt.title("The number of incorrect models vs. alpha")
plt.scatter(a_alpha, num_incorrect_alpha)
plt.xlabel("alpha")
plt.ylabel("The number of incorrect models")
plt.xlim(0,1)
plt.ylim(0,15)
plt.show()


######################################## Linear regerssion vs. Ridge regression
for i in unique_areaId:

    temp_df = df_TFW.loc[df_TFW['AreaId'] == i]
    temp_x = temp_df['Year'].values.reshape(-1, 1)
    temp_y = temp_df['Value'].values.reshape(-1, 1)

    # Detect outliers and remove it
    test_Q1 = np.quantile(temp_y, 0.25)
    test_Q3 = np.quantile(temp_y, 0.75)
    IQR = test_Q3 - test_Q1
    exist_outlier = [str(x[0]) for x in (temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR))]
    if 'True' in exist_outlier:
        temp_x = temp_x[~((temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR)))].reshape(-1, 1)
        temp_y = temp_y[~((temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR)))].reshape(-1, 1)

    # Build a linear regression model
    temp_linear = LinearRegression()
    temp_linear.fit(temp_x, temp_y)
    temp_y_pred = temp_linear.predict(temp_x)
    linear_model_dict[i] = {'m': temp_linear.coef_[0][0], 'b': temp_linear.intercept_[0],
                            'r2': metrics.r2_score(temp_y, temp_y_pred)}
    linear_model_dict[i].update({'pred': temp_linear.predict(Year).reshape(len(Year), ).tolist()})

    # Build a Ridge Regressor
    temp_Ridge = Ridge(alpha=0.98, normalize=True)
    temp_Ridge.fit(temp_x, temp_y)
    temp_y_pred = temp_Ridge.predict(temp_x)
    Ridge_model_dict[i] = {'m': temp_Ridge.coef_[0], 'b': temp_Ridge.intercept_,
                           'r2': metrics.r2_score(temp_y, temp_y_pred)}
    Ridge_model_dict[i].update({'pred': temp_Ridge.predict(Year).reshape(len(Year), ).tolist()})


df_OLS_model = pd.DataFrame.from_dict(linear_model_dict, orient='index')
df_OLS_model.index.names = ['AreaId']
df_OLS_predicted = df_OLS_model[['pred']]
df_OLS_predicted = df_OLS_predicted.pred.apply(pd.Series)
df_OLS_predicted['AreaId'] = df_OLS_predicted.index
df_OLS_predicted.rename(columns={key: value[0] for key, value in zip(range(len(Year)), Year)}, inplace=True)

df_Ridge_model = pd.DataFrame.from_dict(Ridge_model_dict, orient='index')
df_Ridge_model.index.names = ['AreaId']
df_Ridge_predicted = df_Ridge_model[['pred']]
df_Ridge_predicted = df_Ridge_predicted.pred.apply(pd.Series)
df_Ridge_predicted['AreaId'] = df_Ridge_predicted.index
df_Ridge_predicted.rename(columns={key: value[0] for key, value in zip(range(len(Year)), Year)}, inplace=True)

## Only compare countries that fails for linear regression
df_OLS_neg_1980 = df_OLS_predicted.loc[df_OLS_predicted[1980] < 0]
df_Ridge_neg_1980 = df_Ridge_predicted.loc[df_Ridge_predicted[1980] < 0]
df_OLS_neg_areId = df_OLS_neg_1980['AreaId'].tolist()
Ridge_neg_areaId = df_Ridge_neg_1980['AreaId'].tolist()
#
#print(len(Ridge_neg_areaId))

for i in df_OLS_neg_areId:
    temp_df = df_TFW.loc[df_TFW['AreaId'] == i]
    temp_x = temp_df['Year'].values.reshape(-1, 1)
    temp_y = temp_df['Value'].values.reshape(-1, 1)

    # check outliers
    test_Q1 = np.quantile(temp_y, 0.25)
    test_Q3 = np.quantile(temp_y, 0.75)
    IQR = test_Q3 - test_Q1
    exist_outlier = [str(i[0]) for i in (temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR))]
    if 'True' in exist_outlier:
        temp_x = temp_x[~((temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR)))].reshape(-1, 1)
        temp_y = temp_y[~((temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR)))].reshape(-1, 1)

    temp_linear = LinearRegression()
    temp_linear.fit(temp_x, temp_y)
    temp_lienar_y_pred = temp_linear.predict(Year)


    temp_Ridge = Ridge(alpha=0.9, normalize=True)
    temp_Ridge.fit(temp_x, temp_y)
    temp_ridge_y_pred = temp_Ridge.predict(Year)

    temp_area = pd.unique(pd.Series(df_TFW.loc[df_TFW['AreaId'] == i]['Area']))[0]
    temp_title = temp_area + " (AreaId = " + str(i) + ")"
    plt.figure()
    plt.title(temp_title)
    plt.scatter(temp_x, temp_y)
    plt.plot(Year, temp_lienar_y_pred, color='red')
    plt.plot(Year, temp_ridge_y_pred, color='green')
    plt.axhline(y=0.0, color='black', linestyle='--')
    plt.xlabel("Year")
    plt.ylabel("Total Freshwater Withdrawal (TFW)")
    plt.legend(['OLS regression', 'Ridge regression (alpha=0.9)'])
    plt.show()



