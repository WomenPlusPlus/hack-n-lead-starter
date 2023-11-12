import streamlit as st
import pandas as pd
import plotly.express as px
from copy import deepcopy
import matplotlib.pyplot as plt

# Function to display sidebar and handle file upload
def side_bar():
    st.sidebar.title("CSV Data Upload for Organization and Activities")
    st.sidebar.header("Upload your CSV Data File")

    # Using expander for detailed file format information
    with st.sidebar.expander("Click for more info on CSV File Format"):
        st.write("Upload one CSV file about your origanisation, containing:")
        st.write("1. location (city, country)")
        st.write(
            "2. n_beneficiaries, n_staff, n_volunteers, n_activities, tot_duration, "
            "times_per_week, tot_cost, tot_budget, workhours (as dictionaries for each month)"
        )
        st.write("3. demo_beneficiaries, demo_staff, demo_volunteers (as nested dictionaries for each month)")

        st.write("Upload one CSV file about your pariticapants, containing:")
        st.write("1. ,id,gender,age,education,employment_status,start_field,end_field")
        st.write("2. start_field,end_field")



    # Example file download
    with open('data/OrganizationTable.csv', "rb") as file:
        st.sidebar.download_button(
            label="Download Example CSV for Organisation dataset",
            data=file,
            file_name='data/OrganizationTable.csv',
            mime='text/csv',
        )

    with open('data/ParticipantsTable.csv', "rb") as file:
        st.sidebar.download_button(
            label="Download Example CSV for Pariticapnt dataset",
            data=file,
            file_name='data/ParticipantsTable.csv',
            mime='text/csv',
        )
    # File uploader
    uploaded_file = st.sidebar.file_uploader("Choose Organisation data set file")
    if uploaded_file:
        ngo_df_raw = pd.read_csv(uploaded_file)
    else:
        # Load default data if no file is uploaded
       ngo_df_raw = pd.read_csv('data/OrganizationTable.csv')

    uploaded_file = st.sidebar.file_uploader("Choose Participant data set file")
    if uploaded_file:
        participant_df_raw = pd.read_csv(uploaded_file)
    else:
        # Load default data if no file is uploaded
        participant_df_raw = pd.read_csv('data/ParticipantsTable.csv')

    return deepcopy(ngo_df_raw), deepcopy(participant_df_raw)

# Main application
def main():
    st.title("Estimate Impact of your NGO project!")
    NGO_name = st.text_input('NGO name')
    st.text_input('Target area (Food, Education, Poverty)')
    st.text('Provide a CSV data set on the right')

    # Load data from sidebar
    ngo_df, participant_df = side_bar()

    # Data Exploration Section
    st.header("Data Exploration")
    st.header(f"{NGO_name} Impact Measure")

    # Creating a pie chart for gender distribution
    gender_pie = create_pie_chart(participant_df, 'gender', 'Gender Distribution')
    # Display the pie chart in Streamlit
    st.pyplot(gender_pie)

    filtered_data = participant_df[participant_df['gender'] != 'M']
    start_field_chart = create_pie_chart(filtered_data, 'start_field', 'Employment by Start Field (Excluding Males)')
    end_field_chart = create_pie_chart(filtered_data, 'end_field', 'Employment by End Field (Excluding Males)')

    st.pyplot(start_field_chart)
    st.pyplot(end_field_chart)


    # Visualizations
    plot_visualizations(ngo_df, NGO_name)


def plot_visualizations(ngo_df, NGO_name):
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


# Streamlit code for pie chart
def create_pie_chart(data_frame, column, title):
    count = data_frame[column].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(count, labels=count.index, autopct='%1.1f%%')
    plt.title(title)
    return plt



if __name__ == "__main__":
    main()
