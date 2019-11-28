def prepare_response(rows):
    returnDict = {}

    wsi1980Dict = {}
    wsi1985Dict = {}
    wsi1990Dict = {}
    wsi1995Dict = {}
    wsi2000Dict = {}
    wsi2005Dict = {}
    wsi2010Dict = {}
    wsi2015Dict = {}

    for x in rows:
        wsi1980Dict[x[0]] = x[1]
        wsi1985Dict[x[0]] = x[2]
        wsi1990Dict[x[0]] = x[3]
        wsi1995Dict[x[0]] = x[4]
        wsi2000Dict[x[0]] = x[5]
        wsi2005Dict[x[0]] = x[6]
        wsi2010Dict[x[0]] = x[7]
        wsi2015Dict[x[0]] = x[8]

    returnDict['1980'] = wsi1980Dict
    returnDict['1985'] = wsi1985Dict
    returnDict['1990'] = wsi1990Dict
    returnDict['1995'] = wsi1995Dict
    returnDict['2000'] = wsi2000Dict
    returnDict['2005'] = wsi2005Dict
    returnDict['2010'] = wsi2010Dict
    returnDict['2015'] = wsi2015Dict

    return returnDict
