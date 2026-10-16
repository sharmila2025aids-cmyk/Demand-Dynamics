import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# =====================================
# DEMAND DYNAMICS - INNOVATE X
# =====================================

st.set_page_config(
    page_title="Demand Dynamics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 DEMAND DYNAMICS | INNOVATE X")
st.subheader("AI & Data Science Skill Intelligence Dashboard")

st.markdown(
    "Predict future skills, analyse student skill gaps "
    "and recommend relevant training."
)

# =====================================
# 1. LOAD CSV FILES
# =====================================

SKILL_FILE = "demand_dynamics_extracted_skills_summary.csv"
JOBS_FILE = "demand_dynamics_3years_3000.csv"


@st.cache_data
def load_csv(filename):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return None


skills_raw = load_csv(SKILL_FILE)
jobs_df = load_csv(JOBS_FILE)


# =====================================
# 2. PREPARE SKILL DATA
# =====================================

def prepare_skills(df):
    if df is None:
        return None

    df = df.copy()

    # Standardise column names
    df.columns = [
        str(c).strip().replace(" ", "_")
        for c in df.columns
    ]

    # Detect common column-name variations
    aliases = {
        "Year": ["Year", "year", "Date_Year"],
        "Skill": ["Skill", "skill", "Skills", "Technology"],
        "Job_Count": [
            "Job_Count", "job_count", "Jobs",
            "Count", "Frequency", "Demand_Count"
        ],
        "Market_Demand_Percentage": [
            "Market_Demand_Percentage",
            "Demand_Percentage",
            "Market_Demand",
            "Percentage"
        ]
    }

    rename = {}

    for standard, choices in aliases.items():
        for choice in choices:
            if choice in df.columns:
                rename[choice] = standard
                break

    df = df.rename(columns=rename)

    required = ["Year", "Skill", "Job_Count"]

    if not all(c in df.columns for c in required):
        return None

    df["Year"] = pd.to_numeric(
        df["Year"], errors="coerce"
    )

    df["Job_Count"] = pd.to_numeric(
        df["Job_Count"], errors="coerce"
    )

    df["Skill"] = df["Skill"].astype(str).str.strip()

    df = df.dropna(
        subset=["Year", "Skill", "Job_Count"]
    )

    df["Year"] = df["Year"].astype(int)

    # Combine duplicate skill-year records
    df = df.groupby(
        ["Year", "Skill"], as_index=False
    )["Job_Count"].sum()

    # Calculate demand percentage from available counts
    yearly_total = df.groupby("Year")[
        "Job_Count"
    ].transform("sum")

    df["Market_Demand_Percentage"] = (
        df["Job_Count"] / yearly_total * 100
    ).fillna(0)

    return df


df = prepare_skills(skills_raw)

if df is None:
    st.error(
        "Skill CSV columns could not be identified. "
        "Expected columns: Year, Skill, Job_Count."
    )

    if skills_raw is not None:
        st.write("Your actual CSV columns:")
        st.write(list(skills_raw.columns))

    st.stop()


# =====================================
# 3. SKILL SELECTION
# =====================================

st.header("🎯 1. Skill Demand Explorer")

available_skills = sorted(df["Skill"].unique())

selected_skills = st.multiselect(
    "Select skills to analyse",
    available_skills,
    default=available_skills[:min(4, len(available_skills))]
)

selected_df = df[df["Skill"].isin(selected_skills)]

if not selected_df.empty:
    pivot = selected_df.pivot_table(
        index="Year",
        columns="Skill",
        values="Job_Count",
        aggfunc="sum"
    ).sort_index()

    st.line_chart(pivot)

    st.caption(
        "The graph updates when you change the selected skills."
    )

    st.dataframe(
        selected_df.sort_values(["Year", "Skill"]),
        use_container_width=True
    )
else:
    st.info("Select at least one skill to display the graph.")


# =====================================
# 4. YEAR-OVER-YEAR ANALYSIS
# =====================================

st.markdown("---")
st.header("📊 2. Year-over-Year Demand Analysis")

years = sorted(df["Year"].unique())

if len(years) >= 2:
    first_year = years[-2]
    latest_year = years[-1]

    old = df[df["Year"] == first_year].set_index("Skill")
    new = df[df["Year"] == latest_year].set_index("Skill")

    common = old.index.intersection(new.index)

    if len(common) > 0:
        trend = pd.DataFrame({
            "Skill": common,
            f"{first_year} Jobs": old.loc[
                common, "Job_Count"
            ].values,
            f"{latest_year} Jobs": new.loc[
                common, "Job_Count"
            ].values
        })

        trend["Change"] = (
            trend[f"{latest_year} Jobs"]
            - trend[f"{first_year} Jobs"]
        )

        trend["Growth_Percentage"] = (
            trend["Change"]
            / trend[f"{first_year} Jobs"].replace(0, float("nan"))
            * 100
        ).round(2)

        st.dataframe(
            trend.sort_values(
                "Growth_Percentage",
                ascending=False
            ),
            use_container_width=True
        )
else:
    st.info("At least two different years are needed for trend analysis.")


# =====================================
# 5. 2027 DEMAND FORECAST
# =====================================

st.markdown("---")
st.header("🔮 3. Future Skill Demand Prediction")

st.warning(
    "2027 values are model estimates based on historical data, "
    "not confirmed future job postings."
)

forecast_rows = []

