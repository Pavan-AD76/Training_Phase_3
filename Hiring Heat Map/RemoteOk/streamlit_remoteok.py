# remoteok_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("remoteok_jobs.csv")
    df['Date Posted'] = pd.to_datetime(df['Date Posted'], errors='coerce')
    return df

df = load_data()

st.set_page_config(page_title="RemoteOK Jobs Dashboard", layout="wide")
st.title("🌍 RemoteOK Jobs Dashboard")

st.sidebar.header("Filters")

# Sidebar filters
companies = st.sidebar.multiselect("Select Company:", df['Company'].dropna().unique())
locations = st.sidebar.multiselect("Select Location:", df['Location'].dropna().unique())
departments = df['Department'].dropna().unique() if "Department" in df.columns else []

if len(departments) > 0:
    departments = st.sidebar.multiselect("Select Department:", departments)

filtered_df = df.copy()
if companies:
    filtered_df = filtered_df[filtered_df['Company'].isin(companies)]
if locations:
    filtered_df = filtered_df[filtered_df['Location'].isin(locations)]
if "Department" in filtered_df.columns and departments:
    filtered_df = filtered_df[filtered_df['Department'].isin(departments)]

st.markdown(f"### Showing {len(filtered_df)} job(s)")

# --- KPI Section ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(filtered_df))
col2.metric("Unique Companies", filtered_df['Company'].nunique())
col3.metric("Unique Locations", filtered_df['Location'].nunique())

# --- Jobs by Company ---
st.subheader("Jobs by Company")
if not filtered_df.empty:
    company_count = filtered_df['Company'].value_counts().reset_index()
    company_count.columns = ['Company', 'count']
    fig = px.bar(company_count, x="Company", y="count", text="count",
                 color="Company", title="Jobs per Company")
    st.plotly_chart(fig, use_container_width=True)

# --- Jobs by Location ---
st.subheader("Jobs by Location")
if not filtered_df.empty:
    loc_count = filtered_df['Location'].value_counts().reset_index()
    loc_count.columns = ['Location', 'count']
    fig = px.bar(loc_count, x="Location", y="count", text="count",
                 color="Location", title="Jobs per Location")
    st.plotly_chart(fig, use_container_width=True)

# --- Jobs by Department ---
if "Department" in filtered_df.columns:
    st.subheader("Jobs by Department")
    dept_count = filtered_df['Department'].value_counts().reset_index()
    dept_count.columns = ['Department', 'count']
    fig = px.bar(dept_count, x="Department", y="count", text="count",
                 color="Department", title="Jobs per Department")
    st.plotly_chart(fig, use_container_width=True)

# --- Job Postings Over Time ---
st.subheader("Job Postings Over Time")
if not filtered_df.empty and filtered_df['Date Posted'].notna().any():
    time_series = filtered_df.groupby(filtered_df['Date Posted'].dt.date).size().reset_index(name="count")
    fig = px.line(time_series, x="Date Posted", y="count", markers=True,
                  title="Jobs Posted Over Time")
    st.plotly_chart(fig, use_container_width=True)

# --- Data Table ---
st.subheader("Job Listings")
st.dataframe(filtered_df[['Job Title', 'Company', 'Location', 'Tags', 'Date Posted'] + (['Department'] if "Department" in filtered_df.columns else [])])
