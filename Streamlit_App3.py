# -*- coding: utf-8 -*-
"""
PM10 Air Quality Analysis Dashboard
Author: Dr Z.O.Z Sibisi
"""

import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="PM10 Analysis Dashboard",
    layout="wide"
)

# ---------------------------
# Constants
# ---------------------------
WHO_PM10 = 15
SA_PM10 = 40

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]

# ---------------------------
# Load Default Dataset (GitHub)
# ---------------------------
@st.cache_data
def load_default_data():
    return pd.read_csv(
        "Streamlit_PM_Data.csv",
        sep=";",
        decimal=","
    )

df = load_default_data()

# ---------------------------
# Optional Upload (Override)
# ---------------------------
uploaded_file = st.file_uploader(
    "Upload a CSV to override the default dataset",
    type="csv"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=None, engine="python")

# ---------------------------
# Clean Data
# ---------------------------
df.columns = df.columns.str.strip()

if "Month" in df.columns:
    df.rename(columns={"Month": "month"}, inplace=True)

df["Year"] = (
    df["Year"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(int)
)

df["PM10"] = (
    df["PM10"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)
df["PM10"] = pd.to_numeric(df["PM10"], errors="coerce")

df["month"] = df["month"].astype(str).str.strip()
df = df[df["month"].isin(MONTH_ORDER)]

df["Season"] = df["Season"].astype(str).str.strip()

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.header("Researcher Profile")
    st.write("**Name:** Dr Z.O.Z Sibisi")
    st.write("**Field:** Air Quality")
    st.write("**Department:** Environmental Science")
    st.write("**Institution:** University of Science")
    st.markdown("---")

# ---------------------------
# Header Image
# ---------------------------
st.image(
    "https://www.binbin.tech/wp-content/uploads/2024/10/64218ccad12eede4d0ad5792_wide-angle-shot-white-smoke-coming-out-nuclear-plants.jpg",
    caption="Air pollution: Are we slowly killing our future?"
)

# ---------------------------
# Main Title
# ---------------------------
st.title("PM10 Air Quality Analysis Dashboard")
st.markdown(
    "PM10 trends compared with **WHO** and **South African National Air Quality Standards (NAAQS)**."
)

st.caption(
    "Default dataset is archived in the GitHub repository. "
    "Users may upload alternative datasets for comparison."
)

# ---------------------------
# Summary Metric
# ---------------------------
st.metric(
    "Average PM10 Concentration",
    f"{df['PM10'].mean():.2f} µg/m³"
)

st.divider()

# ---------------------------
# Annual Mean Trends (BAR PLOT)
# ---------------------------
st.subheader("Annual Mean PM10 Concentration")

yearly_mean = df.groupby("Year", as_index=False)["PM10"].mean()

bars = alt.Chart(yearly_mean).mark_bar().encode(
    x=alt.X("Year:O", title="Year"),
    y=alt.Y("PM10:Q", title="PM10 (µg/m³)"),
    tooltip=["Year", alt.Tooltip("PM10:Q", format=".2f")]
)

who_line = alt.Chart(
    pd.DataFrame({"PM10": [WHO_PM10]})
).mark_rule(
    color="red",
    strokeDash=[6, 6],
    size=2
).encode(y="PM10")

sa_line = alt.Chart(
    pd.DataFrame({"PM10": [SA_PM10]})
).mark_rule(
    color="orange",
    size=2
).encode(y="PM10")

st.altair_chart(
    (bars + who_line + sa_line).properties(height=400),
    use_container_width=True
)

st.caption(f"🔴 WHO: {WHO_PM10} µg/m³ | 🟠 SA NAAQS: {SA_PM10} µg/m³")

# ---------------------------
# Monthly Patterns
# ---------------------------
st.subheader("Monthly PM10 Patterns")

monthly_mean = df.groupby("month", as_index=False)["PM10"].mean()

m1, m2 = st.columns(2)

with m1:
    bar_month = alt.Chart(monthly_mean).mark_bar().encode(
        x=alt.X("month:N", sort=MONTH_ORDER, title="Month"),
        y=alt.Y("PM10:Q", title="PM10 (µg/m³)"),
        tooltip=["month", alt.Tooltip("PM10:Q", format=".2f")]
    ).properties(height=350)
    st.altair_chart(bar_month, use_container_width=True)

with m2:
    line_month = alt.Chart(monthly_mean).mark_line(point=True).encode(
        x=alt.X("month:N", sort=MONTH_ORDER, title="Month"),
        y=alt.Y("PM10:Q", title="PM10 (µg/m³)"),
        tooltip=["month", alt.Tooltip("PM10:Q", format=".2f")]
    ).properties(height=350)
    st.altair_chart(line_month, use_container_width=True)

# ---------------------------
# Seasonal Distribution
# ---------------------------
st.subheader("Seasonal PM10 Distribution")

boxplot = alt.Chart(df).mark_boxplot(
    extent="min-max",
    size=40,
    rule=False,
    ticks=False
).encode(
    x=alt.X("Season:N", sort=SEASON_ORDER),
    y=alt.Y("PM10:Q", title="PM10 (µg/m³)", scale=alt.Scale(domain=[0, 100], clamp=True)),
    color=alt.Color("Season:N", legend=None),
    tooltip=["Season", alt.Tooltip("PM10:Q", format=".2f")]
).properties(height=400)

st.altair_chart(boxplot, use_container_width=True)

# ---------------------------
# Contact
# ---------------------------
st.header("Contact Information")
email = "sibisizoz99@gmail.com"
st.write(f"You can reach Dr Z.O.Z Sibisi at {email}.")
#st.write("**Email:** sibisizoz99@gmail.com")
