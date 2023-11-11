#%%
import pandas as pd
import random
from random import randint

#%%
fields = ['location'                    #city, country
          ,'n_beneficiaries'            #dict[int per month]
          ,'n_staff'                    #dict[int per month]
          ,'n_volunteers'               #dict[int per month]
          ,'n_activities'               #dict[int per month]
          ,'tot_duration'               #dict[int per month]
          ,'times_per_week'             #dict[int per month]  
          ,'tot_cost'                   #dict[int per month]
          ,'tot_budget'                 #dict[int per month]
          ,'workhours'                  #dict[int per month]
          ,'demo_beneficiaries'         #dict[dict per month]
          ,'demo_staff'                 #dict[dict per month]
          ,'demo_volunteers'            #dict[dict per month]
          ]

#%%
random.seed(1)

#%%
months = ['January', 'February', 'March', 'April','May', 'June'
          , 'July','August','September','October', 'November', 'December']
#%%
n_activities = {month: randint(1, 5) for month in months}

#%%                
dict_org = {'Name': 'WomenPlusPlus'
            , 'N_staff': {month: randint(5, 10) for month in months}
            , 'N_volunteers': {month: randint(0, 10) for month in months}
            ,'N_activities': n_activities
            ,'Activity_id': {month:[i for i in range(0,n_activities[month])] for month in months}
            }

print(dict_org)
# %%
df_org = pd.DataFrame.from_dict(dict_org)
df_org.head()
# %%
df_org.to_csv("data/OrganizationTable.csv")

# %%
#activities = [{'id': 0
#                 ,'Activity_name':'hackaton'
#                 ,'Tot. duration (hours)': 48
#                 ,'Times_per_week':4
#                 ,'Tot_budget':10000
#                 ,'Tot_cost':8735
#                 ,'n_volunteers':10
#                 ,'n_staff':4
#                 ,'n_beneficiaries':120
#                 ,'beneficieary_id':[i for i in range(0,120)]
#                ,'n_waitlist': 40
#                 }]

#%%
activities_names = ['hackaton', 'workshop','networking','deploy(impact)','coffee']
activities_duration = [144,80,10,72,2]
activities_tperw = [3,1,1,3,1]
activities_budget = [20000,12000,5000,12000,500]
activities_cost = [18000,9034,3250,11060,450]
activities_npart = [120,50,100,60,18]
activities_nwaitlist = [20,10,1,12,0]
activities_nvolunteers = [8,5,4,8,5]
activities_nstaff = [5,6,6,6,2]
#%%
nmax = 200
npart = 30
    
def checkPartID(partID, rnd):
    if rnd in partID:
        return 'True'
    else:
        return 'False'
    
def getParticipantID(nmax, npart):
    partID = [-99]*npart
    for i in range(npart):
        rnd =  randint(0,nmax)
        check = checkPartID(partID, rnd)
        while(check=='True'):
            rnd =  randint(0,nmax)
            check = checkPartID(partID, rnd)    
        partID[i] = rnd
            
    return partID

partID = getParticipantID(nmax,npart)
print(partID)
#%%
activities = []
for i in range(0,5):
    activity = {}
    activity['id'] = i
    activity['name'] = activities_names[i]
    activity['Tot. duration (hours)'] = activities_duration[i]
    activity['times_per_week'] = activities_tperw[i]
    activity['Tot_budget'] = activities_budget[i]
    activity['Tot_cost'] = activities_cost[i]
    activity['n_beneficiaries'] = activities_npart[i]
    activity['n_volunteers'] = activities_nvolunteers[i]
    activity['n_staff'] = activities_nstaff[i]
    activity['n_waitlist'] = activities_nwaitlist[i]
    activity['beneficieary_id'] = getParticipantID(nmax, activities_npart[i])
    activities.append(activity)
    

# %%
df_act = pd.DataFrame.from_dict(activities)
df_act.head()
# %%
df_act.to_csv("data/ActivitiesTable.csv")
# %%
def getGender():
    rnd = random.uniform(0,1)
    if rnd<0.7:
        return 'F'
    if rnd>=0.7 and rnd<0.88:
        return 'M'
    if rnd>=0.88 and rnd<0.95:
        return 'nonbinary'
    if rnd>0.95:
        return 'NS'

def getAge():
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

def getEducation():
    rnd = random.uniform(0,1)
    if rnd<0.1:
        return 'HighSchool'
    if rnd>=0.1 and rnd<0.4:
        return 'Bachelor'
    if rnd>=0.4 and rnd<0.75:
        return 'Master'
    if rnd>=0.75:
        return 'PhD'
    
def getEmploymentStatus():
    rnd = random.uniform(0,1)
    if rnd<0.5:
        return 'Employed'
    if rnd>=0.5:
        return 'Unemployed'

#%%
#Generate participants
participants = []
for i in range(0,nmax):
    participant = {}
    participant['id'] = i
    participant['gender'] = getGender()
    participant['age'] = getAge()
    participant['education'] = getEducation()
    participant['employment_status'] = getEmploymentStatus()
    participants.append(participant)
    
# %%
df_part = pd.DataFrame.from_dict(participants)
df_part.head()
# %%
df_part.to_csv("data/ParticipantsTable.csv")