#!/usr/bin/env python
# coding: utf-8

# ## Regular Tracking + Taking Action = Positive Health Gains

# ### Setup

# In[1]:


import pathlib


# In[2]:


import pandas as pd


# In[3]:


date_partition = '20200922'


# In[4]:


home = pathlib.Path.home()


# In[5]:


data_input_path = f"{home}/small-data/apple-health-csv/full-extract/{date_partition}"


# In[6]:


study_path = f"{home}/small-data/study/health-stories/{date_partition}"


# In[7]:


pathlib.Path(study_path).mkdir(parents=True,exist_ok=True)


# In[8]:


bodymass = pd.read_csv(f"{data_input_path}/bodymass-summary.csv",parse_dates=['date'])


# In[9]:


body_weight = bodymass.rename(columns={'bodymass':'weight'})


# In[10]:


body_weight = body_weight.loc[body_weight['date']>'2018-04-01']


# ### Daily Weighing's Relationship to Weight Loss

# In[11]:


# Ignore sparse weight history prior to 2018

body_weight = body_weight.loc[body_weight['date']>'2018-04-01']


# In[12]:


daily_weight = body_weight.plot.line(title="Daily Weight, April 4, 2019 - September 22, 2020", 
                                      x='date', y='weight', 
                                      figsize=(23, 11), style='.-', 
                                      markevery=1, markersize=12, markerfacecolor='orange')


# Ignoring April-October 2018, which has sparse weigh-ins, there are two long periods of weight-loss when daily weighing takes place while two other periods show weight gain when there are barely weigh-ins between months. Regarding April-October 2018, this is the period where I practiced eating less.

# In[13]:


fig = daily_weight.get_figure()


# In[14]:


fig.savefig(f"{study_path}/daily_weight.png")


# ### Monthly Perspective

# In[15]:


weights_by_month = body_weight
del weights_by_month['unit']


# In[16]:


weights_by_month['year_month'] = weights_by_month['date'].apply(lambda x: f"{x.year}-{x.month:02}")


# In[17]:


monthly_weigh_ins = weights_by_month.groupby(by="year_month").count()


# In[18]:


monthly_weigh_ins = monthly_weigh_ins.rename(columns={"weight": "weigh_ins"})


# #### Monthly First Weigh-ins

# Apple iOS Health App has a monthly average view of weight. Having observed a few times that the first weigh-ins of each month show a bigger jump or decline in weight between months, view first monthly weigh-ins over a longer a period of time.

# In[19]:


monthly_first_weighin = weights_by_month.groupby(['year_month'], as_index = False).first().loc[:, ("year_month", "weight")]


# In[20]:


monthly_first_weighin['monthly_change'] = monthly_first_weighin['weight'].diff(periods=1)


# In[21]:


monthly_first_weighin['cumulative_change'] = monthly_first_weighin['monthly_change'].cumsum()


# In[22]:


mfwi_plot = monthly_first_weighin.plot.bar(x='year_month', 
                                y=['monthly_change', 'cumulative_change'], 
                                title="Monthly Weight Loss/Gain (lbs) (First Weigh-in Each Month)",
                                width=0.90,
                                figsize = (23, 11), ylim=(-35, 15))
                               


# In[23]:


monthly_first_weighin


# #### Monthly Averages

# In[24]:


monthly_average_weight = weights_by_month.groupby(by="year_month").mean()


# In[25]:


monthly_average_weight.columns


# In[26]:


monthly_average_weight.index


# In[27]:


# index is year_month, resetting the index results in year_month column
monthly_average_weight = monthly_average_weight.reset_index() 


# In[28]:


monthly_average_weight = monthly_average_weight.rename(columns={'weight': 'weight_lbs'})


# In[29]:


monthly_average_weight.columns


# In[30]:


maw_figure = monthly_average_weight.plot.line(title="Monthly Average Weight",
                                              figsize=(23, 11), style='.-', 
                                              markerfacecolor='orange',
                                              markersize=12)


