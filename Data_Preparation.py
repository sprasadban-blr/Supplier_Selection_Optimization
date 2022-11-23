import pandas as pd
import csv
import numpy as np 

def createPOReciptsFile(order, receipt):
    if (isinstance(receipt['NumberPreviouslyAccepted'], str) == True):
        receipt['NumberPreviouslyAccepted'] = receipt['NumberPreviouslyAccepted'].str.replace(',','').astype(np.float64)

    if (isinstance(receipt['NumberAccepted'], str) == True):
        receipt['NumberAccepted'] = receipt['NumberAccepted'].str.replace(',','').astype(np.float64)

    if (isinstance(receipt['NumberPreviouslyRejected'], object) == True):
        receipt['NumberPreviouslyRejected'] = receipt['NumberPreviouslyRejected'].str.replace(',','').astype(np.float64)

    if (isinstance(receipt['NumberRejected'], object) == True):
        receipt['NumberRejected'] = receipt['NumberRejected'].str.replace(',','').astype(np.float64)
        
    order_details = order[['POId', 'POName', 'SupplierId', 'SupplierName', 'POLineNumber', 'CommodityId', 'CommodityName', 'LineNeedByDate', 'Orderd_Quantity', 
                        'Amount', 'OrderedDate', 'OrderType']]
    order_receipts = pd.merge(order_details, receipt,  how='inner', left_on=['POId','POLineNumber'], right_on = ['OrderId','LineItemNumber'])
    order_receipts_details = order_receipts[['POId', 'POName', 'SupplierId', 'SupplierName', 'POLineNumber','CommodityId', 'CommodityName', 
                                            'LineNeedByDate', 'Orderd_Quantity', 'Amount', 'OrderedDate', 'OrderType', 'ReceiptId','ReceiptDate', 
                                            'DateOfDelivery', 'LineType', 'Receipt_Quantity', 'NumberPreviouslyAccepted', 'NumberAccepted',
                                            'NumberPreviouslyRejected', 'NumberRejected']]
    order_receipts_details['TotalNumberAccepted'] = order_receipts_details['NumberPreviouslyAccepted'] + order_receipts_details['NumberAccepted']
    order_receipts_details['TotalNumberRejected'] = order_receipts_details['NumberPreviouslyRejected'] + order_receipts_details['NumberRejected']
    order_receipts_details['TotalQuantityReceived'] = order_receipts_details['TotalNumberAccepted'] + order_receipts_details['TotalNumberRejected']
    order_receipts_details.to_csv('./output/order_receipts.csv', mode='w', header=True, encoding='utf-8', index=False)
    print("Order Receipts file './output/order_receipts.csv' created")

def main():
    order = pd.read_csv('./input/PO_Details.csv')
    receipt = pd.read_csv('./input/Receipt_Details.csv')
    createPOReciptsFile(order, receipt)

main()