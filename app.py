import streamlit as st
import pandas as pd

st.title("Demand Dynamics")
st.subheader("AI-Based Skill Gap Analyzer")

df = pd.read_csv("demand_dynamics_extracted_skills_summary.csv")

st.subheader("Job Market Skills Summary")
st.dataframe(df)

st.subheader("Student Skill Assessment")

student_name = st.text_input("Enter your name")

skills = ["Python", "SQL", "Machine Learning", "Data Analysis", "Communication"]

selected_skills = st.multiselect("Select the skills you know", skills)

missing_skills = [s for s in skills if s not in selected_skills]

st.write("Skills you know:", selected_skills)
st.write("Skills to improve:", missing_skills)
st.write("Recommended training:", ", ".join(missing_skills))
