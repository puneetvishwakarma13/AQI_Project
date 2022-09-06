# -*- coding: utf-8 -*-
"""AQI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AxZj-xjlVCNmcjHeYlweLnBmBhXzucFA

# **Importing Libraries**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
#import matplotlib.dates as mdates

"""# **Importing the Dataset**"""

df = pd.read_csv("AQI.csv").sort_values(by=['City','Date'])#sorting by city and date.
df.head()

"""# **Check Null Values**"""

df.info() #Print a Concise Summary of Dataframe

df.isnull().sum() #sum(count) of null values.

"""# **Unique values and Count of columns**"""

for i in df.columns:
    print('column name:{}     unique values:{}'.format(i,len(df[i].unique())))  #Finds all the Unique Values Within the df.

cities = df['City'].value_counts()   #Return a Series containing counts of unique values.
print(f'Total no. of different cities in the dataset : {len(cities)}')
print(cities.index)  #priting the unique values of column 'City'

"""# **Filling Null Values**"""

df['PM2.5']=df['PM2.5'].fillna(df['PM2.5'].mean())
df['PM10']=df['PM10'].fillna(df['PM10'].mean())
df['NO']=df['NO'].fillna(df['NO'].mean())
df['NO2']=df['NO2'].fillna(df['NO2'].mean())
df['NOx']=df['NOx'].fillna(df['NOx'].mean())
df['NH3']=df['NH3'].fillna(df['NH3'].mean())
df['CO']=df['CO'].fillna(df['CO'].mean())
df['SO2']=df['SO2'].fillna(df['SO2'].mean())
df['O3']=df['O3'].fillna(df['O3'].mean())
df['Benzene']=df['Benzene'].fillna(df['Benzene'].mean())
df['Toluene']=df['Toluene'].fillna(df['Toluene'].mean())
df['Xylene']=df['Xylene'].fillna(df['Xylene'].mean())
df['AQI']=df['AQI'].fillna(df['AQI'].mode()[0])
df['AQI_Bucket']=df['AQI_Bucket'].fillna('Moderate')

df.info()

"""# **Average Amount Of Pollution In Every City**"""

df.describe()   #Generate descriptive statistics.

df.reset_index(drop=True,inplace=True)
df.head()

"""# **Most Polluted cities**"""

most_polluted = df[['City', 'AQI', 'PM10','PM2.5', 'CO','NO', 'NO2','SO2','O3']].groupby(['City']).mean().sort_values(by = 'AQI', ascending = False)
most_polluted

"""## **Plotting graph of most polluted cities**"""

plt.style.use('seaborn-whitegrid')
f, ax_ = plt.subplots(1,7, figsize = (20,8))
bar1=sns.barplot(x = most_polluted.AQI, y = most_polluted.index, palette='RdBu',ax=ax_[0]);
bar1=sns.barplot(x = most_polluted.sort_values(by="PM10",ascending=False)['PM10'] , y = most_polluted.index, palette='RdBu',ax=ax_[1]);
bar1=sns.barplot(x = most_polluted.sort_values(by="PM2.5",ascending=False)['PM2.5'] , y = most_polluted.index, palette='RdBu',ax=ax_[2]);
bar1=sns.barplot(x = most_polluted.sort_values(by='CO',ascending=False)['CO'], y = most_polluted.index, palette='RdBu',ax=ax_[3]);
bar1=sns.barplot(x = most_polluted.sort_values(by='NO',ascending=False)['NO'] , y = most_polluted.index, palette='RdBu',ax=ax_[4]);
bar1=sns.barplot(x = most_polluted.sort_values(by='SO2',ascending=False)['SO2'] , y = most_polluted.index, palette='RdBu',ax=ax_[5]);
bar1=sns.barplot(x = most_polluted.sort_values(by='O3',ascending=False)['O3'] , y = most_polluted.index, palette='RdBu',ax=ax_[6]);

titles = ['AirQualityIndex', 'ParticulateMatter10','ParticulateMatter2.5', 'CO', 'NO', 'SO2', 'O3']
for i in range(7) :
    ax_[i].set_ylabel('')   
    ax_[i].set_yticklabels(labels = ax_[i].get_yticklabels(),fontsize = 10);
    ax_[i].set_title(titles[i])
    f.tight_layout()

"""### Correlation"""

cor = df.corr()
heatmap_df= cor.drop(['NOx', 'NH3','O3','Toluene','Xylene', 'AQI']).drop(['NOx', 'NH3','O3','Toluene','Xylene', 'AQI'], axis=1)
f, ax = plt.subplots(figsize = (10,10))
sns.heatmap(heatmap_df, vmax = 1, square = True, annot = True)

"""# **Graph of Pollutants in every City.**"""

df[['PM2.5','City']].groupby(['City']).median().sort_values("PM2.5", ascending = False).plot.bar(color='#2C2891')
df[['PM10','City']].groupby(['City']).median().sort_values("PM10", ascending = False).plot.bar(color='#FFB319')
df[['NO','City']].groupby(['City']).median().sort_values("NO", ascending = False).plot.bar(color='#39A388')
df[['NO2','City']].groupby(['City']).median().sort_values("NO2", ascending = False).plot.bar(color='#FFB830')
df[['CO','City']].groupby(['City']).median().sort_values("CO", ascending = False).plot.bar(color='#FF2442')
df[['SO2','City']].groupby(['City']).median().sort_values("SO2", ascending = False).plot.bar(color='#80ED99')
df[['O3','City']].groupby(['City']).median().sort_values("O3", ascending = False).plot.bar(color='#EC9CD3')
df[['Benzene','City']].groupby(['City']).median().sort_values("Benzene", ascending = False).plot.bar(color='#F037A5')