# In[31]:


maw_figure.get_figure().savefig(f"{study_path}/monthly_average_weight.png")


# ##### Calculate monthly average weight changes

# In[32]:


monthly_average_weight['monthly_lbs_change'] = monthly_average_weight['weight_lbs'].diff(periods=1)


# In[33]:


monthly_average_weight['cumulative_lbs_change'] = monthly_average_weight['monthly_lbs_change'].cumsum()


# In[34]:


monthly_average_weight.columns


# In[35]:


mavg_deltas_plot = monthly_average_weight.plot.bar(
    x = "year_month", 
    y=['monthly_lbs_change', 'cumulative_lbs_change'], 
    title="Monthly Average Weight Loss/Gain (lbs)",
    width=0.90, figsize = (23, 11), ylim=(-35, 15))
                               


# In[36]:


monthly_average_weight


# ##### Calculate Frequency of Weigh-ins Each Month

# In[37]:


monthly_weigh_ins = weights_by_month.groupby(by="year_month").count()


# In[38]:


monthly_weigh_ins = monthly_weigh_ins.reset_index()


# In[39]:


monthly_average_weight['weigh_ins'] = monthly_weigh_ins['weight']


# In[40]:


monthly_average_weight


# In[41]:


plot_monthly_avg_lb_changes_with_weighins = monthly_average_weight.plot.bar(
    title='Number of Monthly Weigh-ins and Weight Changes',
    x='year_month',
    y=['monthly_lbs_change', 'cumulative_lbs_change', 'weigh_ins', ], 
    figsize=(23, 11), width=0.9, ylim=(-35, 35))


# In[42]:


plot_monthly_avg_lb_changes_with_weighins.get_figure().savefig(f"{study_path}/monthly-avg-changes-with-weighins")


# ##### Regular Weigh-ins and Daily Distance Covered

# In[43]:


daily_distance = pd.read_csv(f"{data_input_path}/distance-walking-running-summary.csv",parse_dates=['date'])


# In[44]:


del daily_distance['unit']


# In[45]:


daily_distance['year_month'] = daily_distance['date'].apply(lambda x : f"{x.year}-{x.month:02}")


# In[46]:


daily_distance


# **Apple Watch** is responsible for tracking distance covered. I didn't have an Apple Watch prior to October 2018.

# In[47]:


import datetime as dt


# In[48]:


daily_average_distance = daily_distance.loc[(daily_distance['date'] < 
                                             dt.datetime(2020,9,22))].groupby("year_month").mean()


# In[49]:


daily_average_distance = daily_average_distance.rename(columns={'movement_distance': 'daily_average_miles'})


# ##### Combine average daily miles with the rest of the data

# In[50]:


monthly_stats = pd.merge(daily_average_distance, monthly_average_weight, 
                         left_on='year_month', right_on='year_month', how='left')


# In[51]:


plot_monthly_stats = monthly_stats.plot.bar(
    title = 'Monthly Average Weight Losses and Gain, Regular Weigh-ins and Movement',
    x='year_month',
    y=['monthly_lbs_change', 'cumulative_lbs_change', 'weigh_ins', 'daily_average_miles'],
    figsize=(23, 11), width=0.90, ylim=(-35, 35))


# In[52]:


monthly_stats


# Regular Weigh-ins tend to spur more running and walking, which leads to weight loss. While more movement leads to weight loss, the data here don't capture how eating well and less "amplifies" weight loss.
# 
# These 29-month old data confirm what I had noticed from sparse data before 2018, i.e., whenever I have to lose weight, it is very easy and fast to lose the first ten pounds. After the first ten pounds of weight loss, it takes more work and focus to shed more weight.

# In[53]:


plot_monthly_stats.get_figure().savefig(f"{study_path}/monthly-avg-changes-tracking")


# **For future research, compare the two periods of weight decline**
