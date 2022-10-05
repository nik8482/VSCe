import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import calendar
import numpy as np
import plotly.figure_factory as ff

months = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}

@st.cache
def get_data():
    dat = pd.read_csv("Mock_RBSi.csv")
    return dat

def chunk_df(df, transaction_type):
    dt_chunk = df.loc[df["Type"] == transaction_type]
    dt_chunk=dt_chunk.drop(['Unnamed: 0'], axis=1).sort_values('Date').reset_index(drop=True)
    return dt_chunk

df = get_data()
def main() -> None:
	#Header
	st.header('RBSi Spending Dashboard:')
	# Sidebar:
	st.sidebar.image("RBS_International.png", use_column_width=True)
	transaction_type = st.sidebar.selectbox(
		'Transaction Type:',
		tuple(df['Type'].unique())
	)
	month = st.sidebar.selectbox('Month Breakdown:', tuple(months.keys()))
	#Filter DataFrame
	dt_chunk = chunk_df(df, transaction_type)

	tab1, tab2, tab3 = st.tabs(["Yearly", "Monthly", "Quarterly"])
	#Plot Yearly Graph
	fig = px.line(dt_chunk,x="Date",y="Amount",title=f"Yearly Spending of {transaction_type}")
	with tab1:
	   st.plotly_chart(fig, use_container_width=True)

	with tab2:
	   st.header("A dog")
	   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

	with tab3:
	   st.header("An owl")
	   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


if __name__ == "__main__":
    main()