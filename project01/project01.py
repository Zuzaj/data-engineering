#!/usr/bin/env python
# coding: utf-8

# In[160]:


import pandas as pd
import json
import numpy as np


# In[161]:


df = pd.read_csv('proj1_ex01.csv')
df.head()


# In[162]:


columns_info = []
for column in df.columns:
    missing_val = df[column].isnull().mean()
    if df[column].dtype == 'int64':
        data_type = 'int'
    elif df[column].dtype == 'float64':
        data_type = 'float'
    else:
        data_type = 'other'
    column_dict = {
        'name' : column,
        'missing' : missing_val,
        'type' : data_type
    }
    columns_info.append(column_dict)


# In[163]:


print(columns_info[:5])
with open("proj1_ex01_fields.json", "w") as json_file:
    json.dump(columns_info, json_file, indent=4)


# In[164]:


stats_numerical = df.describe(include='number').to_dict()
stats_numerical


# In[165]:


other_stats = {}
for column in df.select_dtypes(exclude=['number']).columns:
    value_counts = df[column].value_counts()
    max_count = value_counts.max()
    modes = value_counts[value_counts == max_count].index.tolist()
    if len(modes) > 1:
        mode = df[column][0]
    else:
        mode = df[column].mode()[0] 
    other_stats[column] = {
         "count": int(df[column].count()),
         "unique": int(df[column].nunique()),
         "top": mode,
         "freq": int(df[column].value_counts().max())
    } 
# In[167]:


stats = {**stats_numerical, **other_stats}
print(stats)
with open("proj1_ex02_stats.json", "w") as json_file:
    json.dump(stats, json_file, indent=4)


# In[168]:


names = df.columns
new_names = []

for name in names:
    new_name = ''
    for char in name:
        if char.isalpha() or char in [' ', '_']:
            new_name += char
    new_name = new_name.lower()
    new_name = new_name.replace(' ', '_')
    new_names.append(new_name)

df.columns = new_names


# In[169]:


df.to_csv("proj1_ex03_columns.csv", index=False)


# In[170]:


df.to_excel('proj1_ex04_excel.xlsx', index=False)


# In[171]:


df.to_json('proj1_ex04_json.json', orient='records')


# In[172]:


df.to_pickle('proj1_ex04_pickle.pkl')


# In[173]:


dp = pd.read_pickle('proj1_ex05.pkl')


# In[174]:


dp = dp.iloc[:,1:3]
rows =[ x.startswith('v') for x in dp.index ]
dp = dp.loc[rows]


# In[175]:


dp = dp.fillna('')
dp.to_markdown('proj1_ex05_table.md')



# In[176]:


f = open('proj1_ex06.json')
data = json.load(f)
data
df = pd.json_normalize(data)
df.to_pickle('proj1_ex06_pickle.pkl')


# In[ ]:




