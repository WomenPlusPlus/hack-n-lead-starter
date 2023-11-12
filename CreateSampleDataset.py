#%%
import pandas as pd
import random
from random import randint
#from Parameters import *
from MergeDatasets import *

TotBeneficiaries = 2000
months = ['January', 'February', 'March', 'April','May', 'June'
          , 'July','August','September','October', 'November', 'December']

years = ['2022','2023']

n_max_activity_year = {'2022':3,'2023':5}
activities_names = ['hackaton', 'workshop','networking','deploy(impact)','coffee']

# Seed for reproducibility
random.seed(1)

# Generate number of activities for each month
n_activities =[random.randint(1, 5) for month in months]

# Helper function to Generate supporter enterprises
def GenerateNSupporterEnterprises(months,n_activities):
    random.seed(1)
    supporters = [0]*len(months)
    for i in range(len(months)):
        if i==0: 
            supporters[i]=randint(1,5)
        else:
            supporters[i]=round(supporters[i-1]+(n_activities[i]*0.5),0)
    return supporters

#print(GenerateNSupporterEnterprises(months,n_activities))
#%%
# Helper function to Generate total donations
def GenerateTotDonations(months,n_activities):
    random.seed(1)
    contributions = [0]*len(months)
    nsup = GenerateNSupporterEnterprises(months,n_activities)
    for i in range(len(months)):
        contribution=0
        for n in range(0,int(nsup[i])):
            contribution+=2000*random.random()
        contributions[i] = round(contribution,0)
    return contributions

def GenerateActivityID(months, n_activities):
    act_id = [0]*len(months)
    for j in range(len(months)):
        act_id[j] = []
        for i in range(n_activities[j]):
             act_id[j].append(i)
    return act_id

# Organization table
staff_data = {
    'Month': months
    ,'N_staff': [random.randint(5, 10) for _ in range(len(months))]
    ,'Tot_Donations (CHF)': GenerateTotDonations(months,n_activities)
    ,'N_Esupporters':GenerateNSupporterEnterprises(months,n_activities)
    , 'N_volunteers':[randint(4, 15) for i in range(len(months))]
    ,'N_activities': n_activities
    ,'Activity_id':GenerateActivityID(months, n_activities)
}
df_org = pd.DataFrame.from_dict(staff_data)
df_org.head()
df_org.to_csv("data/OrganizationTable.csv")
#%%
'''
dict_org = {'N_staff': {month: randint(5, 10) for month in months}
            , 'N_Esupporters': GenerateNSupporterEnterprises()
            , 'Tot_Donations (CHF)': GenerateTotDonations()
            , 'N_volunteers': {month: randint(0, 10) for month in months}
            ,'N_activities': n_activities
            ,'Activity_id': {month:[i for i in range(0,n_activities[month])] for month in months}
            }

df_org = pd.DataFrame.from_dict(dict_org)
df_org.index.name='Month'
df_org.head()
df_org.to_csv("data/OrganizationTable.csv")
'''


#%%
# Activities table
activities_duration = [24,4,10,2,2]
activities_tperw = [2,1,1,3,1]
activities_budget = [20000,12000,5000,12000,500]
activities_cost = [18000,9034,3250,11060,450]
activities_npart = [120,50,100,60,20]
activities_nwaitlist = [20,10,1,12,0]
activities_nvolunteers = [6,4,3,6,4]
activities_nstaff = [5,6,6,6,2]

#%%    
def checkPartID(partID, rnd):
    if rnd in partID:
        return 'True'
    else:
        return 'False'
    
def GenerateParticipantID(nmax, npart):
    partID = [-99]*npart
    for i in range(npart):
        rnd =  randint(0,nmax)
        check = checkPartID(partID, rnd)
        while(check=='True'):
            rnd =  randint(0,nmax)
            check = checkPartID(partID, rnd)    
        partID[i] = rnd    
    return partID

