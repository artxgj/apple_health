#!/usr/bin/env python
# coding: utf-8

# Downloaded from Jupyter notebook; reorganize code later.


# # Comparing Averages To See How Fitness Level Improvements

# In[1]:


import pathlib


# In[2]:


import pandas as pd


# In[3]:


home = pathlib.Path.home()


# In[4]:


study_path = f"{home}/small-data/study/apple-watch-health-tracking/story-data"
average_pace_translated = pd.read_csv(f"{study_path}/fitness-average-pace-translated.csv")
average_movement_distance = pd.read_csv(f"{study_path}/fitness-average-movement-distance.csv")
average_run_distance = pd.read_csv(f"{study_path}/fitness-average-run-distance.csv")

average_distances = pd.merge(average_movement_distance, 
                             average_run_distance,
                             left_on="Interval", right_on="Interval")

average_distances.rename(columns={
    'Days_x': 'Move Days',
    'Days_y': 'Run Days',
    'Mean_x': 'Move Distance Average',
    'Mean_y': 'Run Distance Average'
}, inplace=True)

average_weights = pd.read_csv(f"{study_path}/fitness-average-weight-translated.csv")


average_vo2max = pd.read_csv(f"{study_path}/fitness-average-vo2max-translated.csv")

weight_vo2max = pd.merge(average_weights, average_vo2max, 
                         left_on='Interval', right_on='Interval')


weight_vo2max.rename(columns={
    'Days_x': 'Weighin Days',
    'Days_y': 'VO2Max Days',
    'Translated Mean_x': 'Translated Weight Average',
    'Translated Mean_y': 'Translated VO2Max Average'
}, inplace=True)


average_rhr = pd.read_csv(f"{study_path}/fitness-average-restheart-translated.csv")

weight_vo2max_rhr = pd.merge(weight_vo2max, average_rhr, 
                             left_on='Interval', right_on='Interval')


weight_vo2max_rhr.rename(columns={
    "Translated Mean": "Translated Resting Heart Rate Average",
    "Days": "RHR Days"
}, inplace=True)

runpace_weight_vo2max_rhr = pd.merge(average_pace_translated, weight_vo2max_rhr,
                                     left_on='Interval', right_on='Interval')


runpace_weight_vo2max_rhr.rename(columns={
    "Days": "Run Pace Days",
    "Translated Mean": "Translated Run Pace"
}, inplace=True)


all_averages = pd.merge(average_distances, runpace_weight_vo2max_rhr,
                        left_on='Interval', right_on='Interval')

"""
all_averages.plot.bar(    
    title='Days and Average Distance (Miles)',
    x='Interval', 
    y=["Move Days", "Move Distance Average", "Run Days", "Run Distance Average"],
    figsize=(17, 7),
    rot=0,
    ylim=[-1, 32])


all_averages.plot.line(
    title='Monthly Averages: Weight, Run Pace, VO2 Max, and Resting Heart Rate',
    x='Interval', 
    y=['Translated Weight Average', 'Translated Run Pace', 'Translated VO2Max Average', 'Translated Resting Heart Rate Average'],
    figsize=(8, 7),
    ylim=(-1, 17),
    markevery=1, markersize=8, style='.-', )


# In[22]:


all_averages.plot.bar(
    x="Interval", 
    y=['Translated Weight Average', 
       'Translated Run Pace',
       'Translated Resting Heart Rate Average',
       'Translated VO2Max Average' 
       ],
    title='Changes in Weight, Run Pace, Resting Heart Rate and VO2 Max', 
    rot=0,
    figsize=(17, 11),
    ylim=[-1, 17])


all_averages.loc[:, ["Interval", "Move Days", "Move Distance Average", "Run Days", "Run Distance Average", 
                     "Translated Weight Average", "Translated Run Pace", 
                     "Translated Resting Heart Rate Average", "Translated VO2Max Average"]]


# In[24]:


all_averages.plot.bar(
    title='Monthly Averages (Real and Translated)',
    x='Interval', 
    y=['Move Days', 'Move Distance Average', 'Run Days', 'Run Distance Average',
        'Translated Weight Average',  'Translated Run Pace', 
       'Translated Resting Heart Rate Average', 'Translated VO2Max Average',],
    figsize=(19, 11), rot=0,
    ylim=(-1, 41))


# In[25]:
"""

all_averages.to_csv(f"{study_path}/fitness-combined-average-for-story.csv", index=False)

