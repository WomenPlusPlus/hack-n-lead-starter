from dash import Dash, dcc, html, Input, Output
import plotly.express as px
#from MergeDatasets import *
import matplotlib.pyplot as plt
import pandas as pd
import ast
app = Dash(__name__)
def MergeTables(df_org, df_act, df_part):
    df_org['Activity_id'] = df_org['Activity_id'].apply(ast.literal_eval)
    df_org_dummy = df_org.explode('Activity_id').reset_index(drop=True)
    df_act['beneficiary_id'] = df_act['beneficiary_id'].apply(ast.literal_eval)
    df_act['beneficiary_dropout'] = df_act['beneficiary_dropout'].apply(ast.literal_eval)
    df_act_dummy = df_act.explode(['beneficiary_id','beneficiary_dropout']).reset_index(drop=True)
    df_1 = pd.merge(df_org_dummy, df_act_dummy, how="left", on=["Month","Activity_id"])
    df_tot = pd.merge(df_1, df_part, how="left", left_on="beneficiary_id", right_on = "id")
    df_tot.to_csv("data/TotTable.csv")
    return df_tot
def ImportDataframes():
    file_names = {'org':'data/OrganizationTable.csv'
                  ,'act':'data/ActivitiesTable.csv'
                  ,'part':'data/ParticipantsTable.csv'
                  }
    df = {}
    for key in file_names.keys():
        print(key)
        df[key] = pd.read_csv(file_names[key])
    return df
df = ImportDataframes()
df['tot'] = MergeTables(df['org'], df['act'], df['part'])


def PlotGenderDistributionPerMonth():
    months = ['January', 'February', 'March', 'April','May', 'June'
            , 'July','August','September','October', 'November', 'December']
    grouped_df = df['tot'].groupby(['gender','Month'])['Activity_id'].count().reset_index(name='counts')
    grouped_df['Month'] = pd.Categorical(grouped_df['Month'], categories=months, ordered=True)
    grouped_df.sort_values(by='Month', inplace=True)
    grouped_df.head()
    fig = px.line(grouped_df, x="Month", y="counts", title='Gender distributions/Month', color='gender')
    return fig

# PlotGenderDistributionPerMonth(df).show()