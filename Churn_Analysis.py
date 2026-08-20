# import libraries
import numpy as np
import pandas as pd 
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# import database

connector = sqlite3.connect('customer_churn.db')

sql_query = """

SELECT name 
FROM sqlite_master
WHERE type = "table"

"""

tables = pd.read_sql(sql_query,connector)

# create dataframe for each table

for  table_name in tables ['name']:
    df = pd.read_sql(f"SELECT * FROM {table_name}", connector)
    globals() [f"df_{table_name}"] = df
    print(f"Created dataframe: df_{table_name}")

connector.close()
print(tables)


# Print table names and column names

connector = sqlite3.connect('customer_churn.db')

for table_name in tables['name']:
    print(f"\nTable Name:{table_name}")
    
    # Get column information
    columns_query = f"PRAGMA table_info ({table_name});"
    columns = pd.read_sql(columns_query,connector)
    print("Columns:")
    print(columns['name'].tolist())
    

connector.close()



# data cleaning 

print(df_db_customer.head())

print(df_db_customer.info())

print(df_db_customer.tail())

# rename column 

df_db_customer.rename(
    columns = {'name' : 'Customer Name'}
    , inplace= True
)
print(df_db_customer)

print("\n")
# changed dob datatype

df_db_customer['dob'] = pd.to_datetime(df_db_customer['dob'])
print(df_db_customer['dob'])


# a. drop column interest and pincode

#df_db_customer.drop(df_db_customer.columns[-2:],axis = 1)
#print(df_db_customer)

print(df_db_customer.drop(columns=['interests','pincode']))


#print(df_db_customer.columns[-2:])


# fix gender men, women instead of Male, Female

print(df_db_customer['gender'].unique())

print(df_db_customer['gender'].replace({'Men' : "Male", 'Women' : 'Female'}))

df_db_customer['gender'] = df_db_customer['gender'].replace({'Men' : 'Male', 'Women' : 'Female'})
print(df_db_customer)

print("\n")

print(df_db_customer.drop(columns=['interests','pincode'],inplace = True))


# fix country missing values
print(df_db_customer['country'].isna())

df_db_customer['country'] = df_db_customer['country'].fillna('NA')
print(df_db_customer['country'])

print(df_db_customer[['state','country']])

print("\n")

# country and state unique pair
# Create state → country mapping
state_country_mapping = (
    df_db_customer
    .dropna(subset=['country'])
    .set_index('state')['country']
    .to_dict()
)

# Fill missing country using state
df_db_customer['country'] = df_db_customer['country'].fillna(
    df_db_customer['state'].map(state_country_mapping)
)

# Remove any country values that are still missing
df_db_customer = df_db_customer.dropna(subset=['country'])

# Check
print(df_db_customer[df_db_customer['country'].isna()])

print(df_db_customer[['country','state']])

print("\n")

# subscription Table

print(df_db_subscription.head())

print(df_db_subscription.info())
print("\n")

date_col = ['subscription_start_date','renewal_date','cancellation_date']
df_db_subscription[date_col]= df_db_subscription[date_col].apply(pd.to_datetime)
print(df_db_subscription.info())

print("\n")

print(df_db_support.info())

print(df_db_support.head())
print("\n")

# remove col_1 and comment

df_db_support.drop(
    columns = ['col_1','comment'],
    inplace = True
    )
print(df_db_support)
print("\n")
df_db_support['complaint_date'] = pd.to_datetime(df_db_support['complaint_date'])
print(df_db_support)

print("\n")
#Feature Engineering and Data Analysis

#create churn flag

print(df_db_subscription.head(3))

df_db_subscription['churn_flag'] = np.where(df_db_subscription['cancellation_date'].notna(),1,0)
print(df_db_subscription['churn_flag'])

print("\n")
print(df_db_subscription.head())

# fix support tables duplicates and then  merge

print(df_db_subscription.merge
      (df_db_customer, on = 'customerid',how = 'left')
      .merge(df_db_support, on = 'customerid',how = 'left')
      )
'''
pd.set_option('display.max_columns', None)
print(df_db_subscription)
'''

print(df_db_subscription.shape)
print(df.shape)

print(df_db_subscription['customerid'].nunique())
print(df_db_support['customerid'].nunique())
print(df_db_support['customerid'].size)
print(df_db_customer['customerid'].unique())

df_db_support['complaint_count'] = df_db_support.groupby('customerid')['customerid'].transform('count')
print(df_db_support['complaint_count'])

print(df_db_support.sort_values('complaint_date').drop_duplicates('customerid', keep = 'last'))

print(df_db_support['customerid'].size)
print('\n')
# merge dataframe
df = df_db_subscription.merge(df_db_customer, on = 'customerid', how = 'left').merge(df_db_support, on ='customerid',how = 'left')
print(df)
print(df.shape)


print('\n')

# Data Analysis 

# DA- Churn Rate

print(df.columns)

churn_rate = df['churn_flag'].mean()*100
print("Churn Rate = ", round(churn_rate,2),"%")

# DA- retention Rate

retention_rate = 100 - churn_rate
print("Retention Rate= ", round(retention_rate,2),"%")

print("\n")


print(df.head(2))

# DA- Churn plan type

churn_by_plan = df.groupby('plan_type')['churn_flag'].mean().mul(100).round(2).reset_index(name='churn_rate_pct')
print(churn_by_plan)

print("\n")

# DA- Churn by state and sum(revenue) and count(users)

churn_by_state = df.groupby('state')['churn_flag'].mean().mul(100).round(2).reset_index(name='churn_rate_pct')
print("Churn_State:",churn_by_state)

