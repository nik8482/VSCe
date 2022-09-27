import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import calendar
import numpy as np

months = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}

@st.cache
def get_data():
    dat = pd.read_csv("Mock_RBSi.csv")
    return dat

def chunk_df(df, account, transaction_type):
    dt_chunk = df.loc[(df["Account"] == account) & (df["Type"] == transaction_type)]
    dt_chunk=dt_chunk.drop(['Unnamed: 0'], axis=1).sort_values('Date').reset_index(drop=True)
    return dt_chunk

def monthly_overview(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].apply(lambda x: calendar.month_name[x.month])
    monthly_df = df.groupby('Month').sum().reset_index(drop=False)
    monthly_df['Month_number'] = monthly_df['Month'].apply(lambda x: months[x])
    monthly_df.sort_values('Month_number',inplace=True)
    return monthly_df

def month_insights(df,month_selected):
    df['Date'] = pd.to_datetime(df['Date'])
    df_month = df[df['Date'].dt.month==months[month_selected]]
    return df_month


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
    account_name = st.sidebar.selectbox(
        'Account:',
        tuple(df['Account'].unique())
    )
    month = st.sidebar.selectbox('Month Breakdown:', tuple(months.keys()))

    #Filter DataFrame
    dt_chunk = chunk_df(df, account_name, transaction_type)
    monthly_df = monthly_overview(dt_chunk)


    #Raw View and Metrics
    with st.expander("Raw Dataframe"):
        st.write(dt_chunk)

    st.subheader(f"Yearly Overview for {account_name}")
    st.metric(
            f"Total spent for {transaction_type} for {account_name}",
            f"£{sum(dt_chunk.Amount)}"
        )


    #Plot Yearly Graph
    fig = px.line(dt_chunk,
                  x="Date",
                  y="Amount",
                  title=f"Yearly Spending of {transaction_type} for Account {account_name}")

    fig.update_traces(line=dict(width=4))
    st.plotly_chart(fig, use_container_width=True)



    #Header
    st.subheader(f'Monthy Breakdown')

    describe_df = monthly_df.describe()
    avg, maximum, max_month = st.columns(3)
    
    avg.metric(
            f"Average Monthly for {transaction_type}",
            f"£{np.round(describe_df.loc['mean'].Amount,2)}"
        )
    maximum.metric(
            f"Highest Spend Monthly for {transaction_type}",
            f"£{np.round(describe_df.loc['max'].Amount,2)}"
        )
    max_month.metric(
            f"Most Expensive Month for {transaction_type}",
            f"{monthly_df[monthly_df['Amount']==monthly_df.Amount.max()]['Month'].values[0]}"
        )


    #Plot Monthly Spend
    monthly_fig = px.bar(monthly_df, y='Amount', x='Month', text_auto='.2s',
            title=f"Monthly Spend for {transaction_type}", labels={
                     "Amount": "Amount (£)",
                     "Month": "Month"})
    st.plotly_chart(monthly_fig, use_container_width=True)

    st.subheader(f'Deeper look into {month}')
    df_month = month_insights(dt_chunk, month)

    num_transactions, avg_spend, max_spend = st.columns(3)
    num_transactions.metric(
            f"Number of Transactions",
            f"{len(df_month)}"
        )
    avg_spend.metric(
            f"Average spend in {month}",
            f"£{np.round(df_month['Amount'].mean(),2)}")
    max_spend.metric(
            f"Most expensive transaction",
            f"£{np.round(df_month['Amount'].max(),2)}"
        )

        #Raw View and Metrics
    with st.expander(f"{month} Dataframe"):
        st.write(df_month)

    #Plot Month Graph
    fig_month = px.line(df_month,
                  x="Date",
                  y="Amount",
                  title=f"{month} Spending of {transaction_type} for Account {account_name}")

    fig_month.update_traces(line=dict(width=4))
    st.plotly_chart(fig_month, use_container_width=True)

if __name__ == "__main__":
    main()
