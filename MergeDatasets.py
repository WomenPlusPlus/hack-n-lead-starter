import pandas as pd

def ExplodeDatasets(df_org, df_act):
    df_org_dummy = df_org.explode('Activity_id')
    df_act_dummy = df_act.explode(['beneficiary_id','beneficiary_dropout']).reset_index(drop=True)
    return df_org_dummy,df_act_dummy
#%%
def MergeTables(df_org, df_act, df_part):
    df_org_dummy,df_act_dummy = ExplodeDatasets(df_org, df_act)
    df_1 = pd.merge(df_org_dummy, df_act_dummy, how="left", left_on="Activity_id",right_on= "id")
    df_tot = pd.merge(df_1, df_part, how="left", left_on="beneficiary_id", right_on = "id")
    df_tot.to_csv("data/TotTable.csv")
    return df_tot

