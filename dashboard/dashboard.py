import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_daily_df(df):
    daily_df = df.resample(rule='D', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })
    daily_df = daily_df.reset_index()
    daily_df.rename(columns={
        "registered": "registered_users",
        "casual": "casual_users",
        "cnt": "total_users"
    }, inplace=True)

    return daily_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").sum().reset_index()
    byseason_df.rename(columns={
        "cnt": "total_users"
    }, inplace=True)

    return byseason_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit").sum().reset_index()
    byweather_df.rename(columns={
        "cnt": "total_users"
    }, inplace=True)

    return byweather_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by="holiday").sum().reset_index()
    byholiday_df.rename(columns={
        "cnt": "total_users"
    }, inplace=True)

    return byholiday_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by="weekday").sum().reset_index()
    byweekday_df.rename(columns={
        "cnt": "total_users"
    }, inplace=True)

    return byweekday_df

url = 'https://raw.githubusercontent.com/ffdhil/Bike_Rental/main/dashboard/day_df_data.csv'
all_df = pd.read_csv(url)

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

daily_df = create_daily_df(main_df)
byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(main_df)
byholiday_df = create_byholiday_df(main_df)
byweekday_df = create_byweekday_df(main_df)

st.header('Bike Rental Dashboard :sparkles:')

st.subheader('Daily Users')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_users = daily_df.total_users.sum()
    st.metric("Total Users", value=total_users)
 
with col2:
    total_registered = daily_df.registered_users.sum()
    st.metric("Registered Users", value=total_registered)

with col3:
    total_casual = daily_df.casual_users.sum()
    st.metric("Casual Users", value=total_casual)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_df["dteday"],
    daily_df["total_users"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Based on Season and Weather")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="total_users", 
        x="season",
        data=byseason_df.sort_values(by="season", ascending=False),
        ax=ax
    )
    ax.set_title("Total Users by Season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="total_users", 
        x="weathersit",
        data=byweather_df.sort_values(by="weathersit", ascending=False),
        ax=ax
    )
    ax.set_title("Total Users by Weather", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.subheader("Based on Holiday and Weekday")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="total_users", 
        x="holiday",
        data=byholiday_df.sort_values(by="holiday", ascending=False),
        ax=ax
    )
    ax.set_title("Total Users by Holiday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="total_users", 
        x="weekday",
        data=byweekday_df.sort_values(by="weekday", ascending=False),
        ax=ax
    )
    ax.set_title("Total Users by Days", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.caption('Copyright (c) Fadhilah Akhbar')