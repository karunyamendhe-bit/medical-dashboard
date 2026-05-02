import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="🏥 Medical Imaging Dashboard", layout="wide")

@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1200
    dates = pd.date_range('2020-01-01', periods=n, freq='D')
    data = {
        'Patient_ID': [f'P{i:04d}' for i in range(n)],
        'Study_ID': [f'S{i:06d}' for i in range(n)],
        'Modality': np.random.choice(['CT', 'MRI', 'X-Ray', 'Ultrasound', 'PET'], n),
        'Hospital': np.random.choice(['City General', 'University Hospital', 'Central Medical', 'Eastside Clinic'], n),
        'Image_Size_MB': np.random.uniform(5, 150, n).round(2),
        'Missing_Metadata_Flag': np.random.choice(['Yes', 'No'], n, p=[0.15, 0.85]),
        'Study_Date': dates,
        'Age': np.random.randint(18, 90, n),
        'Gender': np.random.choice(['M', 'F'], n)
    }
    return pd.DataFrame(data)

df = load_data()

st.title("🏥 Medical Imaging Dashboard")
st.markdown("**Interactive analytics for medical imaging data**")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Total Images", f"{len(df):,}")
col2.metric("👥 Patients", df['Patient_ID'].nunique())
col3.metric("📏 Avg Size", f"{df['Image_Size_MB'].mean():.1f}MB")
col4.metric("⚠️ Missing Data", f"{(df['Missing_Metadata_Flag']=='Yes').mean()*100:.1f}%")

# Sidebar filters
st.sidebar.header("🔍 Filters")
modality = st.sidebar.multiselect("Modality", df['Modality'].unique())
hospital = st.sidebar.multiselect("Hospital", df['Hospital'].unique())
age_range = st.sidebar.slider("Age", 18, 90, (18, 90))

filtered_df = df[
    (df['Modality'].isin(modality)) &
    (df['Hospital'].isin(hospital)) &
    (df['Age'].between(*age_range))
]

# Charts
col1, col2 = st.columns(2)
fig1 = px.pie(filtered_df, names='Modality', title="Modality Distribution", hole=0.4)
col1.plotly_chart(fig1, use_container_width=True)

trend = filtered_df.groupby(filtered_df['Study_Date'].dt.to_period('M')).size()
fig2 = px.line(x=trend.index.astype(str), y=trend.values, title="Monthly Trends")
col2.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
px.bar(filtered_df, x='Hospital', title="Hospital Usage").update_layout(height=400).show()
px.histogram(filtered_df, x='Age', color='Gender', title="Age Distribution").update_layout(height=400).show()
