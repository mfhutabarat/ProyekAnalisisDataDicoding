import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load your data
hour_df = pd.read_csv('hour.csv')

# Memperbaiki nama kolom 
hour_df = hour_df.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'hr': 'hour',
    'weekday': 'day',
    'weathersit': 'weather',
    'hum': 'humidity',
    'cnt': 'count',
})

# Mengganti nama Season

hour_df['season'].replace(1, 'Springer', inplace=True)
hour_df['season'].replace(2, 'Summer', inplace=True)
hour_df['season'].replace(3, 'Fall', inplace=True)
hour_df['season'].replace(4, 'Winter', inplace=True)

# Tahun
hour_df['year'].replace(1, '2012', inplace=True)
hour_df['year'].replace(0, '2011', inplace=True)

# Is weekend
hour_df['workingday'].replace(1, 'Workingday', inplace=True)
hour_df['workingday'].replace(0, 'Weekend', inplace=True)

# Is holiday
hour_df['holiday'].replace(1, 'Holiday', inplace=True)
hour_df['holiday'].replace(0, 'non-Holiday', inplace=True)

# Weather
hour_df['weather'].replace(1, 'Clear', inplace=True)
hour_df['weather'].replace(2, 'Mist', inplace=True)
hour_df['weather'].replace(3, 'Light', inplace=True)
hour_df['weather'].replace(4, 'Heavy', inplace=True)

# Nama hari
hour_df['day'].replace(0, 'Sunday', inplace=True)
hour_df['day'].replace(1, 'Monday', inplace=True)
hour_df['day'].replace(2, 'Tuesday', inplace=True)
hour_df['day'].replace(3, 'Wednesday', inplace=True)
hour_df['day'].replace(4, 'Thursday', inplace=True)
hour_df['day'].replace(5, 'Friday', inplace=True)
hour_df['day'].replace(6, 'Saturday', inplace=True)

# Mengubah tipe menjadi datetime
hour_df['datetime'] = pd.to_datetime(hour_df['date'])

# membuat kolom baru dayname dan monthname dengan tipe datetime
hour_df['dayname'] = hour_df['datetime'].dt.day_name()
hour_df['monthname'] = hour_df['datetime'].dt.month_name()

# Create Streamlit app
st.title("Bike Sharing Data Analysis Dashboard")
st.write("Eksploprasi data Bike-sharing oleh:")
st.write("- Nama: <b>Muhammad Ferdiansa Hutabarat</b>", unsafe_allow_html=True)
st.write("- email: muhammad.ferdiansa.17@gmail.com")
st.write("- id Dicoding: mfhutabarat")



# Create bar plots for both casual and registered users
st.subheader("Daily Bike Sharing Analysis")
casual_daily_bike_share = hour_df.groupby('dayname')['casual'].sum().sort_values(ascending=False)
registered_daily_bike_share = hour_df.groupby('dayname')['registered'].sum().sort_values(ascending=False)
user_daily_bike_share = hour_df.groupby('dayname')['count'].sum().sort_values(ascending=False)

# Convert the data into Pandas Series
casual_daily_bike_share = pd.Series(casual_daily_bike_share)
registered_daily_bike_share = pd.Series(registered_daily_bike_share)
user_daily_bike_share = pd.Series(user_daily_bike_share)

plt.figure(figsize=(15, 5))

# Create bar plots for both casual and registered users
plt.subplot(1, 3, 1)
ax1 = sns.barplot(x=casual_daily_bike_share.index,
                  y=casual_daily_bike_share.values, palette='Blues')
ax1.set_title("Casual User Daily Bike Sharing")
ax1.set_xlabel("Day of the Week")
ax1.set_ylabel("Number of Casual Users")
plt.xticks(rotation=45)

plt.subplot(1, 3, 2)
ax2 = sns.barplot(x=registered_daily_bike_share.index,
                  y=registered_daily_bike_share.values, palette='Oranges')
ax2.set_title("Registered User Daily Bike Sharing")
ax2.set_xlabel("Day of the Week")
ax2.set_ylabel("Number of Registered Users")
plt.xticks(rotation=45)

plt.subplot(1, 3, 3)
ax2 = sns.barplot(x=registered_daily_bike_share.index,
                  y=registered_daily_bike_share.values, palette='Greens')
ax2.set_title("User Daily Bike Sharing")
ax2.set_xlabel("Day of the Week")
ax2.set_ylabel("Number of Users")
plt.xticks(rotation=45)

plt.tight_layout()
st.pyplot(plt)

st.subheader("Seasonal Bike Sharing Analysis")

casual_seasonally_bike_share = (hour_df.groupby('season')['casual'].sum().sort_values(ascending=False))
registered_seasonally_bike_share = (hour_df.groupby('season')['registered'].sum().sort_values(ascending=False))

# Create a DataFrame for easier plotting
seasonal_bike_share_df = pd.DataFrame({
    'Season': casual_seasonally_bike_share.index,  # Use the index for season names
    'Casual Users': casual_seasonally_bike_share.values,
    'Registered Users': registered_seasonally_bike_share.values
})

# Set the figure size
plt.figure(figsize=(12, 5))

# Create bar plots for both casual and registered users with adjacent bars
bar_width = 0.35
index = range(len(seasonal_bike_share_df))

plt.bar(index, seasonal_bike_share_df['Casual Users'], bar_width, color='blue', label='Casual Users')
plt.bar([i + bar_width for i in index], seasonal_bike_share_df['Registered Users'], bar_width, color='orange', label='Registered Users')

plt.xlabel('Season')
plt.ylabel('Number of Users')
plt.title('Seasonal Bike Sharing')
plt.xticks([i + bar_width / 2 for i in index], seasonal_bike_share_df['Season'])
plt.legend()

plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)
