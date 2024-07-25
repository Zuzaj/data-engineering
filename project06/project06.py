#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd


con = sqlite3.connect("proj6_readings.sqlite") 
cur = con.cursor()


# In[2]:


cur.execute("""CREATE INDEX IF NOT EXISTS detector_id ON readings (detector_id);""").fetchall() 
cur.execute("""CREATE INDEX IF NOT EXISTS starttime ON readings (starttime); """).fetchall()


# In[3]:


pd.read_sql("SELECT * FROM readings LIMIT 10;", con)


# In[4]:


df_1 = pd.read_sql("SELECT COUNT(DISTINCT detector_id) FROM readings;",con)
df_1.to_pickle("proj6_ex01_detector_no.pkl")


# In[5]:


df_2 = pd.read_sql("""SELECT detector_id, COUNT(*) AS measurement_count, MIN(starttime) AS min_starttime, MAX(starttime) AS max_starttime 
FROM readings 
WHERE count IS NOT NULL 
GROUP BY detector_id;""", con)
df_2.to_pickle("proj6_ex02_detector_stat.pkl")


# In[6]:


df_3 = pd.read_sql("""SELECT detector_id, count, 
LAG(count) OVER (PARTITION BY detector_id ORDER BY starttime) AS prev_count
FROM readings
WHERE detector_id = 146
LIMIT 500;""", con)
df_3.to_pickle("proj6_ex03_detector_146_lag.pkl")


# In[7]:


df_4 = pd.read_sql("""SELECT detector_id, count, 
SUM(count) OVER (PARTITION BY detector_id ORDER BY starttime ROWS BETWEEN CURRENT ROW AND 10 FOLLOWING) AS window_sum
FROM readings
WHERE detector_id = 146
LIMIT 500;""", con)
df_4.to_pickle("proj6_ex04_detector_146_sum.pkl")


# In[ ]:




