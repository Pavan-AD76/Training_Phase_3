# dropbox_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("dropbox_jobs_enriched.xlsx")  # enriched file
    df['post_date'] = pd.to_datetime(df['post_date'], errors='coerce')
    return df

df = load_data()

st.set_page_config(page_title="Dropbox Jobs Dashboard", layout="wide")
st.title("📊 Dropbox Jobs Dashboard")

st.sidebar.header("Filters")

# Sidebar filters
departments = st.sidebar.multiselect("Select Department(s):", df['department'].dropna().unique())
locations = st.sidebar.multiselect("Select Location(s):", df['location'].dropna().unique())

filtered_df = df.copy()
if departments:
    filtered_df = filtered_df[filtered_df['department'].isin(departments)]
if locations:
    filtered_df = filtered_df[filtered_df['location'].isin(locations)]

st.markdown(f"### Showing {len(filtered_df)} job(s)")

# --- KPI Section ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(filtered_df))
col2.metric("Unique Departments", filtered_df['department'].nunique())
col3.metric("Unique Locations", filtered_df['location'].nunique())

# --- Plots ---
st.subheader("Jobs by Department")
if not filtered_df.empty:
    dept_count = filtered_df['department'].value_counts().reset_index()
    dept_count.columns = ['department', 'count']
    fig = px.bar(dept_count, x="department", y="count", text="count",
                 color="department", title="Number of Jobs per Department")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Jobs by Location")
if not filtered_df.empty:
    loc_count = filtered_df['location'].value_counts().reset_index()
    loc_count.columns = ['location', 'count']
    fig = px.bar(loc_count, x="location", y="count", text="count",
                 color="location", title="Number of Jobs per Location")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Job Postings Over Time")
if not filtered_df.empty and filtered_df['post_date'].notna().any():
    time_series = filtered_df.groupby(filtered_df['post_date'].dt.date).size().reset_index(name="count")
    fig = px.line(time_series, x="post_date", y="count", markers=True,
                  title="Jobs Posted Over Time")
    st.plotly_chart(fig, use_container_width=True)

# --- Data Table ---
st.subheader("Job Listings")
st.dataframe(filtered_df[['job_title', 'department', 'location', 'post_date', 'url']])