#%%
def DefineDropOut(act_id):
    rnd = random.uniform(0,1)
    threshold={'0':0.7,'1':0.9,'2':0.85,'3':0.85,'4':0.9}
    if rnd<threshold[str(act_id)]:
        return 0 #Not dropped-out
    if rnd>=threshold[str(act_id)]:
        return 1 #Dropped-out
    
def GenerateParticipantDropOut(npart, act_id):
    partDO = [-99]*npart
    for i in range(0,npart):
        partDO[i] = DefineDropOut(act_id)
    return partDO

#%%
avg_participation = [0.77,0.82,0.93,0.94,0.95]
    
#%%


data = []

# Populate the list with dictionaries for each month
for j, month in enumerate(months):
    if j<12:
        n_act_month = n_activities[j]
        
        #Create a dictionary for the current month
        month_data = {'Month': [month] * n_act_month}
        print(month_data)
        month_data['Activity_id'] =  [i for i in range(len(month_data['Month']))]
        month_data['Tot_budget'] = [activities_budget[month_data['Activity_id'][i]]+randint(-2,2)*1000 for i in range(len(month_data['Month']))]
        month_data['Tot_cost'] = [activities_cost[month_data['Activity_id'][i]]+randint(-2,2)*random.uniform(150,200) for i in range(len(month_data['Month']))]
        month_data['n_beneficiaries'] = [activities_npart[month_data['Activity_id'][i]]+randint(-15,0) for i in range(len(month_data['Month']))]
        month_data['n_volunteers'] = [activities_nvolunteers[month_data['Activity_id'][i]]+randint(-2,2) for i in range(len(month_data['Month']))]
        month_data['n_staff'] = [activities_nstaff[month_data['Activity_id'][i]]+randint(-2,2) for i in range(len(month_data['Month']))]
        month_data['beneficiary_id'] =  [ GenerateParticipantID(TotBeneficiaries, activities_npart[month_data['Activity_id'][i]]) for i in range(len(month_data['Month']))]
        month_data['beneficiary_dropout'] = [GenerateParticipantDropOut(activities_npart[month_data['Activity_id'][i]],i) for i in range(len(month_data['Month']))]
        
        # Append the dictionary to the data list
        data.append(month_data)

activities = data
'''
              ,'Activity_id': [i for i in range(0,5)]
              ,'name':[activities_names[i] for i in range(0,5)]
              ,'Tot. duration (hours)': [activities_duration[i] for i in range(5)]
              ,'times_per_week' : [activities_tperw[i] for i in range(5)]
              ,'Tot_budget' : [activities_budget[i] for i in range(5)]
              ,'Tot_cost' : [activities_cost[i] for i in range(5)]
}
'''
'''
for j in range(len(months)):
    for i in range(0,5):
        activity = {}
        activity['id'] = i
        activity['name'] = activities_names[i]
        activity['Tot. duration (hours)'] = activities_duration[i]
        activity['times_per_week'] = activities_tperw[i]
        activity['Tot_budget'] = activities_budget[i]
        activity['Tot_cost'] = activities_cost[i]
        #activity['n_beneficiaries'] = activities_npart[i]
        activity['n_volunteers'] = activities_nvolunteers[i]
        activity['n_staff'] = activities_nstaff[i]
        activity['n_waitlist'] = activities_nwaitlist[i]
        activity['beneficiary_id'] = GenerateParticipantID(TotBeneficiaries, activities_npart[i])
        activity['beneficiary_dropout'] = GenerateParticipantDropOut(activities_npart[i],i)
        activity['average_participation'] = avg_participation[i]
        activities['Month'].append(activity)
'''

# %%
df_act = pd.DataFrame.from_dict(activities)
column_list = []
for column in df_act.columns:
    column_list.append(column)
df_act_dummy = df_act.explode(column_list).reset_index(drop=True)

df_act_dummy.head()


# %%
df_act_dummy.to_csv("data/ActivitiesTable.csv")
# %%
def GenerateGender():
    rnd = random.uniform(0,1)
    if rnd<0.7:
        return 'F'
    if rnd>=0.7 and rnd<0.88:
        return 'M'
    if rnd>=0.88 and rnd<0.95:
        return 'nonbinary'
    if rnd>0.95:
        return 'NS'

