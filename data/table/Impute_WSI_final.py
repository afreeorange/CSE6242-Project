import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import Ridge

from sklearn import metrics
from scipy.optimize import curve_fit

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
Ridge_model_dict = {key: None for key in unique_areaId}

## Imputation
for i in unique_areaId:

    if (i == 169):  # Paraguay
        tt = df_TFW.loc[df_TFW['AreaId'] == i]
        tt_x = tt['Year'].values
        tt_y = tt['Value'].values
        b, a = np.polyfit(tt_x, np.log(tt_y), 1)

        year_array = Year.reshape(len(Year),)
        y = 5E-60 * np.exp(b * year_array)
        Ridge_model_dict[i]={'pred': y.tolist()}

    elif (i == 175): # Guinea-Bissau or Somalia
        tt = df_TFW.loc[df_TFW['AreaId'] == i]
        tt_x = tt['Year'].values
        tt_y = tt['Value'].values

        # Define sigmoid function
        def sigmoid(x, a, b):
            y = 0.18 / (1 + np.exp(-a * (x - b))) + 0.01
            return y


        popt, pcov = curve_fit(sigmoid, tt_x, tt_y, p0=[0.001778, 1993.5])
        y = sigmoid(year_array, *popt)
        Ridge_model_dict[i] = {'pred': y.tolist()}

    elif (i == 201):
        tt = df_TFW.loc[df_TFW['AreaId'] == i]
        tt_x = tt['Year'].values
        tt_y = tt['Value'].values


        # Define sigmoid function
        def sigmoid(x, a, b):
            y = 2.7 / (1 + np.exp(-a * (x - b))) + 0.7
            return y


        popt, pcov = curve_fit(sigmoid, tt_x, tt_y, p0=[0.58, 1992])
        y = sigmoid(year_array, *popt)
        Ridge_model_dict[i] = {'pred': y.tolist()}

    else:
        temp_df = df_TFW.loc[df_TFW['AreaId'] == i]
        temp_x = temp_df['Year'].values.reshape(-1, 1)
        temp_y = temp_df['Value'].values.reshape(-1, 1)

        # Detect outliers and remove it
        test_Q1 = np.quantile(temp_y, 0.25)
        test_Q3 = np.quantile(temp_y, 0.75)
        IQR = test_Q3 - test_Q1
        exist_outlier = [str(i[0]) for i in (temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR))]
        if 'True' in exist_outlier:
            temp_x = temp_x[~((temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR)))].reshape(-1, 1)
            temp_y = temp_y[~((temp_y < (test_Q1 - 1.5 * IQR)) | (temp_y > (test_Q3 + 1.5 * IQR)))].reshape(-1, 1)

        elif (i == 48): #Costa Rico
            temp_x = np.insert(temp_x, 0, 2001).reshape(-1,1)
            temp_y = np.insert(temp_y, 0, 2.2).reshape(-1,1)


        # Build a Ridge Regressor
        temp_Ridge = Ridge(alpha=0.9, normalize=True)
        temp_Ridge.fit(temp_x, temp_y)
        temp_y_pred = temp_Ridge.predict(temp_x)
        Ridge_model_dict[i] = {'m': temp_Ridge.coef_[0], 'b': temp_Ridge.intercept_,
                               'r2': metrics.r2_score(temp_y, temp_y_pred)}
        Ridge_model_dict[i].update({'pred': temp_Ridge.predict(Year).reshape(len(Year), ).tolist()})

df_Ridge_model = pd.DataFrame.from_dict(Ridge_model_dict, orient='index')
df_Ridge_model.index.names = ['AreaId']
df_Ridge_predicted = df_Ridge_model[['pred']]
df_Ridge_predicted = df_Ridge_predicted.pred.apply(pd.Series)
df_Ridge_predicted['AreaId'] = df_Ridge_predicted.index
df_Ridge_predicted.rename(columns={key: value[0] for key, value in zip(range(len(Year)), Year)}, inplace=True)

################### Create year bin

df_yr_base = pd.DataFrame(data=np.arange(1978, 2018, 1),
                          index=np.arange(0, 2018 - 1978, 1),
                          columns=['Year'])
df_yr_base['bucket'] = np.nan
count = 0
x = 1
for i in range(df_yr_base.shape[0]):
    df_yr_base['bucket'][i] = 'bucket' + str(x)
    count += 1
    if count == 5:
        x += 1
        count = 0

df_base = pd.merge(left=df_TFW[['Area', 'AreaId']].drop_duplicates().assign(foo=1),
                   right=df_yr_base.assign(foo=1),
                   left_on='foo',
                   right_on='foo')
df_base.drop(columns=['foo'], inplace=True)

df_TFW_merged = pd.merge(left=df_base,
                         right=df_TFW,
                         left_on=['Area', 'AreaId', 'Year'],
                         right_on=['Area', 'AreaId', 'Year'],
                         how='left')

df_TFW_merged_bucket_avg = df_TFW_merged.groupby(['Area', 'bucket'], as_index=False).mean()
df_TFW_merged_bucket_avg.drop(columns='bucket', inplace=True)

df_Ridge_pred_melt = pd.melt(df_Ridge_predicted, id_vars=['AreaId'],
                             value_vars=[1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015])
