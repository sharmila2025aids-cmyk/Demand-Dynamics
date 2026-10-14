import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. PYCHARM CONSOLE DATA ANALYSIS ENGINE
# ==========================================
def run_console_analysis(df_skills):
    print("\n" + "="*60)
    print("      PYCHARM DATA LOG: YEAR-OVER-YEAR METRIC TRENDS")
    print("="*60)
    
    skills_list = ['Python', 'Machine Learning', 'SQL', 'NLP', 'GenAI', 'RAG']
    
    print("\n🔹 TREND ANALYSIS: YEAR 2024 TO 2025")
    print("-" * 50)
    df_24 = df_skills[df_skills['Year'] == 2024].set_index('Skill')
    df_25 = df_skills[df_skills['Year'] == 2025].set_index('Skill')
    
    for skill in skills_list:
        v24 = df_24.loc[skill, 'Job_Count']
        v25 = df_25.loc[skill, 'Job_Count']
        diff = v25 - v24
        status = "INCREASED" if diff >= 0 else "DECREASED"
        print(f"Skill: {skill:<18} | 2024: {v24:<4} -> 2025: {v25:<4} | Count: {diff:>+4} ({status})")
        
    print("\n🔹 TREND ANALYSIS: YEAR 2025 TO 2026")
    print("-" * 50)
    df_26 = df_skills[df_skills['Year'] == 2026].set_index('Skill')
    
    for skill in skills_list:
        v25 = df_25.loc[skill, 'Job_Count']
        v26 = df_26.loc[skill, 'Job_Count']
        diff = v26 - v25
        status = "INCREASED" if diff >= 0 else "DECREASED"
        print(f"Skill: {skill:<18} | 2025: {v25:<4} -> 2026: {v26:<4} | Count: {diff:>+4} ({status})")
    print("="*60 + "\n")

try:
    skills_data_raw = pd.read_csv("skill extracting.csv")
    run_console_analysis(skills_data_raw)
except Exception as e:
    print(f"Console Logger Warning: {e}")


# ==========================================
# 2. STREAMLIT INTERACTIVE LIVE DASHBOARD
# ==========================================
st.set_page_config(page_title="Demand Dynamics Dashboard", layout="wide")

st.title("TEAM DEMAND DYNAMICS | INNOVATE X")
st.subheader("Department of Artificial Intelligence and Data Science")
st.markdown("---")

@st.cache_data
def load_data():
    try:
        skills_df = pd.read_csv("skill extracting.csv")
        jobs_df = pd.read_csv("job postings.csv")
        return skills_df, jobs_df
    except FileNotFoundError:
        st.error("Missing raw data files inside your project directory.")
        return None, None

df_skills, df_jobs = load_data()

if df_skills is not None and df_jobs is not None:
    st.header("🚨 IDEA 01: SKILL SHOCK RADAR")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Target Focus Growth Highlights")
        df_2024 = df_skills[df_skills['Year'] == 2024].set_index('Skill')
        df_2026 = df_skills[df_skills['Year'] == 2026].set_index('Skill')
        
        for skill in ['GenAI', 'RAG']:
            c_24 = df_2024.loc[skill, 'Job_Count']
            c_26 = df_2026.loc[skill, 'Job_Count']
            growth = ((c_26 - c_24) / c_24) * 100
            st.metric(label=f"Emerging Skill: {skill}", value=f"{c_26} Jobs", delta=f"+{growth:.1f}% Overall Growth")

    with col2:
        fig, ax = plt.subplots(figsize=(8, 4.2))
        
        pivot_count = df_skills.pivot(index='Skill', columns='Year', values='Job_Count')
        pivot_count = pivot_count.reindex(['Python', 'Machine Learning', 'SQL', 'NLP', 'GenAI', 'RAG'])
        
        pivot_count.plot(kind='bar', ax=ax, width=0.8, edgecolor='black', color=['#aec7e8', '#1f77b4', '#0d3b66'])
        
        ax.set_title("Year-over-Year Job Count Tracking Matrix (2024 - 2026)", fontsize=11, fontweight='bold')
        ax.set_ylabel("Total Job Postings Available")
        ax.set_xlabel("Core Technology Spectrum")
        ax.set_ylim(0, 1100)
        ax.grid(axis='y', linestyle="--", alpha=0.4)
        ax.legend(title="Timeline Block")
        plt.xticks(rotation=0)
        
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.text(p.get_x() + p.get_width()/2., height + 15, f'{int(height)}', ha="center", fontsize=7.5)
                
        st.pyplot(fig)

    st.markdown("---")
    st.header("🤖 IDEA 02: WORKFORCE GAP SIMULATOR")
    
    genai_demand_2026 = float(df_2026.loc['GenAI', 'Market_Demand_Percentage'])
    workforce_readiness = 45.0  
    skill_gap = genai_demand_2026 - workforce_readiness
    
    m1, m2, m3 = st.columns(3)
    m1.metric("INDUSTRY DEMAND", f"{genai_demand_2026}%")
    m2.metric("WORKFORCE READINESS", f"{workforce_readiness}%")
    m3.metric("TOTAL SKILL GAP", f"{skill_gap}%", delta="-Action Required", delta_color="inverse")

    st.subheader("System Outputs")
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.error("🚨 PRIORITY LEVEL: HIGH")
    with status_col2:
        st.info("🛠️ RECOMMENDED ACTION: GenAI + RAG Training Framework Needed")

    st.markdown("---")
    st.header("🔍 SOP DATA PIPELINE: JOB EXTRACTION VIA JOB MARKET")
    st.write("Live filtered extractions targeting Coimbatore matching GenAI & RAG requirements:")
    
    filtered_jobs = df_jobs[(df_jobs['Location'] == 'Coimbatore') & 
                            (df_jobs['Required Skills'].str.contains('GenAI|RAG', na=False))]
    st.dataframe(filtered_jobs[['Job Title', 'Company', 'Platform', 'Required Skills']], width="stretch")
# ==========================================
# 3. AUTOMATIC WEB LINK GENERATOR FOR JURY
# ==========================================
if __name__ == "__main__":
    print("\n" + "•" * 60)
    print(" 🚀 DATA PROCESSING COMPLETE! EXPERT WEB SYSTEM IS READY.")
    print(" 🔗 CLICK THE LINK BELOW TO OPEN THE LIVE PRESENTATION DASHBOARD:")
    print("    👉 http://localhost:8501 👈")
    print("" * 60 + "\n")
