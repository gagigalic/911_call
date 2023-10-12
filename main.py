import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("911.csv")
info = df.info()
print(info)
head = df.head()
print(head)

#top 5 zipcode for 911 calls
top_5_zipcode = df["zip"].value_counts().head(5)

#top 5 townships for 911 calls
top_5_townships = df["twp"].value_counts().head(5)

#unique title codes
unique = df["title"].nunique()
print(unique) #148

# create a reason collumn (EMS, Fire, Traffic)
df["Reason"] = df["title"].apply(lambda title: title.split(":")[0])

#common  reason for 911
common_reason = df["Reason"].value_counts().head(1)
print(common_reason) #EMS: 332692

#countplot for reason
sns.set(style = "whitegrid")
sns.countplot(x= "Reason", data = df, palette = "viridis")
plt.savefig("counplot_for_reason.png")
plt.close()

#convert the column time in Datatime object
df["timeStamp"] = pd.to_datetime(df["timeStamp"])

#Nem column for hour
df["Hour"] = df["timeStamp"].apply(lambda time: time.hour)

#Nem column for month
df["Month"] = df["timeStamp"].apply(lambda time: time.month)

#New column for day od week

df["Day of Week"] = df["timeStamp"].apply(lambda time: time.dayofweek)

#convert Day of week
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)

#Countplot of the day of week
plt.figure(figsize=(15,8))
sns.set(style = "ticks")
sns.countplot(x= "Day of Week", data = df, hue = "Reason", palette="inferno")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig("counplot_day_of_week.png")
plt.close()

#Countplot for month
plt.figure(figsize=(15,8))
sns.set(style = "ticks")
sns.countplot(x= "Month", data = df, hue = "Reason", palette="viridis")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig("counplot_month.png")
plt.close()

#Create date column
df['Date']=df['timeStamp'].apply(lambda t: t.date())

#Plot of counts of 911 calls.*
df.groupby('Date').count()['lat'].plot()
plt.tight_layout()
plt.savefig("counts_of_calls.png")
plt.close()

#Plot for traffic
df[df['Reason']=='Traffic'].groupby('Date').count()['lat'].plot()
plt.title('Traffic')
plt.tight_layout()
plt.savefig("traffic.png")
plt.close()

#Plot for fire
df[df['Reason']=='Fire'].groupby('Date').count()['lat'].plot()
plt.title('Fire')
plt.tight_layout()
plt.savefig("Fire.png")
plt.close()

#Plot for ems
df[df['Reason']=='EMS'].groupby('Date').count()['lat'].plot()
plt.title('EMS')
plt.tight_layout()
plt.savefig("ems.png")
plt.close()

#unstack method, Heatmap for Day of week and Hour
dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
plt.figure(figsize=(12, 6))
sns.heatmap(dayHour,cmap='viridis')
plt.savefig("heatmap.png")
plt.close()

#Clustermap
sns.clustermap(dayHour, cmap = "viridis")
plt.savefig("clustermap.png")
plt.close()

#unstack method, Heatmap for Day of week and Month
dayMonth = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
plt.figure(figsize=(12, 6))
sns.heatmap(dayMonth, cmap="viridis")
plt.savefig("heatmap2.png")
plt.close()

