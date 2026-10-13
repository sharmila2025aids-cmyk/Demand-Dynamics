import streamlit as st

st.title("Demand Dynamics")
st.subheader("AI-Based Skill Gap Analyzer")

st.write("Find your skill gaps and training needs.")

student_name = st.text_input("Enter your name")

skills = ["Python", "SQL", "Machine Learning", "Data Analysis", "Communication"]

selected_skills = st.multiselect("Select the skills you know", skills)

st.write("Your name:", student_name)
st.write("Skills you know:", selected_skills)

missing_skills = [skill for skill in skills if skill not in selected_skills]

st.subheader("Skills to improve")
st.write(missing_skills)

st.info("Recommended training: " + ", ".join(missing_skills))
