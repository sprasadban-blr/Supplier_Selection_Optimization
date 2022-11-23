import streamlit as st
import altair as alt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import math
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import cross_val_score
from numpy import absolute
from numpy import mean
from numpy import std
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import json
import pickle
import SupplierSelection_LP as lp

# https://discuss.streamlit.io/t/streamlit-restful-app/409/2
# https://stackoverflow.com/questions/68273958/how-would-i-get-my-streamlit-application-to-use-a-flask-api-in-order-to-retrieve
# https://docs.streamlit.io/

@st.cache
def load_data():
    # Load data
    biddingData = pd.read_csv('./output/bids_details.csv')
    orderReceipts = pd.read_csv('./output/order_receipts.csv')
    supplierCharacteristics = pd.read_csv('./output/supplier_characteristics_details.csv')
    modelMetrics =  pd.read_csv('./output/modelMetrics.csv')
    biddingSuppCharPrediction =  pd.read_csv('./output/bidding_supplier_characteristics_prediction.csv')
    return (biddingData, orderReceipts, supplierCharacteristics, modelMetrics, biddingSuppCharPrediction)

def visualize_data(df, x_axis, y_axis):
    graph = alt.Chart(df).mark_circle(size=60).encode(
        x=x_axis,
        y=y_axis,
        color='SupplierName',
        tooltip=['CommodityName', 'Price', 'POQuality', 'POTimeliness']
    ).interactive()
    st.write(graph)

def getOptimalValues(bids, weightage_price, weightage_quality, weightage_timeliness, expected_qty):
    lpProblem = lp.evaluateLpExpression(bids, weightage_price, weightage_quality, weightage_timeliness, expected_qty)
    allottedSuppliers = lp.getSelectedSupplier(bids, lpProblem)
    return allottedSuppliers

    
def main(biddingData, orderReceipts, supplierCharacteristics, modelMetrics, biddingSuppCharPrediction):
    
    supplierCharExploration = supplierCharacteristics[['SupplierName', 'CommodityName', 'Price', 'POQuality', 'POTimeliness']]
    page = st.sidebar.selectbox("Choose a page", ["Bidding Details", "PO Receipt Details", "Item Supplier Characteristics", "Data Exploration", 
                                                  "Model Metrics", "Bidding Supplier Characteristics Prediction", "Supplier Recommendation"])
    if page == "Bidding Details":
        st.header("About Supplier Item Bidding Details.")
        st.write("Please select a page on the left.")
        st.write(biddingData) 
    if page == "PO Receipt Details":
        st.header("About PO Item Reciept Details.")
        st.write(orderReceipts)
    if page == "Item Supplier Characteristics":
        st.header("Supplier Characteristics From Historical Data.")
        st.write(supplierCharacteristics)
    elif page == "Data Exploration":
        st.title("Data Exploration On Supplier Characteristics.")
        y_axis = st.selectbox("Choose a variable for the y-axis", supplierCharExploration.columns, index=0)        
        x_axis = st.selectbox("Choose a variable for the x-axis", supplierCharExploration.columns, index=1)         
        visualize_data(supplierCharExploration, x_axis, y_axis)
    elif page == "Model Metrics":
        st.title("Prediction Model Metrics")
        st.write(modelMetrics)
    elif page == "Bidding Supplier Characteristics Prediction":
        st.title("Supplier Characteristics Prediction Of Bidding Suppliers")
        st.write(biddingSuppCharPrediction)     
    elif page == "Supplier Recommendation":
        st.title("Supplier Recommendation By Optimization And Selection Process.")
        st.write("Bidding and supplier characteristics details ")
        st.write(biddingSuppCharPrediction)
        option = st.selectbox('Select Commodity', ('', 'Computer Accessories'))
        weightage_price = st.number_input('Price Weightage', value=34.00, max_value=100.00)
        weightage_quality = st.number_input('Quality Weightage', value=33.00, max_value=100.00)
        weightage_timeliness = st.number_input('Timeliness Weightage', value=33.00, max_value=100.00)
        expected_qty = st.number_input('Expected Quantity', value=100, max_value=None)
        
        if st.button('Go'):
            weightageSum = weightage_price + weightage_quality + weightage_timeliness
            if(weightageSum != 100):
                st.write('Weightage sum must be equal to 100..')
            else:
                allottedSuppliers = getOptimalValues(biddingSuppCharPrediction, weightage_price, weightage_quality, weightage_timeliness, expected_qty)
                st.write("Quantity distributions among allotted supplier's..")
                st.write(allottedSuppliers)
            
#Load data and create ML model
data = load_data()
#Render Data and Predict model
main(data[0], data[1], data[2], data[3], data[4])