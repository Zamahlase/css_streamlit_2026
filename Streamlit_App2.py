# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 15:51:40 2026
@author: DELL Precision
"""

import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------
# Page Configuration
# ---------------------------

# Title of the app
#st.title("PM10 dashboard analysis", layout="wide")

# Collect basic information
name = "Dr. Z.O.Z Sibisi"
#field = "Air Quality"
#institution = "University of Science"

st.set_page_config(page_title="PM10 Analysis Dashboard", layout="wide")

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


st.image(
    "https://www.binbin.tech/wp-content/uploads/2024/10/64218ccad12eede4d0ad5792_wide-angle-shot-white-smoke-coming-out-nuclear-plants.jpg",
    caption="Air pollution: Are we slowly killing our future ?"
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
# Main Header
# ---------------------------
st.title("PM10 Air Quality Analysis Dashboard")
st.markdown("PM10 trends compared with **World Health Organisation** and **South African (SA)** national air quality standards.")

# ---------------------------
# Upload
# ---------------------------
uploaded_file = st.file_uploader(
    "Choose a CSV file (Expected columns: Year, Month, Season, PM10)",
    type="csv"
)

if uploaded_file:

    # ---------------------------
    # Load & Clean Data
    # ---------------------------
    df = pd.read_csv(uploaded_file, sep=None, engine="python")
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
    # Summary Metric
    # ---------------------------
    st.metric(
        "Average PM10 Concentration",
        f"{df['PM10'].mean():.2f} µg/m³"
    )

    st.divider()

    # ---------------------------
    # Annual Mean Trends
    # ---------------------------
    st.subheader("Annual Mean Trends")

    yearly_mean = df.groupby("Year", as_index=False)["PM10"].mean()

    bars = alt.Chart(yearly_mean).mark_bar(color="#4A90E2").encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("PM10:Q", title="PM10 (µg/m³)"),
        tooltip=["Year", alt.Tooltip("PM10:Q", format=".2f")]
    )

    who_line = alt.Chart(
        pd.DataFrame({"y": [WHO_PM10]})
    ).mark_rule(
        color="red",
        strokeDash=[5, 5],
        size=2
    ).encode(y="y")

    sa_line = alt.Chart(
        pd.DataFrame({"y": [SA_PM10]})
    ).mark_rule(
        color="orange",
        size=2
    ).encode(y="y")

    st.altair_chart(
        (bars + who_line + sa_line).properties(height=400),
        use_container_width=True
    )

    st.caption(
        f"🔴 WHO ({WHO_PM10} µg/m³) | 🟠 SA NAAQS ({SA_PM10} µg/m³)"
    )

    # ---------------------------
    # Monthly Patterns
    # ---------------------------
    st.subheader("Monthly Patterns")

    monthly_mean = df.groupby("month", as_index=False)["PM10"].mean()

    m1, m2 = st.columns(2)

    with m1:
        bar_month = alt.Chart(monthly_mean).mark_bar(color="#50C878").encode(
            x=alt.X("month:N", sort=MONTH_ORDER),
            y=alt.Y("PM10:Q"),
            tooltip=["month", alt.Tooltip("PM10:Q", format=".2f")]
        ).properties(height=350)

        st.altair_chart(bar_month, use_container_width=True)

    with m2:
        line_month = alt.Chart(monthly_mean).mark_line(
            point=True, color="#50C878"
        ).encode(
            x=alt.X("month:N", sort=MONTH_ORDER),
            y=alt.Y("PM10:Q"),
            tooltip=["month", alt.Tooltip("PM10:Q", format=".2f")]
        ).properties(height=350)

        st.altair_chart(line_month, use_container_width=True)

    # ---------------------------
    # Seasonal Boxplots
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
        tooltip=[
            "Season",
            alt.Tooltip("PM10:Q", format=".2f")
        ]
    ).properties(height=400)

    st.altair_chart(boxplot, use_container_width=True)

else:
    st.info("Please upload your PM10 CSV file to begin analysis.")
    
# Add a contact section
st.header("Contact Information")
email = "sibisizoz99@gmail.com"
st.write(f"You can reach {name} at {email}.")
