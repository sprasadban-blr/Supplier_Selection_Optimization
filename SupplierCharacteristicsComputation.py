import pandas as pd
import math
from datetime import datetime

def computePercentageRejected(totalRejectedQty, totalQuantityRecived, orderedQuantity):
    '''
     rejected% = (1 - received) * 100 
    '''
    percentageRejected = 0
    if (totalQuantityRecived > 0.0):
        percentageRejected = (1 - ((totalQuantityRecived - totalRejectedQty)/totalQuantityRecived)) * 100
        percentageRejected = round(percentageRejected, 2)  
    
    return percentageRejected


def computeReceiptDiffDays(orderedDateTime, receiptDateTime, needByDateTime):
    diffDays = 0
    
    '''
     diffDays 0 = Received same as need by date
     diffDays +ve = Received earlier than need by date
     diffDays -ve = Received later than need by date 
    '''
    if (str(needByDateTime) != "1970-01-01 00:00:00"):
        diffDays = (needByDateTime - receiptDateTime).days
    
    return diffDays


def getQuality(percentageRejected):
    quality = 1.0
    if(percentageRejected >= 0.0 and percentageRejected <= 10.0):
        quality = 10.0
    elif (percentageRejected > 10.0 and percentageRejected <= 20.0):
        quality = 9.0
    elif (percentageRejected > 20.0 and percentageRejected <= 30.0):
        quality = 8.0
    elif (percentageRejected > 30.0 and percentageRejected <= 40.0):
        quality = 7.0
    elif (percentageRejected > 40.0 and percentageRejected <= 50.0):
        quality = 6.0
    elif (percentageRejected > 50.0 and percentageRejected <= 60.0):
        quality = 5.0
    elif (percentageRejected > 60.0 and percentageRejected <= 70.0):
        quality = 4.0
    elif (percentageRejected > 70.0 and percentageRejected <= 80.0):
        quality = 3.0
    elif (percentageRejected > 85.0 and percentageRejected <= 90.0):
        quality = 2.0
    else:
        quality = 1.0
    
    return quality

def getTimeliness(receiptDiffDays):
    timeliness = 1.0
    if(receiptDiffDays <= -28.0):
        timeliness = 1.0
    elif (receiptDiffDays > -28.0 and receiptDiffDays <= -25.0):
        timeliness = 2.0
    elif (receiptDiffDays > -25.0 and receiptDiffDays <= -22.0):
        timeliness = 3.0
    elif (receiptDiffDays > -22.0 and receiptDiffDays <= -19.0):
        timeliness = 4.0
    elif (receiptDiffDays > -19.0 and receiptDiffDays <= -16.0):
        timeliness = 5.0
    elif (receiptDiffDays > -16.0 and receiptDiffDays <= -13.0):
        timeliness = 6.0
    elif (receiptDiffDays > -13.0 and receiptDiffDays <= -10.0):
        timeliness = 7.0
    elif (receiptDiffDays > -10.0 and receiptDiffDays <= -7.0):
        timeliness = 8.0
    elif (receiptDiffDays > -7.0 and receiptDiffDays < -4.0):
        timeliness = 9.0
    else:
        timeliness = 10.0
    return timeliness
    
def computeHistQuality(percentageRejectedMin, percentageRejectedMax, percentageRejectedMean):
    print("Hist PercentageReceived ="+ str(percentageRejectedMin) +":"+str(percentageRejectedMax)+":"+str(percentageRejectedMean))
    histQuality = 1.0
    percentageRejectedScaled = 0.0
    if(percentageRejectedMax > percentageRejectedMin):
        percentageRejectedScaled = ((percentageRejectedMean - percentageRejectedMin)/(percentageRejectedMax - percentageRejectedMin))*100
        print(percentageRejectedScaled)
    
    return getQuality(percentageRejectedScaled)

