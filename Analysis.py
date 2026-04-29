import pandas as pd

df = pd.read_csv(r"C:\Users\adity\OneDrive - Durham College\Desktop\Cyclist bike analysis\Data\202503-divvy-tripdata.csv")

print(df.head())

import os
print("Current Directory:", os.getcwd())

import glob

files = glob.glob(r"C:\Users\adity\OneDrive - Durham College\Desktop\Cyclist bike analysis\Data/*.csv")

print(files)

import pandas as pd
import glob

files = glob.glob(r"C:\Users\adity\OneDrive - Durham College\Desktop\Cyclist bike analysis\Data/*.csv")

df_list = []

for file in files:
    print("Reading:", file)
    temp_df = pd.read_csv(file)
    df_list.append(temp_df)

df = pd.concat(df_list, ignore_index=True)

print("Final Data Shape:", df.shape)

print(len(files))  # how many files loaded

print("Files:", len(files))
print("Shape:", df.shape)

# Convert to datetime
df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
df['ended_at'] = pd.to_datetime(df['ended_at'], errors='coerce')

df = df.dropna(subset=['started_at', 'ended_at'])

# Create ride length
df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60

# Remove invalid rides
df = df[df['ride_length'] > 0]
df = df[df['ride_length'] < 1440]

# Checking bad rows 
print("Invalid started_at:", df['started_at'].isna().sum())
print("Invalid ended_at:", df['ended_at'].isna().sum())

# New columns
df['day_of_week'] = df['started_at'].dt.day_name()
df['month'] = df['started_at'].dt.month_name()

print(df.head()) 

print(df['member_casual'].value_counts())

# Average Ride Length
print(df.groupby('member_casual')['ride_length'].mean())

# Rides By Day of week 
print(df.groupby(['day_of_week', 'member_casual']).size())

# Rides by Month
print(df.groupby(['month', 'member_casual']).size())

"""
 # Visualisation

import seaborn as sns
import matplotlib.pyplot as plt

# Average ride length
sns.barplot(x='member_casual', y='ride_length', data=df)
plt.title("Average Ride Duration by User Type")
plt.show()

# Rides by day 
sns.countplot(x='day_of_week', hue='member_casual', data=df)
plt.xticks(rotation=45)
plt.title("Rides by Day of Week")
plt.show()

# Rides by month
sns.countplot(x='month', hue='member_casual', data=df)
plt.xticks(rotation=45)
plt.title("Rides by Month")
plt.show()

"""

# Total Rides
rides_summary = df.groupby('member_casual')['ride_id'].count().reset_index()
rides_summary.columns = ['member_casual', 'total_rides']

rides_summary.to_csv("rides_summary.csv", index=False)

# Average Ride Lenght
avg_duration = df.groupby('member_casual')['ride_length'].mean().reset_index()
avg_duration.to_csv("avg_duration.csv", index=False)

# Rides by day 
day_summary = df.groupby(['day_of_week', 'member_casual']).size().reset_index(name='rides')
day_summary.to_csv("day_summary.csv", index=False)

# Rides by month 
month_summary = df.groupby(['month', 'member_casual']).size().reset_index(name='rides')
month_summary.to_csv("month_summary.csv", index=False)

