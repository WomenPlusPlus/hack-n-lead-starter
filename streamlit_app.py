import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df


# Add title and header
st.title("Estimate Impact of your NGO project!")
path = st.text_input('NGO name')
path = st.text_input('Target area (Food, Education, Poverty)')
st.text('Provide a CSV data set, making sure ')
st.header("Data Exploration")

path = st.text_input('CSV file path')
if path:
    mpg_df_raw = load_data(path=path)
    mpg_df = deepcopy(mpg_df_raw)