"""# **Analaysis of data using Time Series**"""

# convert column to datetime
df['Date'] = pd.to_datetime(df['Date'])

pollutants = ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene','Xylene','AQI'] #Creating a list for Pollutants

"""## Plotting the Color Map for Every Month throughout the years"""

df['month'] = pd.DatetimeIndex(df['Date']).month        #Returns Immutable ndarray-like of datetime64 data
mth_dic = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'} #Creating a dict of months
df['month']=df['month'].map(mth_dic)              #Mapping of dict with index
df.groupby('month')[pollutants].mean().plot(figsize=(12,6), cmap='Spectral')    
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.xticks(np.arange(12), mth_dic.values())
plt.ylabel('Concentration per Cubic Meter')

"""# **Analysis of AQI during Covid 19 Pandemic of Major Cities**"""

cities = ['Ahmedabad','Delhi','Bengaluru','Mumbai','Hyderabad','Chennai','Lucknow']  #Major Cities 
filter_city_date = df[df['Date'] >= '2019-01-01']
AQI = filter_city_date[filter_city_date.City.isin(cities)][['Date','City','AQI','AQI_Bucket']] #taking values only after 2019
AQI.head()

"""# Comparing AQI Before and After Lockdown using Line Graph"""

subplot_titles=["Bengaluru","Chennai","Delhi",'Hyderabad','Mumbai', "Ahmedabad","Lucknow"]     #Create a figure and a set of subplots
x_line_annotation = datetime.date(2020, 3, 25)    #Lockdown Date
f, axes = plt.subplots(7, 1, figsize=(15, 15), sharex=True)       #Sharex controls sharing of properties among x or y axes
for count, title in enumerate(subplot_titles):
    ax = AQI[AQI['City']==title].plot(x='Date', y='AQI', kind='line', ax=axes[count], color='#161E54')
    ax.title.set_text(title)
    ax.set_xlim([datetime.date(2019, 1, 1), datetime.date(2020, 7, 1)])
    ax.axvline(x=x_line_annotation, linestyle='dashed', alpha=1, color='#FF0000')

"""From Above Line Graphs we can conclude that:

-The Value Of Aqi gradually increases during January to May

-The Value Of Aqi gradually decreases during June to September

-But After the Lockdown, the value decreses drastically over the all major cities

# **Creating Pivot Tables**
"""

AQI_pivot = AQI.pivot(index='Date', columns='City', values='AQI')       #Pivot returns reshaped DataFrame
AQI_pivot.head()

AQI_beforeLockdown = AQI_pivot['2020-01-01':'2020-03-25']
AQI_afterLockdown = AQI_pivot['2020-03-26':'2020-07-01']
df1= pd.DataFrame(AQI_beforeLockdown.mean().reset_index())
df2= pd.DataFrame(AQI_afterLockdown.mean().reset_index())
df3=df1.merge(df2, on='City')
df3 = df3.rename({'0_x': 'BeforeLockdown', '0_y': 'AfterLockdown'}, axis=1)

"""## **Bar Plot for Comparision**"""

df3.reset_index().plot(x="City", y=["BeforeLockdown", "AfterLockdown"], kind="bar",figsize=(16,8))
plt.title("Comparision Of AQI Before and After Lockdown")
plt.xlabel("Cities")
plt.ylabel("AQI")
plt.show()

"""-The mean AQI value for Mumbai went from moderate(148.77) to satisfactory(64.35)

-The mean AQI value for Ahmedabad went from very poor(372.4) to moderate(118.8)

-The mean AQI value for Delhi went from poor(246.3) to moderate(125.27)

-The mean AQI value for Hyderabad went from moderate(94.43) to satisfactory(64.67)

-The mean AQI value for Bengaluru went from moderate(96) to satisfactory(65.4)

-The mean AQI value for Chennai went from moderate(80.31) to satisfactory(80.1)

**Creating a copy of dataframe**
"""

df_cpy=df.copy()
sub_set=df_cpy[df_cpy['City'].isin(['Ahmedabad','Delhi','Mumbai','Chennai','Hyderabad','Lucknow'])]

sub_set.head()

sub_set.groupby('City')['AQI_Bucket'].value_counts().to_frame()   #Creating a dataframe

plt.figure(figsize=(20,10))
sub_set.groupby('City')['AQI_Bucket'].value_counts().sort_values(ascending=False).plot.bar(color=['#ff4000','#ff8000','#ffbf00','#ffff00','#bfff00','#80ff00','#40ff00','#00ff00','#00ff40','#00ff80','#00ffbf','#00ffff','#00bfff','#0080ff','#0040ff','#0000ff','#4000ff','#8000ff','#bf00ff','#ff00ff','#ff00bf','#ff0080','#ff0040','#ff0000','#660000','#4d0000','#330000'],edgecolor='black')
plt.show()

list=['Good','Moderate','Satisfactory','Poor','Very Poor','Severe']

plt.figure(figsize=(12,12))
plt.pie(df_cpy['AQI_Bucket'].value_counts()
[0:6],labels=(df_cpy['AQI_Bucket'].value_counts()
[0:6].keys()),autopct='%0.1f%%')

plt.figure(figsize=(20,10))
pollutants1 = ['NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene','Xylene']
df_cpy.boxplot(pollutants1)