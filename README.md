# Supplier characteristics Prediction, Finding Desired Supplier and Supplier Selection

**POC to check concept on Supplier Prediction, LP Optimization on desired supplier selection process**

### Highlights:
  * Analyze on bidding event data
  * Supplier Characteristics computation based on historical reporting (buyer integrated) database (Compute Quality and Timeliness)
  * Performing supplier characteristics (Quality, Timeliness) prediction using multi output regression 
  * Selecting one among the best regression algorithms (Liner Regression, KNN, Decision Tree)
  * Deriving optimization problem with objective function and set of constraints based on bidding events and supplier characteristics data
  * Award desired supplier's by evaluting LP objective function
  * An UI to showcase the above capabilities

### Prerequisite:
  * **Install Python 3.6 *https://www.python.org/downloads/release/python-368/*** 
	* **Install needed python libraries**
		- python -m pip install --upgrade pip
		- pip install sklearn
		- pip install --upgrade streamlit
		- pip install pulp
		- pip install altair
		- pip install matplotlib
		- pip install pandas
		- pip install numpy

  * **Clone github**
    - $SRC_DIR>*git clone https://github.com/sprasadban/Supplier_Selection_Optimization*

  * **Steps to extract bidding event data**
    - Use the Event Data Source/Server (EDS) API to download the required bidding event data (Using Postman/Insomnia tool)
      * Persist the JSON files in *'./input/EDS_BIDS.json'* and *'./input/EDS_Items.json'*
    - Parse the above JSON using *'./BIDSParser.py'* to extract the properties required for the PoC
      * Persist the JSON files in *'./output/bids_details.csv'*
  
  * **Steps to extract PO/Receipts data from reporting system**
    - Download PO and PO receipts data from buyer integrated reporting DB (as CSV files from Inspector tool)
      * Persist the CSV files in *'./input/PO_Details.csv'* and *'./input/Receipt_Details.csv'*
      * Queries used to download the data can be referred from *'queries.sql'* file
    - Parse the above CSV using *'Data_Preparation.py'* to extract the properties required for the PoC
      * Persist the CSV files in *'./output/order_receipts.csv'*
    - **Note:** For now we have downloaded the CSV data from reporting system through ***'Inspector'*** tool.. In reality we need to build ***'knowledgebase'*** for supplier characteristics by extracting data directly from Reporting/Prism database
  
  * **Steps to create supplier characteristics knowledgebase**
    - Run *'SupplierCharacteristicsComputation.py'* to compute *'Quality'* and *'Timeliness'* based on historial orders and receipts
    - Persist the CSV file in *'./output/supplier_characteristics_details.csv'*
  
  * **Steps to create supplier characteristics AI/ML prediction model**
    - Choose by running *'ChosingBestSupplierCharacteristicsPredictionModel.py'* to select the best algorithm for our data using **LinearRegression, KNN and Decision Tree** algorithm
    - Persist the AI/ML model *'selected_ai_ml_model.mdl'* and the dictionary used *'suppliermap.dict'* to map Supplier ID's.. These are required during inference time
    - **Note:** For now we have tried out few prediction algorithms with *MSE (Mean Squared Error) and MAS (Mean Absolute Error)* as our prediction performance metrics.. We need to try other algorithms and performance metrics
  
  * **Steps to create supplier characteristics prediction based on Bidding event data**
    - Run *'BiddingSupplierCharacteristicsPrediction.py'*. This will perform inference against all bidding event data to get predicted supplier characteristics
    - Persist *'bidding_supplier_characteristics_prediction.csv'* used for LP optimization 

### Run supplier recommendation dashboard application 
  ***$SRC_DIR>streamlit run SupplierRecommendationDashboard.py***
  * LP optimization is used to award supplier based on weightage given to *price/quality/timeliness* along with desired *quanity* required

### Run UI application
  * *http://localhost:8501/*
  * Select the commodity from the list (For now one commodity)
  * Provide the weightage % importance for *Price/Quality/Timeliness* (Must match 100%)
  * Feed desired quantity required.. Quantity will be split among supplier's if supplier can't fulfill the request by respecting the weightage given to *Price/Quality/Timeliness*
