import streamlit as st

st.set_page_config(page_title="Demand Dynamics", page_icon="📊")

st.title("📊 Demand Dynamics")
st.subheader("AI-Based Skill Gap Analyzer")

st.write("Identify skill gaps and find the training students need.")

st.header("Student Skill Assessment")

student_name = st.text_input("Enter your name")

skills = [
"Python",
"SQL",
"Machine Learning",
"Data Analysis",
"Communication"
]

selected_skills = st.multiselect(
"Select the skills you know",
skills
)

if st.button("Analyze Skill Gap"):
if student_name and selected_skills:
st.success("Assessment completed for " + student_name)

    missing_skills = [
        skill for skill in skills
        if skill not in selected_skills
    ]

    st.subheader("Your Skill Gap")
    st.write("Skills you know:", ", ".join(selected_skills))
    st.write("Skills to improve:", ", ".join(missing_skills))

    if missing_skills:
        st.info(
            "Recommended training: "
            + ", ".join(missing_skills)
        )
    else:
        st.success("You selected all the listed skills!")
else:
    st.warning("Enter your name and select at least one skill.")
