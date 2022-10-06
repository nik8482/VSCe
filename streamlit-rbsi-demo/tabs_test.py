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

def get_metrics(df):
    df['Date'] = pd.to_datetime(df['Date'])
    
    df['Week'] = df['Date'].apply(lambda x: x.week)
    df['Month'] = df['Date'].apply(lambda x: x.month)
    df['Quarter'] = df['Date'].apply(lambda x: x.quarter)

    weekly_df = df[['Week','Amount']].groupby('Week').sum().reset_index()
    monthly_df = df[['Month','Amount']].groupby('Month').sum().reset_index()
    quarter_df = df[['Quarter','Amount']].groupby('Quarter').sum().reset_index()
    
    weekly_mean = df[['Week','Amount']].groupby('Week').sum()['Amount'].mean()
    monthly_mean = df[['Month','Amount']].groupby('Month').sum()['Amount'].mean()
    quarter_mean = df[['Quarter','Amount']].groupby('Quarter').sum()['Amount'].mean()
    
    return np.round(weekly_mean,0),np.round(monthly_mean,0),np.round(quarter_mean,0), weekly_df, monthly_df, quarter_df

df = get_data()
def main() -> None:
	#Header
	st.header('RBSi Spending Dashboard:')
	# Sidebar:
	st.sidebar.image("RBS_International.png", use_column_width=True)
	
	#Filter DataFrames
	df_groceries = chunk_df(df, "Groceries")
	df_bills = chunk_df(df,"Bills")
	df_entertainment = chunk_df(df, "Entertainment")

	Groceries_tab, Bills_tab, Entertainment_tab = st.tabs(["Groceries", "Bills", "Entertainment"])
	
	#Plot Metrics
	with Groceries_tab:
		weekly, monthly, quarterly, weekly_df, monthly_df, quarter_df = get_metrics(df_groceries)
		weekly_col, monthly_col, quarter_col = st.columns(3)
		weekly_col.metric(label='Average Weekly Spend', value=f'£{weekly}0')
		monthly_col.metric(label='Average Monthly Spend', value=f'£{monthly}0')
		quarter_col.metric(label='Average Quarterly Spend', value=f'£{quarterly}0')

		print(weekly_df.columns)
		weekly_tab, monthly_tab, quarter_tab = st.tabs(["Weekly","Monthly","Quarterly"])
		with weekly_tab:
			weekly_fig = px.bar(weekly_df, y='Amount', x='Week', text_auto='.2s',title=f"Weekly Spend for Groceries", labels={"Amount": "Amount (£)","Week": "Week"})
			st.plotly_chart(weekly_fig, use_container_width=True)
		with monthly_tab:
			monthly_fig = px.bar(monthly_df, y='Amount', x='Month', text_auto='.2s',title=f"Monthly Spend for Groceries", labels={"Amount": "Amount (£)","Week": "Week"})
			st.plotly_chart(monthly_fig, use_container_width=True)
		with quarter_tab:
			quarter_fig = px.bar(quarter_df, y='Amount', x='Quarter', text_auto='.2s',title=f"Quarterly Spend for Groceries", labels={"Amount": "Amount (£)","Week": "Week"})
			st.plotly_chart(quarter_fig, use_container_width=True)			

	with Bills_tab:
		weekly, monthly, quarterly, weekly_df, monthly_df, quarter_df = get_metrics(df_bills)
		weekly_col, monthly_col, quarter_col = st.columns(3)
		weekly_col.metric(label='Average Weekly Spend', value=f'£{weekly}0')
		monthly_col.metric(label='Average Monthly Spend', value=f'£{monthly}0')
		quarter_col.metric(label='Average Quarterly Spend', value=f'£{quarterly}0')

		print(weekly_df.columns)
		weekly_tab, monthly_tab, quarter_tab = st.tabs(["Weekly","Monthly","Quarterly"])
		with weekly_tab:
			weekly_fig = px.bar(weekly_df, y='Amount', x='Week', text_auto='.2s',title=f"Weekly Spend for Groceries", labels={"Amount": "Amount (£)","Week": "Week"})
			st.plotly_chart(weekly_fig, use_container_width=True)
		with monthly_tab:
			monthly_fig = px.bar(monthly_df, y='Amount', x='Month', text_auto='.2s',title=f"Monthly Spend for Groceries", labels={"Amount": "Amount (£)","Week": "Week"})
			st.plotly_chart(monthly_fig, use_container_width=True)
		with quarter_tab:
			quarter_fig = px.bar(quarter_df, y='Amount', x='Quarter', text_auto='.2s',title=f"Quarterly Spend for Groceries", labels={"Amount": "Amount (£)","Week": "Week"})
			st.plotly_chart(quarter_fig, use_container_width=True)
	
	with Entertainment_tab:
		weekly, monthly, quarterly, weekly_df, monthly_df, quarter_df = get_metrics(df_entertainment)
		weekly_col, monthly_col, quarter_col = st.columns(3)
		weekly_col.metric(label='Average Weekly Spend', value=f'£{weekly}0')
		monthly_col.metric(label='Average Monthly Spend', value=f'£{monthly}0')
		quarter_col.metric(label='Average Quarterly Spend', value=f'£{quarterly}0')

		print(weekly_df.columns)
		weekly_tab, monthly_tab, quarter_tab = st.tabs(["Weekly","Monthly","Quarterly"])
		with weekly_tab:
			weekly_fig = px.bar(weekly_df, y='Amount', x='Week', text_auto='.2s',title=f"Weekly Spend for Groceries", labels={"Amount": "Amount (£)","Week": "Week"})
			st.plotly_chart(weekly_fig, use_container_width=True)
		with monthly_tab:
			monthly_fig = px.bar(monthly_df, y='Amount', x='Month', text_auto='.2s',title=f"Monthly Spend for Groceries", labels={"Amount": "Amount (£)","Week": "Week"})
			st.plotly_chart(monthly_fig, use_container_width=True)
		with quarter_tab:
			quarter_fig = px.bar(quarter_df, y='Amount', x='Quarter', text_auto='.2s',title=f"Quarterly Spend for Groceries", labels={"Amount": "Amount (£)","Week": "Week"})
			st.plotly_chart(quarter_fig, use_container_width=True)


if __name__ == "__main__":
    main()