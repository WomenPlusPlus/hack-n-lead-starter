import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
ngo_df = pd.DataFrame()
def side_bar():

    st.sidebar.title("CSV Data Upload for Organization and Activities")

    st.sidebar.header("Upload your CSV Data File")
    st.sidebar.write("Please upload a CSV file containing the following fields:")
    st.sidebar.write("1. location (city, country)")
    st.sidebar.write(
        "2. n_beneficiaries, n_staff, n_volunteers, n_activities, tot_duration, times_per_week, tot_cost, tot_budget, workhours (as dictionaries for each month)")
    st.sidebar.write("3. demo_beneficiaries, demo_staff, demo_volunteers (as nested dictionaries for each month)")

    with open('data/OrganizationTable.csv', "rb") as file:
        st.sidebar.download_button(
        label="Download Example Dataset as CSV",
        data=file,
        file_name='data/OrganizationTable.csv',
        mime='text/csv',
    )
    # Add other required fields descriptions
    # Add title and header

    # request_data()

    # path = st.sidebartext_input('CSV file path')
    uploaded_file = st.sidebar.file_uploader("Choose your data set file")

    if uploaded_file:
        ngo_df_raw = pd.read_csv(uploaded_file)
        ngo_df = deepcopy(ngo_df_raw)
        # ngo_df
    else:
        # this is not relevant, but i added otherwise, the app shows an error until the data file is uplaoded
        ngo_df_raw = pd.read_csv('data/OrganizationTable.csv')
        ngo_df = deepcopy(ngo_df_raw)
        ngo_df
    return ngo_df
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df


st.title("Estimate Impact of your NGO project!")
NGO_name = path = st.text_input('NGO name')
path = st.text_input('Target area (Food, Education, Poverty)')
st.text('Provide a CSV data set on the right')


# Open Credentials
ngo_df = side_bar()

st.header("Data Exploration")
st.header(f"{NGO_name} impact measure")
st.text('Charts and fun dashboards')



# 1. Line Graph for Staff and Volunteers Over Time
st.subheader(f'Staff and Volunteers Over Time {NGO_name}')
fig1 = px.line(ngo_df, x='Month', y=['N_staff', 'N_volunteers'])
st.plotly_chart(fig1)

# 2. Bar Chart for Number of Activities Each Month
st.subheader('Number of Activities Each Month')
fig2 = px.bar(ngo_df, x='Month', y='N_activities')
st.plotly_chart(fig2)

# 3. Box Plot for Staff and Volunteer Variability
st.subheader('Staff and Volunteer Variability')
fig3 = px.box(ngo_df, y=['N_staff', 'N_volunteers'])
st.plotly_chart(fig3)

# 4. Stacked Bar Chart for Staff and Volunteers
st.subheader('Staff and Volunteers Each Month')
fig4 = px.bar(ngo_df, x='Month', y=['N_staff', 'N_volunteers'], barmode='stack')
st.plotly_chart(fig4)

# 5. Scatter Plot for Staff vs. Volunteers
st.subheader('Staff vs. Volunteers')
fig5 = px.scatter(ngo_df, x='N_staff', y='N_volunteers')
st.plotly_chart(fig5)