#!/usr/bin/env python
# coding: utf-8

# In[341]:


import pandas as pd
import re
import numpy as np


# In[342]:


df = pd.read_csv('proj2_data.csv', sep='[;|]', engine='python', thousands=None)
df.head()


# In[343]:


def convert_comma_to_dot(text):
    # Regular expression pattern to match standalone numbers with comma as decimal separator
    pattern = r'(\d+,\d+)'
    # Function to replace commas with dots
    def replace_comma(match):
        return match.group().replace(',', '.')
    # Apply the regular expression pattern
    if not re.search(r'[a-zA-Z]', str(text)):
        # Apply the regular expression pattern
        return re.sub(pattern, replace_comma, str(text))
    else:
        return text

# Apply the conversion function to each element of the DataFrame
df = df.applymap(convert_comma_to_dot) 
df[['task_1','task_2', 'task_3', 'tasks_avg']] = df[['task_1','task_2', 'task_3', 'tasks_avg']].astype(float)
df


# In[344]:


df.to_pickle('proj2_ex01.pkl')


# In[345]:


new_df = df.copy()

with open("proj2_scale.txt", "r") as f:
    scale = f.read().splitlines()
scale_dict = {value: i+1 for i,value in enumerate(scale)}

print(scale_dict)


# In[346]:


for column in new_df.columns:
    if new_df[column].isin(scale).all():
        new_df[column] = new_df[column].map(scale_dict)
new_df


# In[347]:


new_df.to_pickle('proj2_ex02.pkl')


# In[348]:


df_3 = df.copy()
df_3


# In[349]:


for column in df_3.columns:
    if df_3[column].isin(scale).all():
        df_3 = df_3.astype({column: 'category'})
        df_3[column] = df_3[column].cat.set_categories(scale)
df_3.dtypes
df_3.to_pickle('proj2_ex03.pkl')
df_3


# In[350]:


df_4 = df.copy()

# Function to extract numbers from a string
def extract_number(text):
    # Regular expression pattern to match numbers
    pattern = r'[-+]?\d*[\.,]?\d+'
    match = re.search(pattern, str(text))
    if match:
        return float(match.group().replace(",","."))  # Convert the matched string to a float
    else:
        return None  # Return None if no number found

# Create a DataFrame to store extracted numbers
extracted_numbers_df = pd.DataFrame()

# Iterate over non-numeric columns
for column in df_4.select_dtypes(exclude='float64'):
    # Scan strings for numbers and extract the first one
    extracted_numbers_df[column] = df_4[column].apply(extract_number)
    
extracted_numbers_df = extracted_numbers_df.dropna(axis=1, how='all')
# Save the DataFrame with extracted numbers to a pickle file
extracted_numbers_df.to_pickle('proj2_ex04.pkl')
extracted_numbers_df


# In[351]:


df_5 = df.copy()


# In[352]:


selected_cols = []
for column in df_5.select_dtypes(include='object'):
    unique_val = df_5[column].unique()
    if((len(unique_val)<=10) and all(value.islower() for value in unique_val) and
        not any(value in scale for value in unique_val)):
        selected_cols.append(column)
print(selected_cols)
    


# In[353]:


for i, col in enumerate(selected_cols):
    encoded_df = pd.get_dummies(df_5[col])
    encoded_df.columns = encoded_df.columns.str.replace(' ', '_')
    encoded_df.to_pickle(f"proj2_ex05_{i+1}.pkl")
    print(encoded_df)
    