df_Ridge_pred_melt.columns = ['AreaId', 'Year', 'pred_val']
df_TFW_comb = pd.merge(left=df_TFW_merged_bucket_avg, right=df_Ridge_pred_melt,
                       left_on=['AreaId', 'Year'], right_on=['AreaId', 'Year'], how='left')
df_TFW_comb.loc[pd.isnull(df_TFW_comb['Value']), 'Value'] = df_TFW_comb.loc[pd.isnull(df_TFW_comb['Value']), 'pred_val']

df_TFW_imputed = df_TFW_comb
df_TFW_imputed.drop(columns='pred_val', inplace=True)



## impute WSI
get_WSI = """
SELECT Year, AreaId, Area, Value from parameter
WHERE VariableId = 4550
ORDER BY AreaId ASC
"""

df_WSI = pd.read_sql(sql=get_WSI, con=conn)
df_WSI_merged = pd.merge(left=df_base,
                         right=df_WSI,
                         left_on=['Area', 'AreaId', 'Year'],
                         right_on=['Area', 'AreaId', 'Year'],
                         how='left')
df_WSI_merged_bucket_avg = df_WSI_merged.groupby(['Area', 'bucket'], as_index=False).mean()
df_WSI_merged_bucket_avg.drop(columns='bucket', inplace=True)
df_WSI_merged_bucket_avg.rename(columns={'Value': 'WSI'}, inplace=True)



# Read filled EFW and TRWR
df_TRWR = pd.read_csv('filledTRWR.csv')
df_EFR = pd.read_csv('filledEFR.csv')
df_TRWR_EFR = pd.merge(left=df_TRWR, right=df_EFR,
                       left_on=['AreaId'], right_on=['AreaId'], how='left')
df_TRWR_EFR.drop(columns=['Area_x','latitude', 'longitude'],inplace=True)

df_TRWR_EFR['diff'] = df_TRWR_EFR['TRWR'] - df_TRWR_EFR['EFR']

# Remove a row that (TRWR-EFR) is negative
df_TRWR_EFR.drop(df_TRWR_EFR.loc[df_TRWR_EFR['diff'] <= 0].index, inplace=True)

df_TFW_diff_merge = pd.merge(left=df_TFW_imputed, right=df_TRWR_EFR,
                       left_on=['AreaId'], right_on=['AreaId'], how='left')
df_TFW_diff_merge.drop(columns=['Area_y', 'TRWR','EFR'], inplace=True)
df_TFW_diff_merge.rename(columns={'Area_x': 'Area', 'Value':'TFW'}, inplace=True)
df_TFW_diff_merge['calc_WSI'] = df_TFW_diff_merge['TFW']*100 / df_TFW_diff_merge['diff']


## Fill NA of WSI in raw data
df_calcWSI_comb = pd.merge(left=df_WSI_merged_bucket_avg, right=df_TFW_diff_merge,
                       left_on=['AreaId', 'Year'], right_on=['AreaId', 'Year'], how='left')
df_calcWSI_comb.drop(columns=['Area_y', 'TFW', 'diff'], inplace=True)
df_calcWSI_comb.loc[pd.isnull(df_calcWSI_comb['WSI']), 'WSI'] = df_calcWSI_comb.loc[pd.isnull(df_calcWSI_comb['WSI']), 'calc_WSI']

df_WSI_imputed = df_calcWSI_comb
df_WSI_imputed.rename(columns={'Area_x':'Area'}, inplace=True)
df_WSI_imputed.drop(columns=['calc_WSI'],inplace=True)

df_WSI_imputed_wide = pd.pivot_table(data = df_WSI_imputed, values='WSI',
                                        columns = 'Year', index = 'Area', aggfunc = 'first')
df_WSI_imputed['Year'] = df_WSI_imputed['Year'].apply(str)

export_df_WSI_imputed_wide = df_WSI_imputed_wide.to_csv(r'imputed_WSI.csv', index=True, header=True)


## Combine with interpolated WSI values
df_interp = pd.read_csv('interpolated_WSI_values.csv')
df_interp.drop(columns=['2017'], inplace=True)
df_interp_melt = pd.melt(df_interp, id_vars=['area_id', 'area'],
                             value_vars=['1980', '1985', '1990', '1995', '2000', '2005', '2010', '2015'])
df_interp_melt.rename(columns={'variable': 'Year', 'value': 'interpolated'}, inplace=True)

df_comb = pd.merge(left=df_WSI_imputed, right=df_interp_melt,
                       left_on=['AreaId', 'Area','Year'], right_on=['area_id', 'area' ,'Year'], how='left')
df_comb.loc[pd.isnull(df_comb['area']), 'interpolated'] = df_comb.loc[pd.isnull(df_comb['area']), 'WSI']
df_comb.drop(columns=['WSI', 'area_id', 'area'], inplace=True)

df_comb_wide = pd.pivot_table(data = df_comb, values='interpolated',
                                        columns = 'Year', index = ['AreaId', 'Area'], aggfunc = 'first')
df_comb_wide.reset_index(inplace=True)

df_comb_wide.to_csv(r'imputed_ridge_combined_WSI.csv', index=True, header=True)