def computeHistTimeliness(diffDaysMin, diffDaysMax, diffDaysMean):
    print("Hist Timeliness ="+ str(diffDaysMin) +":"+str(diffDaysMax))
    poTimelinesScaled = 0.0
    if(diffDaysMax > diffDaysMin):
        poTimelinesScaled = ((diffDaysMean - diffDaysMin)/(diffDaysMax - diffDaysMin))*100
        print(poTimelinesScaled)
    
    return getTimeliness(poTimelinesScaled)


def computeSupplierCharacteristicsAtPOLevel(orderReceipts):
    '''
    Compute supplier characteristics at PO/Item/Supplier level
    '''
    row = 0
    supplierCharacteristicsDf = pd.DataFrame(
        columns=['POId', 'SupplierId', 'SupplierName', 'CommodityId', 'CommodityName', 'OrderedQuantity', 'TotalQuantityReceived', 
                 'TotalQuantityRejected', 'Price', 'OrderedDate', 'NeedByDate', 'ReceivedDate', 'PercentageRejected', 'DiffDays', 
                 'POQuality', 'POTimeliness', 'HistQuality', 'HistTimeliness'])

    allPOs = orderReceipts['POId'].unique()

    # compute supplier characteristics across all PO/Item level
    for i in range(len(allPOs)):
        poID = allPOs[i]
        print("POID = "+poID)
        poReceipts = orderReceipts.query('POId == "'+ poID + '"')
        supplierId = poReceipts['SupplierId'].unique()[0]
        print("SupplierID = "+str(supplierId))
        supplierName = poReceipts['SupplierName'].unique()[0]
        print("SupplierName = "+ str(supplierName))
        poReceiptsAllCommodity = poReceipts['CommodityId'].unique()
        
        # All items of a PO/Supplier
        for j in range(len(poReceiptsAllCommodity)):
            commodityId = poReceiptsAllCommodity[j]
            print("commodityId = " + str(commodityId))
            
            queryStr = 'POId == "' + poID + '" & SupplierId == "' + str(supplierId) + '" & CommodityId == ' + str(commodityId)
            print(queryStr)
            selectedPOReceipts = poReceipts.query(queryStr)
            selectedPOReceipts_last = selectedPOReceipts.iloc[-1]
            commodityName = selectedPOReceipts_last['CommodityName']
            print("CommodityName = " + str(commodityName))
            
            orderedQuantity =  selectedPOReceipts_last['Orderd_Quantity']
            print("Ordered Quantity = " +str(orderedQuantity))
            amount = float(selectedPOReceipts_last['Amount'].replace(',',''))
            print("Amount = "+str(amount))
            price = 0.0
            if (orderedQuantity > 0):
                price = amount/orderedQuantity
            print("Price = "+str(price))
        
            # Compute item quality at PO/Receipt level
            totalRejectedQty = selectedPOReceipts_last['TotalNumberRejected']
            print("TotalRejectedQty = " +str(totalRejectedQty))
            totalQuantityRecived = selectedPOReceipts_last['TotalQuantityReceived']
            print("TotalQtyReceived = " +str(totalQuantityRecived))
            
            percentageRejected = computePercentageRejected(totalRejectedQty, totalQuantityRecived, orderedQuantity)
            print("PercentageRejected=" + str(percentageRejected))
            poQuality = getQuality(percentageRejected)
            print("POQuality=" + str(poQuality))
            
            
            # Compute item timeliness at PO/Receipts level
            orderedDate = selectedPOReceipts_last['OrderedDate']
            if (isinstance(orderedDate, str)):
                orderedDateTime = datetime.strptime(orderedDate, "%m/%d/%Y %I:%M %p")
            else:
                orderedDateTime = orderedDate
                
            receiptDate = selectedPOReceipts_last['ReceiptDate']
            print(receiptDate)
            if (isinstance(receiptDate, str)):
                receiptDateTime = datetime.strptime(receiptDate, "%m/%d/%Y %I:%M %p")
            else:
                receiptDateTime = receiptDate
            
            needByDate = selectedPOReceipts_last['LineNeedByDate']
            if(isinstance(needByDate, str)):
                needByDateTime = datetime.strptime(needByDate, "%m/%d/%Y %I:%M %p")
            else:
                needByDateTime = needByDate
            print("NeedByDateTime = " + str(needByDateTime))
            
            receiptDiffDays = computeReceiptDiffDays(orderedDateTime, receiptDateTime, needByDateTime)
            print("ReceiptDiffDays = "+ str(receiptDiffDays))
            poTimeliness = getTimeliness(receiptDiffDays)
            print("poTimeliness = "+ str(poTimeliness))
            
            
            supplierCharacteristicsDf.loc[row] = [poID, supplierId, supplierName, commodityId, commodityName, orderedQuantity, 
                                                  totalQuantityRecived, totalRejectedQty, price, orderedDate, needByDate, receiptDate, 
                                                  percentageRejected, receiptDiffDays, poQuality, poTimeliness, 0.0, 0.0]
            row = row + 1 
        print("-------------------------------------------------------------------------------------------------------")
    
    return supplierCharacteristicsDf
        