# DA- churn by subscription type + sum(revenue) & count(users)

# Avg. Revenue per users
Avg_Revenue = df['monthly_charges'].mean()
print("Avg. Revenue:",Avg_Revenue.round(2))

#calculate customer age
#DA- Avg Customer Tenure
# count of days users had user our services : cancellation date else curret date

today =pd.Timestamp.today()
print(today)
df['tenure_days'] = np.where(
     df['cancellation_date'].notna(),
     (df['cancellation_date'] - df['subscription_start_date']).dt.days,
     (today-df['subscription_start_date']).dt.days
)

avg_tenure = df['tenure_days'].mean()
print("avg_tenure(Days)=", round(avg_tenure),0)

print(df.head())


# DA- revenue lost for churn users

revenue_loss = df.loc[df['churn_flag']== 1, 'monthly_charges'].sum()
print("Revenue at risk (RS 'K')=",revenue_loss.round(2))

# DA- Escalation Rate

print(df.columns)

print(df['escalations'].unique())

escalation_rate = (df['escalations'] == 'Y').mean()*100
print("Escalation Rate is:", escalation_rate.round(2),"%")

# DA- Avg. Complaint per user
print(df['complaint_count'].sum())

Avg_Complaint_User = df['complaint_count'].sum()/ df['customerid'].nunique()
print("Average complaint per user:", Avg_Complaint_User.round(2))


# DA- Correlation Escalation VS Churn

df['escalations'] = np.where(df['escalations'] == 'Y',1,0)
print(df['escalations'])

corr_df = df[['escalations','churn_flag']].dropna()

correlation = corr_df['escalations'].corr(df['churn_flag'])
print("The correlation between Escalations and Churn_Flag is :",(correlation).round(2))

print(df['churn_score'].head())

# DA - churn risk - create a column using existing column 

conditions = [
    (df['churn_score'] <= 50),
    (df['churn_score'] >50) & (df['churn_score'] <70),
    (df['churn_score'] >= 70)
]

risk_level = ['Low','Med','High']

df['churn_risk']= np.select(conditions, risk_level,default="unkown")
print(df['churn_risk'])

print(df[['churn_score','churn_risk']].head())


print(df.head())

print("\n")


# Visualization

df_visual = df.copy()
print(df_visual)
print(df_visual.head())
print(df_visual.shape)
print(df.columns)

#V1> Monthly Churn Trend

df_visual['cancellation_month'] = df_visual['cancellation_date'].dt.to_period('M') #Period Alias
print(df_visual['cancellation_month'])

churn_trend = (
    df_visual[df_visual['churn_flag'] == 1].groupby('cancellation_month').size()
)

print(churn_trend)

plt.figure(figsize=(8,3))

plt.plot(churn_trend.index.astype('str'), churn_trend.values, color = 'green', marker = 'o', linestyle = 'dashed', linewidth = 2,
         markersize = 12)

plt.title('Monthly Churn Trend')
plt.xlabel('Month')
plt.ylabel('Churn Flag')


print("\n")

# Churn Plan Type

#print(df_db_subscription)

churn_plan = df_visual.groupby('plan_type')['churn_flag'].mean()
plt.figure(figsize=(8,4))
colour = ['orange', 'yellow','blue']
plt.bar(churn_plan.index, churn_plan.values, color = colour)


# Churn by State

churn_state = df_visual.groupby('state')['churn_flag'].mean()
plt.figure(figsize=(14,4))
colours1 = plt.cm.Set2(np.linspace(0,1, len(churn_plan)))
plt.bar(churn_state.index, churn_state.values, color = colours1)
#plt.title('Churn by State')
#plt.show()

# Encoding str to num so we can find correlation between features

print(df.columns)

# df encoded
print(df_visual[['plan_type','contract_type','churn_score','churn_flag','churn_risk','escalations']].head())

df_encoded = df_visual[['plan_type','churn_score','churn_flag','churn_risk','escalations','contract_type']]
categorical_cols = ['plan_type','churn_risk','contract_type']

for col in categorical_cols:
    df_encoded[col] = df_encoded[col].astype('category').cat.codes

print(df_encoded.head())

# Heatmap(Correlation Matrix)

sns.heatmap(df_encoded.corr(),annot=True)

# correct mapping


df_encoded = df_visual[['plan_type','churn_score','churn_flag','churn_risk','escalations','contract_type']]
order_mappings = {
    'plan_type' : ['Basic','standard','Premium'],
    'contract_type' : ['Monthly','Annual'],
    'churn_risk': ['Low','Med','High']
}
for col, order in order_mappings.items():
    df_encoded[col] = pd.Categorical(df_encoded[col].astype('category'),categories=order,ordered=True).codes
print(df_encoded.head())

sns.heatmap(df_encoded.corr(),annot=True)


# pair plot

sns.pairplot(df_encoded)
# catplot
sns.catplot(data = df_visual,
    x= 'plan_type',
    y= 'monthly_charges',
    hue= 'gender',
    col= 'churn_risk'
    )

# pivot table
print(pd.pivot_table(
    df_visual,
    values= 'churn_flag',
    index= 'plan_type',
    aggfunc='mean'
).round(2))

print(
pd.pivot_table(
    df_visual,
    index='plan_type',
    values=['monthly_charges','customerid','churn_flag'],
    aggfunc={
        'monthly_charges' : 'sum',
        'customerid' : 'nunique',
        'churn_flag': 'mean'
    }
).round(2)
)