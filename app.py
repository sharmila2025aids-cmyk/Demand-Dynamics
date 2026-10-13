import streamlit as st
import pandas as pd
import os

st.title("Demand Dynamics")
st.subheader("AI-Based Skill Gap Analyzer")

st.write("Analyze job skills and student training needs.")

file_name = "demand_dynamics_extracted_skills_summary.csv"

if os.path.exists(file_name):
df = pd.read_csv(file_name)
else:
df = pd.DataFrame()

st.subheader("Job Market Skills Summary")
st.dataframe(df)

st.subheader("Student Skill Assessment")
student_name = st.text_input("Enter your name")

skills = ["Python", "SQL", "Machine Learning", "Data Analysis", "Communication"]
selected_skills = st.multiselect("Select the skills you know", skills)

missing_skills = [s for s in skills if s not in selected_skills]

st.write("Skills you know:", selected_skills)
st.write("Skills to improve:", missing_skills)
