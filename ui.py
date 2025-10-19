import streamlit as st
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
import LLM_comparision_database as llm
import db_utils
from mysql.connector import Error
import plotly.graph_objects as go
import plotly.express as px

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Exchange Program Matcher",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling with lighter colors
st.markdown("""
<style>
    /* Main background gradient - Light blue gradient */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 50%, #7dd3fc 100%);
    }
    
    /* Container styling */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Header styling - Dark text for visibility */
    .main-header {
        color: #0f172a;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Sub-header - Dark for visibility */
    .sub-header {
        text-align: center;
        color: #334155;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    /* Button styling - Orange/coral for contrast */
    .stButton > button {
        background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
        color: white;
        border: none;
        margin: 0 auto;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
        width: auto;            /* was 100% */
        min-width: 350px;       /* keep a nice min size */
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(251, 146, 60, 0.3);
    }   

    .stButton {
        display: flex;           /* center the button within its Streamlit wrapper */
        justify-content: center;
        align-items: center;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(251, 146, 60, 0.4);
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 2px dashed rgba(14, 165, 233, 0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Base metric card styling */
    .metric-card {
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Individual metric card colors */
    .metric-card-pink {
        background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
        border-left: 4px solid #ec4899;
    }
    
    .metric-card-green {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border-left: 4px solid #22c55e;
    }
    
    .metric-card-purple {
        background: linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 100%);
        border-left: 4px solid #a855f7;
    }
    
    .metric-card-yellow {
        background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%);
        border-left: 4px solid #eab308;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
    }
    
    .metric-label {
        color: #374151;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
    }
    
    /* Make all text darker for better visibility */
    p, span, div {
        color: #1e293b;
    }
    
    /* Expander styling - UPDATED with different colors */
    .streamlit-expanderHeader {
        background-color: #e0e7ff !important;  /* Light purple/indigo background */
        border: 1px solid #a5b4fc !important;  /* Indigo border */
        border-radius: 8px !important;
        color: #312e81 !important;  /* Dark indigo text */
        font-weight: 500 !important;
    }
    
    
    /* Expanded content area - DIFFERENT COLOR */
    div[data-testid="stExpander"] div[role="region"] {
        background-color: #fef3c7 !important;  /* Light yellow/amber background */
        border: 1px solid #fde68a !important;  /* Yellow border */
        border-radius: 0 0 8px 8px !important;
        padding: 1rem !important;
        margin-top: -1px !important;
    }
    
    /* Style the dataframe inside expander */
    div[data-testid="stExpander"] .stDataFrame {
        background-color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'schools_df' not in st.session_state:
    st.session_state.schools_df = None
if 'students_df' not in st.session_state:
    st.session_state.students_df = None
if 'matches' not in st.session_state:
    st.session_state.matches = None

# Function: Transfer CSVs to MySQL with prepared statements
def transfer_to_mysql(schools_df: pd.DataFrame, students_df: pd.DataFrame):
    """
    Transfer data from DataFrames to MySQL tables using insert functions.
    
    Args:
        schools_df (pd.DataFrame): DataFrame containing school data
        students_df (pd.DataFrame): DataFrame containing student CV data
    
    Returns:
        bool: True if transfer is successful, False otherwise
    """
    conn = db_utils.get_connection()  # Reuse get_connection from db_utils
    if not conn:
        print("Failed to establish database connection")
        return False
    cursor= None
    try:
        cursor = conn.cursor()

        db_utils.clear_database_tables()
            
        # Create school_req table (aligned with previous schema)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS school_req (
                id INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
                gpa_req FLOAT NOT NULL,
                quota INT NOT NULL,
                course_req text,
                extra_req TEXT
            )
        """)
        # Create student_cv table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_cv (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cgpa FLOAT NOT NULL,
                major VARCHAR(100) NOT NULL,
                language_certificate TEXT,
                courses_studied TEXT,
                exchange_1 VARCHAR(100),
                exchange_description_1 TEXT,
                exchange_2 VARCHAR(100),
                exchange_description_2 TEXT,
                eca_project_experience_1 VARCHAR(100),
                eca_project_description_1 TEXT,
                eca_project_experience_2 VARCHAR(100),
                eca_project_description_2 TEXT,
                eca_project_experience_3 VARCHAR(100),
                eca_project_description_3 TEXT,
                recommendation_letter TEXT,
                scholarships_awards TEXT,
                hobbies TEXT,
                student_preference text not null,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

        # Insert schools
        for _, row in schools_df.iterrows():
            success = db_utils.insert_school(
                gpa_req=float(row['gpa_req']) if not pd.isna(row.get('gpa_req')) else 0.0,
                quota=int(row['quota']) if not pd.isna(row.get('quota')) else 0,
                course_req = None if pd.isna(row.get('course_req')) else str(row['course_req']),
                extra_req = None if pd.isna(row.get('extra_req')) else str(row['extra_req'])
            )
            if not success:
                print(f"Failed to insert school: {row}")
                return False

        # Insert students
        for _, row in students_df.iterrows():
            cgpa = float(row['cgpa']) if not pd.isna(row.get('cgpa')) else 0.0
            if not (0.0 <= cgpa <= 4.3):
                raise ValueError(f"Invalid cgpa {cgpa}")
            major = str(row['major']) if not pd.isna(row.get('major')) else 'Unknown'
            student_preference = str(row['student_preference']) if not pd.isna(row.get('student_preference')) else '0'
            success = db_utils.insert_student(
                cgpa=cgpa,
                major=major,
                language_certificate=None if pd.isna(row.get('language_certificate')) else str(row['language_certificate']),
                courses_studied=None if pd.isna(row.get('courses_studied')) else str(row['courses_studied']),
                exchange_1=None if pd.isna(row.get('exchange_1')) else str(row['exchange_1']),
                exchange_description_1=None if pd.isna(row.get('exchange_description_1')) else str(row['exchange_description_1']),
                exchange_2=None if pd.isna(row.get('exchange_2')) else str(row['exchange_2']),
                exchange_description_2=None if pd.isna(row.get('exchange_description_2')) else str(row['exchange_description_2']),
                eca_project_experience_1=None if pd.isna(row.get('eca_project_experience_1')) else str(row['eca_project_experience_1']),
                eca_project_description_1=None if pd.isna(row.get('eca_project_description_1')) else str(row['eca_project_description_1']),
                eca_project_experience_2=None if pd.isna(row.get('eca_project_experience_2')) else str(row['eca_project_experience_2']),
                eca_project_description_2=None if pd.isna(row.get('eca_project_description_2')) else str(row['eca_project_description_2']),
                eca_project_experience_3=None if pd.isna(row.get('eca_project_experience_3')) else str(row['eca_project_experience_3']),
                eca_project_description_3=None if pd.isna(row.get('eca_project_description_3')) else str(row['eca_project_description_3']),
                recommendation_letter=None if pd.isna(row.get('recommendation_letter')) else str(row['recommendation_letter']),
                scholarships_awards=None if pd.isna(row.get('scholarships_awards')) else str(row['scholarships_awards']),
                hobbies=None if pd.isna(row.get('hobbies')) else str(row['hobbies']),
                student_preference=student_preference,
            )
            if not success:
                print(f"Failed to insert student with CGPA: {row.get('cgpa')}")
                return False

        return True
    except Error as e:
        print(f"Error during transfer: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# Start of main container with white background
with st.container():
    # App title - Dark text for visibility
    st.markdown('<h1 class="main-header">🎓 International Exchange Program Matcher</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Student-School Matching System</p>', unsafe_allow_html=True)

    # Statistics row with colored boxes
    if st.session_state.schools_df is not None and st.session_state.students_df is not None:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card metric-card-pink">
                <div class="metric-icon">🏫</div>
                <div class="metric-value">{len(st.session_state.schools_df)}</div>
                <div class="metric-label">Schools Available</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card metric-card-green">
                <div class="metric-icon">👥</div>
                <div class="metric-value">{len(st.session_state.students_df)}</div>
                <div class="metric-label">Students Registered</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            total_quota = st.session_state.schools_df['quota'].sum() if 'quota' in st.session_state.schools_df.columns else 0
            st.markdown(f"""
            <div class="metric-card metric-card-purple">
                <div class="metric-icon">📊</div>
                <div class="metric-value">{total_quota}</div>
                <div class="metric-label">Total Positions</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            if "matches" in st.session_state and st.session_state.matches is not None:
                matched_count = len([v for v in st.session_state.matches.values() if v is not None])
                st.markdown(f"""
                <div class="metric-card metric-card-yellow">
                    <div class="metric-icon">✨</div>
                    <div class="metric-value">{matched_count}</div>
                    <div class="metric-label">Matches Made</div>
                        </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card metric-card-yellow">
                    <div class="metric-icon">✨</div>
                    <div class="metric-value">0</div>
                    <div class="metric-label">Matches Made</div>
                </div>
                """, unsafe_allow_html=True)

    # Section: Upload Data - Using st.header instead of markdown to avoid line
    st.header("📤 Upload Data Files")

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.markdown("### 🏫 Schools Data")
            school_file = st.file_uploader("Upload Schools CSV", type="csv", key="school_upload")
            if school_file:
                try:
                    st.session_state.schools_df = pd.read_csv(school_file)
                    st.success(f"✅ Successfully loaded {len(st.session_state.schools_df)} schools")
                    
                    with st.expander("Preview School Data", expanded=False):
                        st.dataframe(
                            st.session_state.schools_df.head(),
                            width='stretch',
                            hide_index=True
                        )
                except Exception as e:
                    st.error(f"❌ Error reading schools CSV: {e}")

    with col2:
        with st.container():
            st.markdown("### 👥 Students Data")
            student_file = st.file_uploader("Upload Students CSV", type="csv", key="student_upload")
            if student_file:
                try:
                    st.session_state.students_df = pd.read_csv(student_file)
                    st.success(f"✅ Successfully loaded {len(st.session_state.students_df)} students")
                    
                    with st.expander("Preview Student Data", expanded=False):
                        st.dataframe(
                            st.session_state.students_df.head(),
                            width='stretch',
                            hide_index=True
                        )
                except Exception as e:
                    st.error(f"❌ Error reading students CSV: {e}")

    # Process button - FIXED: Keep columns [1,2,1] but center button in middle column
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Matching Process"):
            if st.session_state.schools_df is not None and st.session_state.students_df is not None:
                try:
                    with st.spinner("Processing data..."):
                        progress = st.progress(0)
                        status_text = st.empty()
                        
                        # Step 1: Transfer to MySQL
                        status_text.text("📊 Transferring data to database...")
                        transfer_to_mysql(st.session_state.schools_df, st.session_state.students_df)
                        progress.progress(30)
                        
                        # Step 2: Run matching algorithm
                        status_text.text("🤖 Running AI matching algorithm...")
                        progress.progress(60)
                        matches = llm.main()
                        """
                        # Step 3: Clear database tables for privacy
                        status_text.text("🗑️ Clearing database for privacy...")
                        clear_success = db_utils.clear_database_tables()
                        if not clear_success:
                            st.warning("⚠️ Matching completed, but failed to clear database tables")
                        """
                        progress.progress(100)
                        status_text.empty()
                        st.session_state.matches = matches
                        
                        st.success("✨ Matching process completed successfully!")
                        st.balloons()
                        
                        # Force page reload to update metrics
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Processing failed: {e}")
            else:
                st.warning("⚠️ Please upload both school and student CSV files before processing.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Display results
    if st.session_state.matches:
        st.header("📊 Matching Results")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Match List", "📈 Analytics", "💾 Export"])
        
        with tab1:
            matches_df = pd.DataFrame([
                {"Student ID": student, "School ID": str(school), "Status": "Matched"}
                for student, school in st.session_state.matches.items() if school is not None
            ])
    
            unmatched_df = pd.DataFrame([
                {"Student ID": student, "School ID": "N/A", "Status": "Unmatched"}
                for student, school in st.session_state.matches.items() if school is None
            ])
    
            # Sort both DataFrames by Student ID before concatenating
            if not matches_df.empty:
                matches_df = matches_df.sort_values("Student ID").reset_index(drop=True)
            if not unmatched_df.empty:
                unmatched_df = unmatched_df.sort_values("Student ID").reset_index(drop=True)
    
            all_matches_df = pd.concat([matches_df, unmatched_df], ignore_index=True)
    
            st.dataframe(
                all_matches_df,
                width='stretch',
                hide_index=True,
                column_config={
                    "Student ID": st.column_config.NumberColumn("Student ID", format="%d"),
                    "School ID": st.column_config.TextColumn("School ID"),  # TextColumn handles strings
                    "Status": st.column_config.TextColumn("Status")
                }
            )
        
        with tab2:
            # Pie chart for match rate - centered
            matched_count = len([m for m in st.session_state.matches.values() if m is not None])
            unmatched_count = len([m for m in st.session_state.matches.values() if m is None])
            
            # Center the chart
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                fig = go.Figure(data=[go.Pie(
                    labels=['Matched', 'Unmatched'],
                    values=[matched_count, unmatched_count],
                    hole=.3,
                    marker_colors=['#0ea5e9', '#f97316']
                )])
                fig.update_layout(
                    title="Match Distribution",
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("### 💾 Export Results")
            
            col1, col2 = st.columns(2)
            with col1:
                csv = all_matches_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="matching_results.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Generate summary report
                summary = f"""
                MATCHING SUMMARY REPORT
                =======================
                Total Students: {len(st.session_state.students_df)}
                Total Schools: {len(st.session_state.schools_df)}
                Successfully Matched: {matched_count}
                Unmatched Students: {unmatched_count}
                Match Rate: {(matched_count/len(st.session_state.matches)*100):.1f}%
                
                Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                st.download_button(
                    label="📄 Download Summary Report",
                    data=summary,
                    file_name="matching_summary.txt",
                    mime="text/plain"
                )

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #475569; font-size: 0.9rem;">
    <p>Powered by AI | Built with Streamlit | © 2025 Exchange Program Matcher</p>
</div>
""", unsafe_allow_html=True)