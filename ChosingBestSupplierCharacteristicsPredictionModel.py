import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from numpy import absolute
from numpy import mean
from numpy import std
import math
import pickle

algoMap = {}

def preProcessData(supCharDf):
    allSuppliers = supCharDf['SupplierId'].unique()
    
    supplierSeed = 10001
    supplierMap = { }
    for supplier in allSuppliers:
        supplierMap[supplier] = supplierSeed
        
        chosenSupplierData = supCharDf.query('SupplierId == "' + supplier + '"')
        
        updateSupplierIndices = chosenSupplierData.index
        print(updateSupplierIndices)
        
        for k in range(len(updateSupplierIndices)):
            supCharDf.at[updateSupplierIndices[k],'Mapped_SupplierId'] = supplierSeed

        supplierSeed += 1
        
    print(supplierMap)
    # Required during inference stage
    with open('./output/suppliermap.dict', 'wb') as fileHandle:
        pickle.dump(supplierMap, fileHandle, protocol=pickle.HIGHEST_PROTOCOL)
    
    return supCharDf

def linearRegrression(X, y):
    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2)
    model = LinearRegression()
    model.fit(train_x, train_y)

    # predict the target on the train dataset
    predict_train = model.predict(train_x)
    print('Target on train data', predict_train[:5])
    
    mas = mean_absolute_error(train_y, predict_train)
    mse = math.sqrt(mean_squared_error(train_y, predict_train))
    print('Mean Absolute Error on train dataset : ', mas)
    print('Mean Squared Error on train dataset : ', mse)
    algoMap["LinearRegression"] = (mse, mas, model)
    
    # predict the target on the test dataset
    predict_test = model.predict(test_x)
    print('Target on test data', predict_test[:5])
    
    print('Mean Absolute Error on test dataset : ', mean_absolute_error(test_y, predict_test))
    print('Mean Squared Error on test dataset : ', math.sqrt(mean_squared_error(test_y, predict_test))) 


def KNN(X, y):
    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2)
    model = KNeighborsRegressor()
    model.fit(train_x, train_y)

    # predict the target on the train dataset
    predict_train = model.predict(train_x)
    print('Target on train data', predict_train[:5]) 

    mas = mean_absolute_error(train_y, predict_train)
    mse = math.sqrt(mean_squared_error(train_y, predict_train))
    print('Mean Absolute Error on train dataset : ', mas)
    print('Mean Squared Error on train dataset : ', mse)
    algoMap["KNN"] = (mse, mas, model)
    
    # predict the target on the test dataset
    predict_test = model.predict(test_x)
    print('Target on test data', predict_test[:5]) 

    print('Mean Absolute Error on test dataset : ', mean_absolute_error(test_y, predict_test))
    print('Mean Squared Error on test dataset : ', math.sqrt(mean_squared_error(test_y, predict_test)))


def decisionTree(X, y):
    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2)
    model = DecisionTreeRegressor()
    # define the evaluation procedure
    cv = RepeatedKFold(n_splits=5, n_repeats=4, random_state=1)
    # evaluate the model and collect the scores
    n_scores = cross_val_score(model, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
    # force the scores to be positive
    n_scores = absolute(n_scores)
    # summarize performance
    print('Mean and Std Dev: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))
    
    # predict the target on the train dataset
    model.fit(train_x, train_y)
    predict_train = model.predict(train_x)
    print('Target on train data', predict_train[:5]) 

    mas = mean_absolute_error(train_y, predict_train)
    mse = math.sqrt(mean_squared_error(train_y, predict_train))
    print('Mean Absolute Error on train dataset : ', mas)
    print('Mean Squared Error on train dataset : ', mse)
    algoMap["DecisionTree"] = (mse, mas, model)
    
    # predict the target on the test dataset
    predict_test = model.predict(test_x)
    print('Target on test data', predict_test[:5]) 

    print('Mean Absolute Error on test dataset : ', mean_absolute_error(test_y, predict_test))
    print('Mean Squared Error on test dataset : ', math.sqrt(mean_squared_error(test_y, predict_test)))
    
def printModelMetrics():
    print("---------------------------------------------------------------------------------------")
    print("Model Metrics...")
    for key in algoMap:
        print(key + " = MSE(" + str(algoMap[key][0]) + "), MAS(" + str(algoMap[key][1]) + ")")
    print("---------------------------------------------------------------------------------------")
    
def compareAndStoreModel():
    minMSE = 9999
    selectedAlgo = ""
    selectedModel = None
    for key in algoMap:
        algoTripple = algoMap[key]
        algoMSE = algoTripple[0]
        if(algoMSE < minMSE):
            minMSE = algoMSE
            selectedAlgo = key
            selectedModel = algoTripple[2]
    
     # Required for inference
    with open('./output/selected_ai_ml_model.mdl', 'wb') as fileHandle:
        pickle.dump(selectedModel, fileHandle, protocol=pickle.HIGHEST_PROTOCOL)
        
    print("Best algorithm selected = " +selectedAlgo) 

def persistModelPerformanceMetrics():
    # Persist model metrics and selection for UI
    row = 0
    modelP4Metrics = pd.DataFrame(columns=['Algorithm', 'MSE', 'MAS'])
    for key in algoMap:
        algoTripple = algoMap[key]
        algoMSE = round(algoTripple[0], 2)
        algoMAS = round(algoTripple[1], 2)
        modelP4Metrics.loc[row] = [key, algoMSE, algoMAS]
        row = row + 1
    modelP4Metrics.to_csv('./output/modelMetrics.csv', mode='w', header=True, encoding='utf-8', index=False)
    print("Model metrics file saved succesfully...")
        
            
def main():
    supCharDf = pd.read_csv('./output/supplier_characteristics_details.csv')
    supCharDf = preProcessData(supCharDf)

    dataDf = supCharDf[['Mapped_SupplierId', 'CommodityId', 'Price', 'POQuality', 'POTimeliness']]
    X = dataDf.drop(columns=['POQuality', 'POTimeliness'], axis=1)
    y = dataDf[['POQuality', 'POTimeliness']]
    
    linearRegrression(X, y)
    KNN(X, y)
    decisionTree(X, y)
    
    printModelMetrics()
    compareAndStoreModel()
    persistModelPerformanceMetrics()
    
main()
