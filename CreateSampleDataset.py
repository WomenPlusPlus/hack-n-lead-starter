#%%
import pandas as pd
import random
from random import randint


#%%
random.seed(1)

#%%
months = ['January', 'February', 'March', 'April','May', 'June'
          , 'July','August','September','October', 'November', 'December']
#%%
n_activities = {month: randint(1, 5) for month in months}

#%%
def GetNSupporterEnterprises():
    supporters = [4,5,8,8,9,9,12,14,15,15,18,20]
    supporter_dic = {}
    for i,month in enumerate(months):
        print(i, month)
        supporter_dic[month] = supporters[i]
    return supporter_dic

GetNSupporterEnterprises()

#%%
def GetTotContributions():
    contribution_dic = {}
    random.seed(1)
    for i,month in enumerate(months):
        print(i, month)
        nsup = GetNSupporterEnterprises()[month]
        contribution=0
        for n in range(0,nsup):
            contribution+=2000*random.random()
        contribution_dic[month] = contribution
    return contribution_dic

GetTotContributions()

#%%                
dict_org = {'Name': 'WomenPlusPlus'
            , 'N_staff': {month: randint(5, 10) for month in months}
            , 'N_Esupporters': GetNSupporterEnterprises()
            , 'Tot_Contribution (CHF)': GetTotContributions()
            , 'N_volunteers': {month: randint(0, 10) for month in months}
            ,'N_activities': n_activities
            ,'Activity_id': {month:[i for i in range(0,n_activities[month])] for month in months}
            }


print(dict_org)
# %%
df_org = pd.DataFrame.from_dict(dict_org)
df_org.index.name='Month'
df_org.head()
# %%
df_org.to_csv("data/OrganizationTable.csv")


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
def DefineDropOut(act_id):
    rnd = random.uniform(0,1)
    threshold={'0':0.7,'1':0.9,'2':0.85,'3':0.85,'4':0.9}
    if rnd<threshold[str(act_id)]:
        return 0 #Not dropped-out
    if rnd>=threshold[str(act_id)]:
        return 1 #Dropped-out
    
def GetParticipantDropOut(npart, act_id):
    partDO = [-99]*npart
    for i in range(0,npart):
        partDO[i] = DefineDropOut(act_id)
    return partDO

#%%
avg_participation = [0.77,0.82,0.93,0.94,0.95]
    
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
    #activity['n_beneficiaries'] = activities_npart[i]
    activity['n_volunteers'] = activities_nvolunteers[i]
    activity['n_staff'] = activities_nstaff[i]
    activity['n_waitlist'] = activities_nwaitlist[i]
    activity['beneficiary_id'] = getParticipantID(nmax, activities_npart[i])
    activity['beneficiary_dropout'] = GetParticipantDropOut(activities_npart[i],i)
    activity['average_participation'] = avg_participation[i]
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
start_fields = {'Business':0.1,'Construction':0.01,'Education':0.13,'Engineering':0.1,'Farming':0.01,'Health':0.02,'Hospitality':0.04,'Law':0.02,'Management':0.02,'Media':0.05,'Administration':0.02,'Science':0.18,'IT':0.3}
end_fields = {'Business':0.09,'Construction':0.008,'Education':0.09,'Engineering':0.05,'Farming':0.009,'Health':0.018,'Hospitality':0.036,'Law':0.016,'Management':0.02,'Media':0.046,'Administration':0.019,'Science':0.14,'IT':0.458}

def check_sum_to_one(di):
    sum = 0
    for key in di.keys():
        sum+=di[key]
    print(sum)
    return

check_sum_to_one(start_fields)
check_sum_to_one(end_fields)
#%%
def getStartField(start_fields):
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
        

getStartField(start_fields)
#%%
def getEndField(start,start_fields,end_fields):
    end = ''
    if start!='IT':
        rnd = random.uniform(0,1)
        ratio = end_fields[start]/start_fields[start]
        print(ratio)
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
for i in range(0,nmax):
    participant = {}
    participant['id'] = i
    participant['gender'] = getGender()
    participant['age'] = getAge()
    participant['education'] = getEducation()
    participant['employment_status'] = getEmploymentStatus()
    participant['start_field'] = getStartField(start_fields)
    participant['end_field'] = getEndField(participant['start_field'],start_fields,end_fields)
    participants.append(participant)
    
# %%
df_part = pd.DataFrame.from_dict(participants)
df_part.head()
# %%
df_part.to_csv("data/ParticipantsTable.csv")
# %%
