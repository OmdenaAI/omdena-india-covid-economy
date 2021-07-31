import numpy as np
import xgboost as xgb

def predictCovid(inputArray):
    count0 = 0
    count1 = 0
    for i in range(1, 9):
        model_load = xgb.XGBClassifier()
        model_load.load_model("model" + str(i) + ".json")
        result = model_load.predict(inputArray.reshape((1, 8)))
        if result[0] == 1:
            count1 += 1
        else:
            count0 += 1
    if count1 >= count0:
        return True
    else:
        return False