def GenerateAge():
    rnd = random.uniform(0,1)
    if rnd<0.2:
        return randint(20,30)
    if rnd>=0.2 and rnd<0.65:
        return randint(30,40)
    if rnd>=0.65 and rnd<0.85:
        return randint(40,50)
    if rnd>=0.85 and rnd<0.97:
        return randint(50,60)
    if rnd>=0.97:
        return randint(60,90)

def GenerateEducation():
    rnd = random.uniform(0,1)
    if rnd<0.1:
        return 'HighSchool'
    if rnd>=0.1 and rnd<0.4:
        return 'Bachelor'
    if rnd>=0.4 and rnd<0.75:
        return 'Master'
    if rnd>=0.75:
        return 'PhD'
    
def GenerateEmploymentStatus():
    rnd = random.uniform(0,1)
    if rnd<0.5:
        return 'Employed'
    if rnd>=0.5:
        return 'Unemployed'

#%%
start_fields = {'Business':0.1,'Construction':0.01,'Education':0.13,'Engineering':0.1,'Farming':0.01,'Health':0.02,'Hospitality':0.04,'Law':0.02,'Management':0.02,'Media':0.05,'Administration':0.02,'Science':0.18,'IT':0.3}
end_fields = {'Business':0.09,'Construction':0.008,'Education':0.09,'Engineering':0.05,'Farming':0.009,'Health':0.018,'Hospitality':0.036,'Law':0.016,'Management':0.02,'Media':0.046,'Administration':0.019,'Science':0.14,'IT':0.458}

def check_sum_to_one(di):
    sum = 0
    for key in di.keys():
        sum+=di[key]
    print(sum)
    return

#check_sum_to_one(start_fields)
#check_sum_to_one(end_fields)
#%%
def GenerateStartField(start_fields):
    rnd = random.uniform(0,1)
    #print(rnd)
    thr = [0]*(len(start_fields)+1)
    for i,key in enumerate(start_fields):
        thr[i+1]=thr[i]+start_fields[key]
    #print(thr)
    for i,key in enumerate(start_fields):
        if rnd>thr[i] and rnd<=thr[i+1]:
            #print(rnd, thr[i],thr[i+1])
            return key
        

GenerateStartField(start_fields)
#%%
def GenerateEndField(start,start_fields,end_fields):
    end = ''
    if start!='IT':
        rnd = random.uniform(0,1)
        ratio = end_fields[start]/start_fields[start]
        #print(ratio)
        if rnd<=1-ratio:
            end = 'IT'
        else:
            end = start
    else:
        end = start
    return end




#%%
#Generate participants
participants = []
for i in range(0,TotBeneficiaries):
    participant = {}
    participant['id'] = i
    participant['gender'] = GenerateGender()
    participant['age'] = GenerateAge()
    participant['education'] = GenerateEducation()
    #participant['employment_status'] = GenerateEmploymentStatus()
    participant['start_field'] = GenerateStartField(start_fields)
    participant['end_field'] = GenerateEndField(participant['start_field'],start_fields,end_fields)
    participants.append(participant)
    
df_part = pd.DataFrame.from_dict(participants)
df_part.head()
df_part.to_csv("data/ParticipantsTable.csv")

#%%
MergeTables(df_org, df_act_dummy, df_part)
# %%

#%%
'''
def MergeTables(df_org, df_act_dummy, df_part):
    df_org_dummy = df_org.explode('Activity_id')
    df_act_dummy = df_act_dummy.explode(['beneficiary_id','beneficiary_dropout']).reset_index(drop=True)
    df_1 = pd.merge(df_org_dummy, df_act_dummy, how="left", on=["Month","Activity_id"])
    df_tot = pd.merge(df_1, df_part, how="left", left_on="beneficiary_id", right_on = "id")
    return df_tot
df_tot = MergeTables(df_org, df_act_dummy, df_part)
df_tot.head()
'''
# %%
