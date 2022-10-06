import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.image("RBS_International.png", width=200)

st.write("# Welcome to the RBSi Spending Dashboard! 👋")

st.sidebar.success("Select a Juristdiction above.")

st.markdown(
    """
    The spending dashboard has been built specifically for visualising spending habits for each of the different jurisdictions across all personal accounts. You can start by selecting a jurisdiction from the side-bar on the left.
    ### Want to learn more?
    - Message the Data Science Team within the Data and Analytics Practice 
    ### Authors
    - Nikhil Modha (nikhil.modha@rbsint.com)
    - Sachin Rawat (sachin.rawat@rbsint.com)
"""
)