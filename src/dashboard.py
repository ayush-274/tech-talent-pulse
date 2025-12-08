import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Page Configuration
st.set_page_config(page_title="Tech Talent Pulse", layout="wide")

st.title("📈 Tech Talent Pulse")
st.markdown("Tracking the most in-demand skills for **Remote Programming Jobs**.")

# 1. Load Data
@st.cache_data
def load_data():
    # Load the enriched job list
    try:
        df_jobs = pd.read_csv("data/processed/jobs_enriched.csv")
    except FileNotFoundError:
        st.error("❌ Job data not found. Run the scraper first!")
        return None, None
    
    # Load the latest trend file
    # We look for the most recent file in data/processed that starts with 'skills_trend_'
    processed_dir = "data/processed"
    trend_files = [f for f in os.listdir(processed_dir) if f.startswith("skills_trend_")]
    
    if trend_files:
        # Sort to get the latest one
        latest_file = sorted(trend_files)[-1]
        df_trends = pd.read_csv(os.path.join(processed_dir, latest_file))
        data_date = latest_file.replace("skills_trend_", "").replace(".csv", "")
    else:
        st.warning("⚠️ No trend data found.")
        df_trends = pd.DataFrame()
        data_date = "N/A"
        
    return df_jobs, df_trends, data_date

df_jobs, df_trends, data_date = load_data()

if df_jobs is not None:
    
    # --- METRICS SECTION ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs Tracked", len(df_jobs))
    col2.metric("Latest Update", data_date)
    top_skill = df_trends.iloc[0]['skill'].title() if not df_trends.empty else "N/A"
    col3.metric("Top Skill", top_skill)

    st.divider()

    # --- VISUALIZATION SECTION ---
    col_chart, col_raw = st.columns([2, 1])

    with col_chart:
        st.subheader("🔥 Top 15 In-Demand Skills")
        if not df_trends.empty:
            # Bar Chart using Plotly
            fig = px.bar(
                df_trends.head(15), 
                x='count', 
                y='skill', 
                orientation='h',
                title="Skill Frequency in Recent Job Postings",
                labels={'count': 'Mentions', 'skill': 'Technology'},
                color='count',
                color_continuous_scale='viridis'
            )
            fig.update_layout(yaxis=dict(autorange="reversed")) # Top skill at top
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trend data available to plot.")

    with col_raw:
        st.subheader("📋 Latest Jobs")
        # Simple Search Filter
        search_term = st.text_input("Search by Skill (e.g., Python)", "")
        
        display_cols = ['title', 'company', 'published_date', 'url']
        
        if search_term:
            # Filter logic: Check if search term is in the 'skills_found' string or title
            filtered_df = df_jobs[
                df_jobs['title'].str.contains(search_term, case=False) | 
                df_jobs['skills_found'].str.contains(search_term, case=False)
            ]
            st.dataframe(filtered_df[display_cols], hide_index=True)
        else:
            st.dataframe(df_jobs[display_cols], hide_index=True)

    # --- INSIGHTS SECTION ---
    st.divider()
    st.markdown("### 💡 Insights")
    st.info(f"""
    The data suggests that **{top_skill}** is currently the dominant skill in the remote market. 
    This dashboard updates daily via a GitHub Actions pipeline.
    """)