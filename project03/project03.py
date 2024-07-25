#!/usr/bin/env python
# coding: utf-8

# In[89]:


import pandas as pd
import csv
import json

df_1 = pd.read_json("proj3_data1.json")
df_2 = pd.read_json("proj3_data2.json")
df_3 = pd.read_json("proj3_data3.json")


# In[90]:


df = pd.concat([df_1, df_2, df_3], axis=0, ignore_index=True)


# In[91]:


df.to_json("proj3_ex01_all_data.json")


# In[92]:



with open("proj3_ex02_no_nulls.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    for column in df.items():
        if column[1].isna().sum() > 0:
            writer.writerow([column[0], str(column[1].isna().sum())])


# In[93]:



with open("proj3_params.json") as json_data:
    params = json.load(json_data)


# In[94]:


concat_columns = params["concat_columns"]
df["description"] = df[concat_columns].apply(lambda x: ' '.join(x), axis=1)
df.to_json("proj3_ex03_descriptions.json")



# In[95]:


df_4 = pd.read_json("proj3_more_data.json")



# In[96]:


join_column = params["join_column"]
df_final = df.merge(df_4, on=join_column, how='left')
df_final.to_json("proj3_ex04_joined.json")



# In[97]:


for i in df_final.index:
    file_name = df_final.loc[i,'description'].replace(" ","_").lower()
    df_final.loc[i, df_final.columns != 'description'].to_json("proj3_ex05_{}.json".format(file_name))


# In[98]:


int_columns = params['int_columns']


# In[99]:


df_5 = df_final.loc[:, df_final.columns != 'description']
df_5.loc[:,int_columns] = df_5.loc[:,int_columns].astype("Int64")

for i in df_5.index:
    file_name = df_final.loc[i,'description'].replace(" ","_").lower()
    df_5.loc[i, :].to_json("proj3_ex05_int_{}.json".format(file_name))


    


# In[100]:


df_6 = pd.read_json("proj3_ex04_joined.json")

dict_6 = {}
for aggregation in params['aggregations']:
    col, func= aggregation
    name = func+"_"+col
    dict_6[name] = df_6[col].agg(func)

with open('proj3_ex06_aggregations.json', 'w') as fp:
    json.dump(dict_6, fp)   


# In[101]:


df_7 = pd.read_json("proj3_ex04_joined.json")
grouping_column = params['grouping_column']
# df_7.groupby(grouping_column).mean()
df_7 = df_7.groupby(grouping_column).filter(lambda x: len(x) > 1)
df_7 = df_7.groupby(grouping_column).mean(numeric_only=True)
df_7.to_csv("proj3_ex07_groups.csv")


# In[102]:


df_8 =  pd.read_json("proj3_ex04_joined.json")
pivot_index = params["pivot_index"]
pivot_columns = params["pivot_columns"]
pivot_values = params["pivot_values"]
df_8 = pd.pivot_table(df_8, values=pivot_values, index=pivot_index, columns=pivot_columns, aggfunc='max')
df_8.to_pickle("proj3_ex08_pivot.pkl")


# In[103]:


df_8 =  pd.read_json("proj3_ex04_joined.json")
id_vars = params["id_vars"]
df_8 = pd.melt(df_8, id_vars=id_vars)
df_8.to_csv('proj3_ex08_melt.csv', header=True, index=False)


# In[104]:


df_9 = pd.read_csv("proj3_statistics.csv")



# In[107]:


pivot_index = params['pivot_index']


df= pd.read_csv("proj3_statistics.csv")
# Melt the DataFrame to long format
df_melted = df.melt(id_vars=df.columns[0], var_name="Year_Model", value_name="Value")

# # Split the Year_Model column into Year and Model
df_melted[[pivot_index, 'Year']] = df_melted['Year_Model'].str.split('_', expand=True)
df_melted = df_melted.drop("Year_Model",axis=1)
df_melted[''] = list(zip(df_melted['Country'], df_melted['Year']))
df_melted.set_index('', inplace=True)
df_melted.sort_index(ascending=False, inplace=True)
df_melted.drop(columns=['Country', 'Year'], inplace=True)
# # # Set a MultiIndex with Model as columns and (Country, Year) as index
df_pivoted = df_melted.pivot_table(index='', columns=pivot_index, values='Value')
df_pivoted.reset_index(drop=True, inplace=False)
df_pivoted = df_pivoted[['Audi', 'BMW', 'Volkswagen', 'Renault']]
df_pivoted.to_pickle("proj3_ex08_stats.pkl")




