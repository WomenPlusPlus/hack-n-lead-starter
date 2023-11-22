import streamlit as st
import pandas as pd
import plotly.express as px
from copy import deepcopy
import matplotlib.pyplot as plt
from PIL import Image

import Dashboard
NGO_name =''



# Function to display sidebar and handle file upload


def side_bar():
    st.markdown(f'''
        <style>
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 40rem;}}
        </style>
    ''', unsafe_allow_html=True)
    st.sidebar.title("Tell us about your NGO project")

    NGO_name = st.sidebar.text_input("NGO name")


    impact_value = st.sidebar.text_input('Key values for the impact [leave empty if unsure]')

    st.title(f"{NGO_name} Impact Measure \n {impact_value}")

    logo_file = st.sidebar.file_uploader("Your company logo")
    if logo_file:
        image = Image.open(logo_file)
        st.image(image)

    st.title(f"{NGO_name} Impact Measure")

    st.sidebar.text_input("Target area (Food, Education, Poverty)")

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
        st.write(
            "3. demo_beneficiaries, demo_staff, demo_volunteers (as nested dictionaries for each month)"
        )

        st.write("Upload one CSV file about your pariticapants, containing:")
        st.write("1. id,gender,age,education,employment_status")
        st.write("2. start_field,end_field")

    # Example file download
    with open("data/OrganizationTable.csv", "rb") as file:
        st.sidebar.download_button(
            label="Download Example CSV for Organisation dataset",
            data=file,
            file_name="data/OrganizationTable.csv",
            mime="text/csv",
        )

    with open("data/ParticipantsTable.csv", "rb") as file:
        st.sidebar.download_button(
            label="Download Example CSV for Pariticapnt dataset",
            data=file,
            file_name="data/ParticipantsTable.csv",
            mime="text/csv",
        )

    st.sidebar.text_input('Parameters in data set for your impact '
                          '[if Empty, then default is used]')

def upload_files():
    # File uploader
    # ngo_df_raw = False
    # participant_df_raw = False
    uploaded_file = st.sidebar.file_uploader("Choose Organisation data set file")
    if uploaded_file:
        ngo_df_raw = pd.read_csv(uploaded_file)
    else:
        ngo_df_raw = pd.read_csv("data/OrganizationTable.csv")

    uploaded_file = st.sidebar.file_uploader("Choose Participant data set file")
    if uploaded_file:
        participant_df_raw = pd.read_csv(uploaded_file)
    else:
        # Load default data if no file is uploaded
        participant_df_raw = pd.read_csv("data/ParticipantsTable.csv")
    return deepcopy(ngo_df_raw), deepcopy(participant_df_raw)


# Main application
def main():
    # st.title("Estimate Impact of your NGO project!")

    # Load data from sidebar
    side_bar()
    ngo_df, participant_df = upload_files()
    #
    # if st.checkbox('Show data'):
    #     ngo_df
    #     participant_df


    if st.sidebar.checkbox('Analyse data'):

        # Data Exploration Section
        # st.header("Data Exploration")

        # Creating a pie chart for gender distribution
        gender_pie = create_pie_chart(participant_df, "gender", "Gender Distribution")
        # Display the pie chart in Streamlit
        # st.pyplot(gender_pie)

        filtered_data = participant_df[participant_df["gender"] != "M"]
        start_field_chart = create_pie_chart(
            filtered_data, "start_field", "Employment by Start Field (Excluding Males)"
        )
        end_field_chart = create_pie_chart(
            filtered_data, "end_field", "Employment by End Field (Excluding Males)"
        )

        # st.pyplot(start_field_chart)
        # st.pyplot(end_field_chart)


        # Visualizations
        plot_visualizations(ngo_df, participant_df, NGO_name)


def plot_visualizations(ngo_df, participant_df, NGO_name):
    # Data aggregation for career changes
    start_field_count = participant_df.groupby(["start_field"])["start_field"].count()
    end_field_count = participant_df.groupby(["end_field"])["end_field"].count()
    transitions_df = pd.DataFrame([start_field_count, end_field_count]).T
    transitions_df.rename({"start_field": "before", "end_field": "after"}, axis=1, inplace=True)

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # 1. Line Graph for Staff and Volunteers Over Time
    row1_col1.subheader(f"Staff and Volunteers Over Time {NGO_name}")
    fig1 = px.line(ngo_df, x="Month", y=["N_staff", "N_volunteers"])
    fig1.update_layout(legend_title=None)
    row1_col1.plotly_chart(fig1)

    # 2. Bar Chart for Number of Activities Each Month
    row1_col2.subheader("Number of Activities Each Month")
    fig2 = px.bar(ngo_df, x="Month", y="N_activities")
    fig2.update_layout(legend_title=None)
    row1_col2.plotly_chart(fig2)

    # 3. Box Plot for Staff and Volunteer Variability
    # st.subheader("Staff and Volunteer Variability")
    # fig3 = px.box(ngo_df, y=["N_staff", "N_volunteers"])
    # st.plotly_chart(fig3)

    # 4. Stacked Bar Chart for Staff and Volunteers
    row2_col1.subheader("Staff and Volunteers Each Month")
    fig4 = px.bar(ngo_df, x="Month", y=["N_staff", "N_volunteers"], barmode="stack")
    fig4.update_layout(legend_title=None)
    row2_col1.plotly_chart(fig4)

    row2_col2.subheader("Career Transitions by Industry")
    fig6 = px.bar(
        transitions_df,
        x=transitions_df.index,
        y=["before", "after"],
        barmode="group",
    )
    fig6.update_layout(
        legend_title=None, xaxis_title="Industry", yaxis_title="# Participants"
    )
    row2_col2.plotly_chart(fig6)
    # 5. Scatter Plot for Staff vs. Volunteers
    # st.subheader("Staff vs. Volunteers")
    # fig5 = px.scatter(ngo_df, x="N_staff", y="N_volunteers")
    # st.plotly_chart(fig5)


# Streamlit code for pie chart
def create_pie_chart(data_frame, column, title):
    count = data_frame[column].value_counts()
    plt.figure(figsize=(4, 4))
    plt.pie(count, labels=count.index, autopct="%1.1f%%")
    plt.title(title)
    return plt




st.set_page_config(layout="wide")

if __name__ == "__main__":
    main()
