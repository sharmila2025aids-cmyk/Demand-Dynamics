import streamlit as st
import pandas as pd
import os

st.title("📊 Demand Dynamics")
st.subheader("AI-Based Skill Gap Analyzer")

st.write("Analyze job skills and identify student training needs.")

file_name = "demand_dynamics_extracted_skills_summary.csv"

if os.path.exists(file_name):
df = pd.read_csv(file_name)
st.success("Skills data loaded successfully!")
st.subheader("Job Market Skills Summary")
st.dataframe(df)
else:
st.warning("CSV file not found. Please upload the skills summary CSV.")

st.subheader("Student Skill Assessment")

student_name = st.text_input("Enter your name")

skills = ["Python", "SQL", "Machine Learning", "Data Analysis", "Communication"]

selected_skills = st.multiselect("Select the skills you know", skills)

st.write("Skills you know:", selected_skills)

missing_skills = [
skill for skill in skills
if skill not in selected_skills
]

st.subheader("Skills to improve")
st.write(missing_skills)

if missing_skills:
st.info("Recommended training: " + ", ".join(missing_skills))
