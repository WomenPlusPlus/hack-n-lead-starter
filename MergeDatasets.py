import pandas as pd

#%%
def MergeTables(df_org, df_act_dummy, df_part):
    df_org_dummy = df_org.explode('Activity_id')
    df_act_dummy = df_act_dummy.explode(['beneficiary_id','beneficiary_dropout']).reset_index(drop=True)
    df_1 = pd.merge(df_org_dummy, df_act_dummy, how="left", on=["Month","Activity_id"])
    df_tot = pd.merge(df_1, df_part, how="left", left_on="beneficiary_id", right_on = "id")
    df_tot.to_csv("data/TotTable_2.csv")
    return df_tot

