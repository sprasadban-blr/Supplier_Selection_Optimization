import json
import pandas as pd

def load():
    with open('./input/EDS_Items.json') as bidsItems:
        bidsItemsJson = json.load(bidsItems)
    return bidsItemsJson

def parseBids(bidsItems):
    bidsItemsDetails = bidsItems['data']['event']['items']
    itemCommodityMap = {}
    for index in range(len(bidsItemsDetails)):
        itemCommodityMap[bidsItemsDetails[index]['id']] = bidsItemsDetails[index]['commodityCodeId']

    with open('./input/EDS_Bids.json') as bidsFile:
        bids = json.load(bidsFile)
        
    bidsRoot = bids['data']['event']['supplierItemValues']
    bidsDf = bidsRoot[0]

    row = 0
    bidDf = pd.DataFrame(columns=['ItemId', 'CommodityId', 'SupplierId', 'Quantity', 'Quoted_Price', 'ExtendedPrice'])

    for i in range(len(bidsRoot)):
        itemId = bidsRoot[i]['itemId']
        supplierId = bidsRoot[i]['submitForId']
        itemTermValues = bidsRoot[i]['itemTermValues']
        commodityId = itemCommodityMap.get(itemId)
        qty = 0
        quoted_Price = 0.0
        extendedPrice = 0.0
        for k in range(len(itemTermValues)):
            itemTermUniqueName = itemTermValues[k]['itemTermUniqueName']
            if(itemTermUniqueName == 'EXTENDEDPRICE'):
                extendedPrice = itemTermValues[k]['value']['moneyValue']
                currency = itemTermValues[k]['value']['attribute']
            elif(itemTermUniqueName == 'PRICE'):
                quoted_Price = itemTermValues[k]['value']['moneyValue']
                currency = itemTermValues[k]['value']['attribute']
            elif(itemTermUniqueName == 'QUANTITY'):
                qty = itemTermValues[k]['value']['quantityValue']
        bidDf.loc[row] = [itemId, commodityId, supplierId, qty, quoted_Price, extendedPrice]
        row = row + 1
    
    return bidDf 

def main():
    bidsItemsJson = load()
    bidDf = parseBids(bidsItemsJson)
    bidDf.to_csv('./output/bids_details.csv', mode='w', header=True, encoding='utf-8', index=False)
    print("Bids sucessfully parsed and persisted in output folder")

main()