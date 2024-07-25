#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd
import json


# In[60]:


with open("proj5_params.json") as json_data:
    params = json.load(json_data)


# In[61]:


#ex 1
df = pd.read_csv("proj5_timeseries.csv")
df.columns = df.columns.str.lower().str.replace(r"[^a-z]", "_", regex=True)
df['date'] = pd.to_datetime(df['date'], format='mixed')
df.set_index('date', inplace=True)
df = df.asfreq(params['original_frequency'])
df.to_pickle("proj5_ex01.pkl")


# In[62]:


#ex 2
df_target = df.copy()
df_target = df_target.asfreq(params['target_frequency'])
df_target.to_pickle("proj5_ex02.pkl")


# In[63]:


#ex 3
df_downsample = df.copy()
df_downsample = df_downsample.resample(str(params['downsample_periods'])+params['downsample_units']).sum(min_count=params['downsample_periods'])
df_downsample.to_pickle("proj5_ex03.pkl")


# In[64]:


#ex 4
df_upsample = df.copy()
df_upsample = df_upsample.resample(str(params['upsample_periods'])+params['upsample_units']).interpolate(params['interpolation'], order=params['interpolation_order'])
freq_ratio = pd.Timedelta(params['upsample_periods'], params['upsample_units']) / pd.Timedelta(1, params['original_frequency'])
df_upsample = df_upsample * freq_ratio
df_upsample.to_pickle("proj5_ex04.pkl")


# In[65]:


#ex 5 
df = pd.read_pickle("proj5_sensors.pkl")
dfp = df.pivot(columns='device_id', values='value')
new_index = pd.date_range(start=dfp.index.round('1min').min(), end=dfp.index.round('1min').max(), freq=str(params['sensors_periods']) + str(params['sensors_units']))
dfp.reindex(new_index)   
dfp2 = dfp.reindex(new_index.union(dfp.index)).interpolate()
dfp3 = dfp2.reindex(new_index)
dfp3 = dfp3.dropna()
dfp3.to_pickle("proj5_ex05.pkl")


# In[ ]:




