import streamlit as st
import pandas as pd
import plotly.express as px
from copy import deepcopy

# Function to display sidebar and handle file upload
def side_bar():
    st.sidebar.title("CSV Data Upload for Organization and Activities")
    st.sidebar.header("Upload your CSV Data File")

    # Using expander for detailed file format information
    with st.sidebar.expander("Click for more info on CSV File Format"):
        st.write("Please upload a CSV file containing the following fields:")
        st.write("1. location (city, country)")
        st.write(
            "2. n_beneficiaries, n_staff, n_volunteers, n_activities, tot_duration, "
            "times_per_week, tot_cost, tot_budget, workhours (as dictionaries for each month)"
        )
        st.write("3. demo_beneficiaries, demo_staff, demo_volunteers (as nested dictionaries for each month)")

    # Example file download
    with open('data/OrganizationTable.csv', "rb") as file:
        st.sidebar.download_button(
            label="Download Example Dataset as CSV",
            data=file,
            file_name='data/OrganizationTable.csv',
            mime='text/csv',
        )

    # File uploader
    uploaded_file = st.sidebar.file_uploader("Choose your data set file")
    if uploaded_file:
        ngo_df_raw = pd.read_csv(uploaded_file)
    else:
        # Load default data if no file is uploaded
        ngo_df_raw = pd.read_csv('data/OrganizationTable.csv')

    return deepcopy(ngo_df_raw)

# Main application
def main():
    st.title("Estimate Impact of your NGO project!")
    NGO_name = st.text_input('NGO name')
    st.text_input('Target area (Food, Education, Poverty)')
    st.text('Provide a CSV data set on the right')

    # Load data from sidebar
    ngo_df = side_bar()

    # Data Exploration Section
    st.header("Data Exploration")
    st.header(f"{NGO_name} Impact Measure")

    # Visualizations
    plot_visualizations(ngo_df, NGO_name)

def plot_visualizations(ngo_df, NGO_name):
    # Line Graph for Staff and Volunteers Over Time
    st.subheader(f'Staff and Volunteers Over Time for {NGO_name}')
    fig1 = px.line(ngo_df, x='Month', y=['N_staff', 'N_volunteers'])
    st.plotly_chart(fig1)

    # Additional charts like bar chart, box plot, stacked bar chart, and scatter plot
    # ...

if __name__ == "__main__":
    main()
