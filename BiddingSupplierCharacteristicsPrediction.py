import pandas as pd
import pulp as p
import pickle

def load():
    bidDetails = pd.read_csv('./output/bids_details.csv')
    return bidDetails

def normalizePrice(bidDetails):
    minBidPrice = bidDetails['Quoted_Price'].min()
    print(minBidPrice)
    maxBidPrice = bidDetails['Quoted_Price'].max()
    print(maxBidPrice)

    minRange = 1.0
    maxRange = 10.0
    bidDetails['ScaledQuotedPrice'] = round((bidDetails['Quoted_Price'] - minBidPrice)/(maxBidPrice - minBidPrice) * (maxRange - minRange) + minRange, 2)
    # Lower the bidding price higher the ranking
    bidDetails['ScaledQuotedPrice'] = (10 - bidDetails['ScaledQuotedPrice']) + 1
    
    return bidDetails

def predictSupplierCharacteristics(bidDetails):
    modelFile = open('./output/selected_ai_ml_model.mdl', 'rb')
    model = pickle.load(modelFile)
    modelFile.close()

    supplierMapFile = open('./output/suppliermap.dict', 'rb')
    supplierMap = pickle.load(supplierMapFile)
    supplierMapFile.close()

    for index, row in bidDetails.iterrows():
        commodityId = row['CommodityId']
        supplierId = supplierMap[row['SupplierId']]
        price = row['Quoted_Price']
        print("(" + str(row['SupplierId']) + ", " + str(commodityId) + ", " + str(price) + ")")
        
        bidData = pd.DataFrame([[supplierId, commodityId, price]])
        predict_bid = model.predict(bidData)
        
        quality = predict_bid[0][0]
        timeliness = predict_bid[0][1]
        
        print("Quality = " + str(quality) + ", Timeliness = " + str(timeliness))
        print("------------------------------------------------------------------")

        bidDetails.at[index,'Quality'] = quality
        bidDetails.at[index, 'Timeliness'] = timeliness

    return bidDetails
    

def main():
    bidDetails = load()
    bidDetails = normalizePrice(bidDetails)
    bidDetails = predictSupplierCharacteristics(bidDetails)
    bidDetails.to_csv('./output/bidding_supplier_characteristics_prediction.csv')
    print("Bidding supplier characteristics details saved succesfully... ")

main()