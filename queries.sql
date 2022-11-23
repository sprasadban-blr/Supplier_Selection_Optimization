1. Query fully received Orders and Order Items.. Download as CSV file

select 
  po.POId as POId, 
  po.OrderID as OrderID, 
  po.POName as POName, 
  po.Amount as Amount, 
  po.DeliveryTime as DeliveryTime, 
  po.ReceiptTime as ReceiptTime, 
  po.InvoiceTime as InvoiceTime, 
  po.OnTimeOrLate as OnTimeOrLate, 
  po.RejectedItems as RejectedItems, 
  po.SubstitutedItems as SubstitutedItems, 
  po.OrderedDate.Day as OrderedDate, 
  po.NeedByDate.Day as NeedByDate, 
  po.Supplier.SupplierId as SupplierId, 
  po.Supplier.SupplierName as SupplierName, 
  po.Supplier.SupplierPublicName as SupplierPublicName, 
  po.Supplier.City as SupplierCity, 
  po.Supplier.State as SupplierState, 
  po.Supplier.Country as SupplierCountry, 
  po.Supplier.SupplierLocationId as SupplierLocationId, 
  pol.POLineNumber as POLineNumber, 
  pol.Title as Title, 
  pol.Description as Description, 
  pol.Supplier.SupplierId as LineSupplierId, 
  pol.Supplier.SupplierName as LineSupplierName, 
  pol.Supplier.SupplierPublicName as LineSupplierPublicName, 
  pol.Supplier.City as LineSupplierCity, 
  pol.Supplier.State as LineSupplierState, 
  pol.Supplier.Country as LineSupplierCountry, 
  pol.Supplier.SupplierLocationId as LineSupplierLocationId, 
  pol.Quantity as Orderd_Quantity, 
  pol.NeedByDate.Day as LineNeedByDate, 
  pol.Amount as Amount, 
  pol.LineItemCount as LineItemCount, 
  pol.POCount as POCount, 
  pol.OrderedDate.Day as OrderedDate, 
  pol.Commodity.CommodityId as CommodityId,
  pol.Commodity.CommodityName as CommodityName,
  pol.Commodity.UNSPSCCodeId as UNSPSCCodeId, 
  pol.Part.SupplierPartNumber as SupplierPartNumber, 
  pol.Part.PartName as PartName, 
  pol.OrderType as OrderType
from 
  ariba.analytics.fact.PODelivery po 
  inner join ariba.analytics.fact.SSPPOLineItem pol on po.POId = pol.POId
where po.Receipt = 'FullyReceived'
Order by po.POId

2. Query matching Order receipts.. Download to CSV file

select 
  rec.OrderId as OrderId, 
  rec.ReceiptId as ReceiptId, 
  rec.ReceiptDate.Day as ReceiptDate, 
  rec.LineItemNumber as LineItemNumber, 
  rec.Quantity as Receipt_Quantity, 
  rec.LineType as LineType, 
  rec.DateOfDelivery.Day as DateOfDelivery, 
  rec.NumberPreviouslyAccepted as NumberPreviouslyAccepted, 
  rec.NumberAccepted as NumberAccepted, 
  rec.NumberPreviouslyRejected as NumberPreviouslyRejected, 
  rec.NumberRejected as NumberRejected
from 
  ariba.analytics.fact.PODelivery po, 
  ariba.analytics.fact.Receipt rec 
where 
  po.POId = rec.OrderId 
Order by po.POId, rec.ReceiptId

3. Perform Inner Join on the above CSV files in python code to get fully received orders and associated receipts.  