for skill in available_skills:
    data = df[df["Skill"] == skill].sort_values("Year")

    # Require at least two different years
    if data["Year"].nunique() < 2:
        continue

    x = data["Year"].to_numpy(dtype=float)
    y = data["Job_Count"].to_numpy(dtype=float)

    # Linear trend prediction
    slope, intercept = __import__("numpy").polyfit(x, y, 1)

    predicted = max(0, slope * 2027 + intercept)

    forecast_rows.append({
        "Skill": skill,
        "Latest_Year": int(x.max()),
        "Latest_Job_Count": int(y[-1]),
        "Predicted_2027_Jobs": round(predicted),
        "Estimated_Change": round(predicted - y[-1])
    })

if forecast_rows:
    forecast_df = pd.DataFrame(forecast_rows)

    st.dataframe(
        forecast_df.sort_values(
            "Predicted_2027_Jobs",
            ascending=False
        ),
        use_container_width=True
    )

    forecast_chart = forecast_df.set_index("Skill")[
        ["Latest_Job_Count", "Predicted_2027_Jobs"]
    ]

    st.bar_chart(forecast_chart)

    st.caption(
        "Forecast uses a simple linear trend. "
        "With only three years of data, predictions may be uncertain."
    )
else:
    st.info(
        "Each skill needs data from at least two different years "
        "to generate a forecast."
    )


# =====================================
# 6. STUDENT SKILL GAP SIMULATOR
# =====================================

st.markdown("---")
st.header("🎓 4. Student Skill Gap Simulator")

st.write(
    "Select a skill and enter the student's current proficiency. "
    "The dashboard compares it with a target level."
)

gap_skill = st.selectbox(
    "Choose a skill for gap analysis",
    available_skills
)

student_level = st.slider(
    "Student proficiency (%)",
    min_value=0,
    max_value=100,
    value=45
)

target_level = st.slider(
    "Target proficiency (%)",
    min_value=0,
    max_value=100,
    value=80
)

skill_gap = max(0, target_level - student_level)

c1, c2, c3 = st.columns(3)

c1.metric("Student Level", f"{student_level}%")
c2.metric("Target Level", f"{target_level}%")
c3.metric("Skill Gap", f"{skill_gap}%")

if skill_gap >= 30:
    st.error("Priority: HIGH — intensive training recommended.")
elif skill_gap >= 15:
    st.warning("Priority: MEDIUM — focused training recommended.")
elif skill_gap > 0:
    st.info("Priority: LOW — practise and improve the skill.")
else:
    st.success("Target achieved! Continue practising.")

st.progress(skill_gap / 100)


# =====================================
# 7. TRAINING RECOMMENDATIONS
# =====================================

st.markdown("---")
st.header("🤖 5. Training & Course Recommendations")

recommendations = {
    "Python": [
        "Python Fundamentals",
        "Data Structures and Problem Solving",
        "Python Projects"
    ],
    "Machine Learning": [
        "Machine Learning Fundamentals",
        "Model Evaluation and Feature Engineering",
        "Hands-on ML Projects"
    ],
    "SQL": [
        "SQL Fundamentals",
        "Joins and Subqueries",
        "Database Query Practice"
    ],
    "NLP": [
        "Natural Language Processing Basics",
        "Text Processing and Embeddings",
        "NLP Projects"
    ],
    "GenAI": [
        "Generative AI Fundamentals",
        "Prompt Engineering",
        "LLM Application Development"
    ],
    "RAG": [
        "Retrieval-Augmented Generation Fundamentals",
        "Vector Databases and Embeddings",
        "Build a RAG Application"
    ]
}

courses = recommendations.get(
    gap_skill,
    [
        f"{gap_skill} Fundamentals",
        f"{gap_skill} Practical Training",
        f"{gap_skill} Project-Based Learning"
    ]
)

st.subheader(f"Recommended learning path: {gap_skill}")

if skill_gap == 0:
    st.success(
        "Your target has been achieved. "
        "Try an advanced course or a real-world project."
    )
else:
    for i, course in enumerate(courses, start=1):
        st.write(f"{i}. {course}")

st.write(
    "Suggested learning format: theory, guided practice, "
    "mini-project and final assessment."
)


# =====================================
# 8. JOB MARKET DATA
# =====================================

st.markdown("---")
st.header("💼 6. Job Market Data Explorer")

if jobs_df is not None:
    st.write("Job records loaded from your CSV file.")

    search = st.text_input(
        "Search job data",
        placeholder="Enter a skill, role or keyword"
    )

    if search:
        mask = jobs_df.astype(str).apply(
            lambda column: column.str.contains(
                search, case=False, na=False
            )
        ).any(axis=1)

        display_jobs = jobs_df[mask]
    else:
        display_jobs = jobs_df

    st.metric("Matching Job Records", len(display_jobs))

    st.dataframe(
        display_jobs,
        use_container_width=True
    )

    st.download_button(
        "Download filtered job data",
        data=display_jobs.to_csv(index=False).encode("utf-8"),
        file_name="filtered_job_data.csv",
        mime="text/csv"
    )
else:
    st.warning(
        f"Could not find {JOBS_FILE}. "
        "Check the exact file name in your GitHub repository."
    )


# =====================================
# 9. PROJECT NOTES
# =====================================

st.markdown("---")
st.caption(
    "DEMAND DYNAMICS | INNOVATE X | AI & Data Science"
)
st.caption(
    "Forecasts are estimates. Training recommendations are "
    "rule-based suggestions, not personalised AI-generated advice."
    )
