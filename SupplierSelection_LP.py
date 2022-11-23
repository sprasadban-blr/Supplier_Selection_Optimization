import pandas as pd
import pulp as p
import pickle
import numpy as np

def loadData(): 
    bids = pd.read_csv('./output/bidding_supplier_characteristics_prediction.csv')
    return bids

def evaluateLpExpression(bids, weightage_price, weightage_quality, weightage_timeliness, expected_qty):
    problem = p.LpProblem(name='Supplier_Optimization', sense=p.LpMaximize)
    suppliers = p.LpVariable.dicts("", bids['SupplierId'], cat='Integer', lowBound=0, upBound=100)
    priceProblem = p.lpSum(suppliers[bids['SupplierId'][i]] * bids['ScaledQuotedPrice'][i] for i in range(bids['SupplierId'].count()))
    qualityProblem = p.lpSum(suppliers[bids['SupplierId'][i]] * bids['Quality'][i] for i in range(bids['SupplierId'].count()))
    timelinessProblem =  p.lpSum(suppliers[bids['SupplierId'][i]] * bids['Timeliness'][i] for i in range(bids['SupplierId'].count()))

    problem += (weightage_price * priceProblem) + (weightage_quality * qualityProblem) + (weightage_timeliness * timelinessProblem)
    problem += p.lpSum(suppliers[bids['SupplierId'][i]] for i in range(bids['SupplierId'].count())) == expected_qty

    # Solve problem
    problem.solve()

    # Print status
    status = p.LpStatus[problem.status]
    print("Status:", status)
    
    return problem

def getSelectedSupplier(bids, problem):
    # Print optimal values of decision variables

    row = 0
    allottedSuppliers = pd.DataFrame(columns=['Supplier', 'Alloted Quantity', 'Quoted Price', 'Extended Price'])
    supplier = {}
    selectedSupplier = ""
    for v in problem.variables():
        print(v.name, "=", v.varValue)
        supplier[v.name.replace("_", "")] = v.varValue
        if v.varValue is not None and v.varValue > 0:
            selectedSupplier = v.name
    optimizedValue = p.value(problem.objective)
    print("Optimal value for supplier's " + "'" + str(supplier) + "' and the optimized objective function value is " + str(optimizedValue))

    totalAmount = 0.0
    totalAllotedQty = 0.0
    for key in supplier:
        supplierKey = key
        alloted_qty = supplier[key]
        if(alloted_qty > 0):
            supplierBidsData = bids.query('SupplierId == "'+key+'"')
            quoted_price = supplierBidsData['Quoted_Price'].unique()[0]
            extendedPrice = alloted_qty * quoted_price
            totalAmount = totalAmount + extendedPrice
            totalAllotedQty = totalAllotedQty + alloted_qty
            print(supplierKey + ", " + str(alloted_qty) + ", " + str(quoted_price) + ", " + str(totalAmount))
            allottedSuppliers.loc[row] = [supplierKey, round(alloted_qty, 2), round(quoted_price, 2), round(extendedPrice, 2)]
            row = row + 1
    
    allottedSuppliers.loc[row] = ['Total', totalAllotedQty, np.nan, round(totalAmount,2)]
    print("Total Amount = "+ str(totalAmount))
    return allottedSuppliers

def main():
    weightage_price = 0.34
    weightage_quality = 0.33
    weightage_timeliness = 0.33
    expected_qty = 150
    
    bids = loadData()
    lpProblem = evaluateLpExpression(bids, weightage_price, weightage_quality, weightage_timeliness, expected_qty)
    allottedSuppliers = getSelectedSupplier(bids, lpProblem)
    print(allottedSuppliers)

main()
    
    