def computeSupplierCharacteristicsHistory(supplierCharacteristicsDf):
    allSuppliers = supplierCharacteristicsDf['SupplierId'].unique()
    allCommodities = supplierCharacteristicsDf['CommodityId'].unique()

    for i in range(len(allSuppliers)):
        supplierId = allSuppliers[i]
        for j in range(len(allCommodities)):
            commodityId = allCommodities[j]
            
            # Compute average quality and timeliness
            supplier_item = supplierCharacteristicsDf.query('SupplierId == "'+str(supplierId)+ '" & CommodityId == '+str(commodityId))
            print(supplier_item.index)
            quality = 0.0
            timeliness = 0.0
            
            # PercentageReceived	DiffDays
            if (supplier_item.size > 0):
                poID = supplier_item['POId'].unique()
                #Compute Quality
                percentageRejectedMin  = supplier_item['PercentageRejected'].min()
                percentageRejectedMax = supplier_item['PercentageRejected'].max()
                percentageRejectedMean = supplier_item['PercentageRejected'].mean()
                histQuality = computeHistQuality(percentageRejectedMin, percentageRejectedMax, percentageRejectedMean)
                
                #Compute Timeliness
                diffDaysMin = supplier_item['DiffDays'].min()
                diffDaysMax = supplier_item['DiffDays'].max()
                diffDaysMean = supplier_item['DiffDays'].mean()
                histTimeliness = computeHistTimeliness(diffDaysMin, diffDaysMax, diffDaysMean)
                
                print("Quality=" +str(quality))
                print("Timeliness=" +str(timeliness))
                updateIndices = supplier_item.index
                for k in range(len(updateIndices)):
                    supplierCharacteristicsDf.at[updateIndices[k],'HistQuality'] = histQuality
                    supplierCharacteristicsDf.at[updateIndices[k],'HistTimeliness'] = histTimeliness
    return supplierCharacteristicsDf
    
    
def main():
    orderReceipts = pd.read_csv('./output/order_receipts.csv')
    # Compute supplier characteristics at PO level
    supplierCharacteristicsAtPODf = computeSupplierCharacteristicsAtPOLevel(orderReceipts)
    print("At PO Level")
    print(supplierCharacteristicsAtPODf)
    # Compute supplier characteristics across PO's --> History
    supplierCharacteristicsDf = computeSupplierCharacteristicsHistory(supplierCharacteristicsAtPODf)
    print("At history")
    print(supplierCharacteristicsDf)
    supplierCharacteristicsDf.to_csv('./output/supplier_characteristics_details.csv', mode='w', header=True, encoding='utf-8', index=False)
    print("Supplier characteristics file saved succesfully...")
    
main()
        