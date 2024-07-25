import streamlit as st
import pandas as pd
import ast

st.set_page_config(page_title="Course Eligibility and Recommendation System", layout="wide")
st.image("gust.png",width=400)
navigation = st.sidebar.radio("Go To", ["User Guide", "Course Eligibility and Recommendation System","Quick Check"])

# Add custom CSS to the Streamlit app
st.markdown(
    """
    <style>
    /* Ensure the font-family applies to all text elements */
    @font-face {
        font-family: 'Times New Roman';
        src: url('https://fonts.cdnfonts.com/s/15292/Times_New_Roman.woff') format('woff');
    }
    body, div, p, h1, h2, h3, h4, h5, h6, span, td, th, li, label, input, button, select, textarea, .stMarkdown, .stTextInput, .stTextArea, .stRadio, .stCheckbox, .stSelectbox, .stMultiSelect, .stButton, .stSlider, .stDataFrame, .stTable, .stExpander, .stTabs, .stAccordion, .stDownloadButton {
        font-family: 'Times New Roman', serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar Navigation

# Sample DataFrame
def create_sample_data():
    sample_data = pd.DataFrame({
        'Student_ID': [112255,112255, 24856,24856],
        'Semester': [2202,2202, 2302,2302],
        'College': ['CBA','CBA','CAS', 'CAS'],
        'Passed Credits': [30,30,45, 45],
        'Student_Level': [1,1,2, 2],
        'Program': ['Accounting','Accounting','Computer Science', 'Computer Science'],
        'Major': ['Accounting','Accounting','Computer Science', 'Computer Science'],
        'Course_ID': ['ACCT201','MATH111', 'CSC123','ENGL110']
    })
    return sample_data


# Eligibility Functions
def is_eligible(course, taken_courses, prerequisites):
    prereqs = prerequisites.get(course, [])
    return all(prereq in taken_courses for prereq in prereqs)


def is_eligible_special_acc(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "Credits":
        return student_info['Passed Credits'] >= 81
    elif condition == "Credits_College":
        return student_info['Passed Credits'] >= 81 and student_info['College'] == "CBA"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "AND_Senior":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Student_Level'] == 4
    elif condition == "Junior_AND_Major_ACC":
        return student_info['Student_Level'] == 3 and student_info['Major'] == "Accounting"
    elif condition == "AND_Major_ACC":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Accounting"
    elif condition == "Senior":
        return student_info['Student_Level'] == 4
    else:
        return False

def is_eligible_special_ib(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_Major_MG_IB":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior")
    elif condition == "AND_Major_MG_IB_MRKT":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior" or student_info['Major'] == "Marketing")
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "Credits":
        return student_info['Passed Credits'] >= 81
    elif condition == "Credits_College":
        return student_info['Passed Credits'] >= 81 and student_info['College'] == "CBA"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "Senior_And_Major_MG_IB":
        return student_info['Student_Level'] == 4 and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior")
    elif condition == "Junior_And_Major_IB":
        return student_info['Student_Level'] == 3 and student_info['Major'] == "International Business"
    elif condition == "Junior_And_Major_MOB":
        return student_info['Student_Level'] == 3 and student_info['Major'] == "Mgmt & Organizational Behavior"
    elif condition == "Senior":
        return student_info['Student_Level'] == 4
    else:
        return False
    
def is_eligible_special_mob(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_Major_MG_IB":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior")
    elif condition == "AND_Major_MG_IB_MRKT":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior" or student_info['Major'] == "Marketing")
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "Credits":
        return student_info['Passed Credits'] >= 81
    elif condition == "Credits_College":
        return student_info['Passed Credits'] >= 81 and student_info['College'] == "CBA"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "Senior_And_Major_MG_IB":
        return student_info['Student_Level'] == 4 and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior")
    elif condition == "Junior_And_Major_IB":
        return student_info['Student_Level'] == 3 and student_info['Major'] == "International Business"
    elif condition == "Junior_And_Major_MOB":
        return student_info['Student_Level'] == 3 and student_info['Major'] == "Mgmt & Organizational Behavior"
    elif condition == "Senior":
        return student_info['Student_Level'] == 4
    else:
        return False

def is_eligible_special_mis(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")

    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "Credits":
        return student_info['Passed Credits'] >= 81
    elif condition == "Credits_College":
        return student_info['Passed Credits'] >= 81 and student_info['College'] == "CBA"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "Senior_AND_Major_MIS":
        return student_info['Student_Level'] == 4 and student_info['Major'] == "Management Information Systems" 
    elif condition == "Junior_AND_Major_MIS":
        return student_info['Student_Level'] == 3 and student_info['Major'] == "Management Information Systems"
    elif condition == "AND_Major_MIS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Management Information Systems"
    elif condition == "Senior":
        return student_info['Student_Level'] == 4
    else:
        return False
    

def is_eligible_special_mrkt(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")

    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_Major_MG_IB_MRKT":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior" or student_info['Major'] == "Marketing")
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "Credits":
        return student_info['Passed Credits'] >= 81
    elif condition == "Credits_College":
        return student_info['Passed Credits'] >= 81 and student_info['College'] == "CBA"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "Senior_AND_Major_MRKT":
        return student_info['Student_Level'] == 4 and student_info['Major'] == "Marketing"
    elif condition == "Junior_AND_Major_MRKT":
        return student_info['Student_Level'] == 3 and student_info['Major'] == "Marketing"
    elif condition == "AND_Major_MRKT":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Marketing"
    else:
        return False

def is_eligible_special_fin(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "Credits":
        return student_info['Passed Credits'] >= 81
    elif condition == "Credits_College":
        return student_info['Passed Credits'] >= 81 and student_info['College'] == "CBA"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "OR_AND":
        return all(prereq in taken_courses for prereq in prereqs[:2]) or any(prereq in taken_courses for prereq in prereqs[2:])
    elif condition == "Senior_AND_Major_FIN":
        return student_info['Student_Level'] == 4 and student_info['Major'] == "Finance"
    elif condition == "AND_Major_FIN":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Finance"
    elif condition == "AND_Senior":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Student_Level'] == 4
    elif condition == "Senior":
        return student_info['Student_Level'] == 4
    else:
        return False
    

def is_eligible_special_cs(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "AND_College_OR":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "OR_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Computer Science"
    elif condition == "Junior_CS":
        return student_info['Student_Level'] == 3 and student_info['Major'] == "Computer Science"
    elif condition == "Senior_CS":
        return student_info['Student_Level'] == 4 and student_info['Major'] == "Computer Science"
    elif condition == "Any_Two":
        return sum(prereq in taken_courses for prereq in prereqs) >= 2
    elif condition == "OR_AND_College_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    else:
        return False

def is_eligible_special_dmp(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "OR_MCOM":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 54 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM_2":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 60 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_OR_2":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:3]) and any(prereq in taken_courses for prereq in prereqs[3:])
    elif condition == "AND_OR_PR":
        return (all(prereq in taken_courses for prereq in prereqs[:3]) and student_info['Major'] == "Public relations & Advertising") or all(prereq in taken_courses for prereq in prereqs[4:]) 
    elif condition == "AND_OR_Junior_Program":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:]) and student_info['Student_Level'] == 3 and student_info['Program'] == "Mass Communication"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    elif condition == "AND_Junior":
        return student_info['Student_Level'] == 3 and all(prereq in taken_courses for prereq in prereqs)
    elif condition == "Junior_Program":
        return student_info['Student_Level'] == 3 and student_info['Program'] == "Mass Communication"
    elif condition == "Senior_MCOM":
        return student_info['Student_Level'] == 4 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Junior_Program":
        return student_info['Student_Level'] == 3 and all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    else:
        return False

def is_eligible_special_eng_lin(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_UENG":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "English"
    elif condition == "Senior_Lingusitics":
        return student_info['Student_Level'] == 4 and student_info['Major'] == "Eng- Linguistics - Translation"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    else:
        return False
    
def is_eligible_special_eng_edu(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_EDU":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "English Education"
    elif condition == "AND_UENG":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "English"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    elif condition == "Any_Three":
        return sum(prereq in taken_courses for prereq in prereqs) >= 3
    else:
        return False
    
def is_eligible_special_eng_lit(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_UENG":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "English"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    else:
        return False
    
def is_eligible_special_pr(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "OR_MCOM":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 54 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM_2":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 60 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_OR_2":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:3]) and any(prereq in taken_courses for prereq in prereqs[3:])
    elif condition == "AND_OR_PR":
        return (all(prereq in taken_courses for prereq in prereqs[:3]) and student_info['Major'] == "Public relations & Advertising") or all(prereq in taken_courses for prereq in prereqs[4:])
    elif condition == "AND_OR_Junior_Program":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:]) and student_info['Student_Level'] == 3 and student_info['Program'] == "Mass Communication"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    elif condition == "Junior_Program":
        return student_info['Student_Level'] == 3 and student_info['Program'] == "Mass Communication"
    elif condition == "Senior_MCOM":
        return student_info['Student_Level'] == 4 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Junior_Program":
        return student_info['Student_Level'] == 3 and all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    else:
        return False
    
def is_eligible_special_vc(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "OR_MCOM":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 54 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_OR_Junior_Program":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:]) and student_info['Student_Level'] == 3 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM_2":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 60 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_OR_2":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:3]) and any(prereq in taken_courses for prereq in prereqs[3:])
    elif condition == "AND_OR_PR":
        return (all(prereq in taken_courses for prereq in prereqs[:3]) and student_info['Major'] == "Public relations & Advertising") or all(prereq in taken_courses for prereq in prereqs[4:])
    elif condition == "Senior_MCOM":
        return student_info['Student_Level'] == 4 and student_info['Program'] == "Mass Communication"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    elif condition == "Junior_Program":
        return student_info['Student_Level'] == 3 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Junior_Program":
        return student_info['Student_Level'] == 3 and all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    else:
        return False

def is_eligible_special_mgmt(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_College":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['College'] == "COE"
    elif condition == "AND_College_OR":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "AND_OR_2":
        return all(prereq in taken_courses for prereq in prereqs[:2]) and any(prereq in taken_courses for prereq in prereqs[3:])
    else:
        return False

def is_eligible_special_elec(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_College":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['College'] == "COE"
    elif condition == "OR_AND_College_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "AND_College_OR":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "AND_Senior":
        return student_info['Student_Level'] == 4 and all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_OR_2":
        return all(prereq in taken_courses for prereq in prereqs[:2]) and any(prereq in taken_courses for prereq in prereqs[3:])
    elif condition == "AND_3_Courses":
        return all(prereq in taken_courses for prereq in prereqs[:3]) and sum(prereq in taken_courses for prereq in prereqs[3:]) >= 3
    else:
        return False

def is_eligible_special_comp(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_College":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['College'] == "COE"
    elif condition == "OR_AND_College_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "Junior_ECOM":
        return student_info['Student_Level'] == 3 and student_info['Program'] == "Computer Engineering"
    elif condition == "Senior_ECOM":
        return student_info['Student_Level'] == 4 and student_info['Program'] == "Computer Engineering"
    elif condition == "AND_OR_2":
        return all(prereq in taken_courses for prereq in prereqs[:2]) and any(prereq in taken_courses for prereq in prereqs[2:])
    elif condition == "AND_OR_3":
        return any(prereq in taken_courses for prereq in prereqs[:2]) and all(prereq in taken_courses for prereq in prereqs[2:])
    elif condition == "AND_College_OR":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    else:
        return False    

# Helper Functions from provided logic
def combine_eligible_courses(df1, df2):
    if df1.shape != df2.shape:
        raise ValueError("Dataframes do not have the same shape.")
    
    if list(df1.columns) != list(df2.columns):
        raise ValueError("Dataframes do not have the same headers.")
    
    combined_data = []
    for index, row in df1.iterrows():
        combined_row = row.copy()
        combined_courses = list(set(row['Eligible_Courses'] + df2.loc[index, 'Eligible_Courses']))
        combined_row['Eligible_Courses'] = combined_courses
        combined_data.append(combined_row)
    
    combined_df = pd.DataFrame(combined_data)
    
    return combined_df

def find_course_combinations(student_courses, requisites_data):
    combinations = []
    for _, row in requisites_data.iterrows():
        requisites_list = row['REQUISITES_LIST']
        course_id = row['Course_ID']
        if all(course in student_courses for course in requisites_list):
            combination = requisites_list + [course_id]
            combinations.append(combination)
    return combinations

def create_combined_courses(row, co):
    eligible_courses = row['Eligible_Courses']
    combined_courses = eligible_courses[:]
    co_requisite_courses = []
    combinations = find_course_combinations(eligible_courses, co)
    for combination in combinations:
        combined_courses += combination
        co_requisite_courses.append(combination)
    row['Co_Requisite_Courses'] = co_requisite_courses
    row['Eligible_Courses_CO'] = list(set(combined_courses))
    return row

def find_additional_eligibilities(courses, taken_courses, prerequisites):
    additional_eligibilities = set()
    for course in courses:
        hypothetical_courses = taken_courses.copy()
        hypothetical_courses.add(course)
        for c in prerequisites.keys():
            if is_eligible(c, hypothetical_courses, prerequisites) and c not in hypothetical_courses:
                additional_eligibilities.add(c)
    return list(additional_eligibilities)

def find_additional_eligibilities_special(courses, taken_courses, student_info, prerequisites_special, conditions, is_eligible_special):
    additional_eligibilities = set()
    hypothetical_courses = taken_courses.copy()
    for course in courses:
        hypothetical_courses.add(course)
        for c in prerequisites_special.keys():
            if is_eligible_special(c, hypothetical_courses, student_info, prerequisites_special, conditions) and c not in hypothetical_courses:
                additional_eligibilities.add(c)
    return list(additional_eligibilities)

def is_eligible_special_acc_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "AND_Senior":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Student_Level'] == 4
    elif condition == "AND_Major_ACC":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Accounting"
    else:
        return False
    
def is_eligible_special_ib_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_Major_MG_IB":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior")
    elif condition == "AND_Major_MG_IB_MRKT":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior" or student_info['Major'] == "Marketing")
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    else:
        return False
    
def is_eligible_special_mob_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")

    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_Major_MG_IB":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior")
    elif condition == "AND_Major_MG_IB_MRKT":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior" or student_info['Major'] == "Marketing")
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    else:
        return False
    
def is_eligible_special_mis_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")

    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "AND_Major_MIS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Management Information Systems"
    else:
        return False
    
def is_eligible_special_mrkt_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_Major_MG_IB_MRKT":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "International Business" or student_info['Major'] == "Mgmt & Organizational Behavior" or student_info['Major'] == "Marketing")
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "AND_Major_MRKT":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Marketing"
    else:
        return False
    
def is_eligible_special_fin_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_NOT_CS":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "OR_AND_NOT_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] != "Computer Science"
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "OR_AND":
        return all(prereq in taken_courses for prereq in prereqs[:2]) or any(prereq in taken_courses for prereq in prereqs[2:])
    elif condition == "AND_Major_FIN":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Finance"
    elif condition == "AND_Senior":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Student_Level'] == 4
    else:
        return False

def is_eligible_special_cs_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "AND_College_OR":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "OR_CS":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "Computer Science"
    elif condition == "Any_Two":
        return sum(prereq in taken_courses for prereq in prereqs) >= 2
    elif condition == "OR_AND_College_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    else:
        return False
    
def is_eligible_special_dmp_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "OR_MCOM":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 54 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM_2":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 60 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_OR_2":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:3]) and any(prereq in taken_courses for prereq in prereqs[3:])
    elif condition == "AND_OR_PR":
        return (all(prereq in taken_courses for prereq in prereqs[:3]) and student_info['Major'] == "Public relations & Advertising") or all(prereq in taken_courses for prereq in prereqs[4:]) 
    elif condition == "AND_OR_Junior_Program":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:]) and student_info['Student_Level'] == 3 and student_info['Program'] == "Mass Communication"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    elif condition == "AND_Junior":
        return student_info['Student_Level'] == 3 and all(prereq in taken_courses for prereq in prereqs)
    elif condition == "OR_MCOM":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Junior_Program":
        return student_info['Student_Level'] == 3 and all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    else:
        return False
    
def is_eligible_special_eng_lin_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_UENG":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "English"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    else:
        return False
    
def is_eligible_special_eng_edu_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_EDU":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Major'] == "English Education"
    elif condition == "AND_UENG":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "English"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    elif condition == "Any_Three":
        return sum(prereq in taken_courses for prereq in prereqs) >= 3
    else:
        return False
    
def is_eligible_special_eng_lit_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_UENG":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "English"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    else:
        return False
    
def is_eligible_special_pr_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "OR_MCOM":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 54 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM_2":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 60 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_OR_2":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:3]) and any(prereq in taken_courses for prereq in prereqs[3:])
    elif condition == "AND_OR_PR":
        return (all(prereq in taken_courses for prereq in prereqs[:3]) and student_info['Major'] == "Public relations & Advertising") or all(prereq in taken_courses for prereq in prereqs[4:])
    elif condition == "AND_OR_Junior_Program":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:]) and student_info['Student_Level'] == 3 and student_info['Program'] == "Mass Communication"
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    elif condition == "AND_Junior_Program":
        return student_info['Student_Level'] == 3 and all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    else:
        return False
    
def is_eligible_special_vc_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "OR_MCOM":
        return any(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 54 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_OR_Junior_Program":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:]) and student_info['Student_Level'] == 3 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_Credits_MCOM_2":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['Passed Credits'] >= 60 and student_info['Program'] == "Mass Communication"
    elif condition == "AND_OR_2":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:3]) and any(prereq in taken_courses for prereq in prereqs[3:])
    elif condition == "AND_OR_PR":
        return (all(prereq in taken_courses for prereq in prereqs[:3]) and student_info['Major'] == "Public relations & Advertising") or all(prereq in taken_courses for prereq in prereqs[4:])
    elif condition == "OR_AND_Program_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Program'] == "Mass Communication" or student_info['Program'] == "English")
    elif condition == "AND_Junior_Program":
        return student_info['Student_Level'] == 3 and all(prereq in taken_courses for prereq in prereqs) and student_info['Program'] == "Mass Communication"
    else:
        return False
    
def is_eligible_special_mgmt_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_College":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['College'] == "COE"
    elif condition == "AND_College_OR":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "AND_OR_2":
        return all(prereq in taken_courses for prereq in prereqs[:2]) and any(prereq in taken_courses for prereq in prereqs[3:])
    else:
        return False
    
def is_eligible_special_elec_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_College":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['College'] == "COE"
    elif condition == "OR_AND_College_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "AND_College_OR":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "AND_Senior":
        return student_info['Student_Level'] == 4 and all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_OR_2":
        return all(prereq in taken_courses for prereq in prereqs[:2]) and any(prereq in taken_courses for prereq in prereqs[3:])
    elif condition == "AND_3_Courses":
        return all(prereq in taken_courses for prereq in prereqs[:3]) and sum(prereq in taken_courses for prereq in prereqs[3:]) >= 3
    else:
        return False
    
def is_eligible_special_comp_(course, taken_courses, student_info,prerequisites,conditions):
    prereqs = prerequisites.get(course, [])
    condition = conditions.get(course, "")
    
    if condition == "OR":
        return any(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND":
        return all(prereq in taken_courses for prereq in prereqs)
    elif condition == "AND_College":
        return all(prereq in taken_courses for prereq in prereqs) and student_info['College'] == "COE"
    elif condition == "OR_AND_College_OR":
        return any(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    elif condition == "AND_OR":
        return prereqs and prereqs[0] in taken_courses and any(prereq in taken_courses for prereq in prereqs[1:])
    elif condition == "AND_OR_2":
        return all(prereq in taken_courses for prereq in prereqs[:2]) and any(prereq in taken_courses for prereq in prereqs[2:])
    elif condition == "AND_OR_3":
        return any(prereq in taken_courses for prereq in prereqs[:2]) and all(prereq in taken_courses for prereq in prereqs[2:])
    elif condition == "AND_College_OR":
        return all(prereq in taken_courses for prereq in prereqs) and (student_info['Major'] == "Computer Science" or student_info['College'] == "COE")
    else:
        return False

def find_best_courses_cba(group):
    sorted_courses = group.sort_values(by='Course_Score', ascending=False)
    return sorted_courses['Eligible_Courses'].tolist()[:4] 

def find_best_courses(group):
    sorted_courses = group.sort_values(by='Course_Score', ascending=False)
    return sorted_courses['Eligible_Courses_CO'].tolist()[:4] 

# Function to process the data

def process_data_acc(cba_data, acc_data, major_data):
    # Filtering and Sorting Data
    acc_data = cba_data[cba_data['Major'] == 'Accounting']
    acc_data = acc_data.sort_values(by=['Student_ID', 'Semester'])

    cba_list = major_data["CBA_list"]
    acc_list = cba_list[cba_list["Major"] == "ACCOUNTING"]

    cba_special_cases = major_data["CBA_Special_Cases"]
    acc_special_cases = cba_special_cases[cba_special_cases["Major"] == "ACCOUNTING"]

    # Combining DataFrames
    courses_acc = pd.concat([acc_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           acc_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_acc = courses_acc.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_acc = acc_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_acc = acc_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_acc = acc_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_acc = acc_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_acc = []

    for student_id, group in acc_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_acc.keys() if is_eligible(course, cumulative_courses, prerequisites_acc) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_acc.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_acc = pd.DataFrame(final_results_acc)

    # Processing for Special Eligibility
    final_results_special_acc = []

    for student_id, group in acc_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_acc.keys() if is_eligible_special_acc(course, cumulative_courses, student_info,prerequisites_special_acc,conditions_acc) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_acc.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_acc = pd.DataFrame(final_results_special_acc)

    # Combine Eligible Courses from Both DataFrames
    combined_acc_list = combine_eligible_courses(final_results_df_acc, final_results_special_df_acc)

    # Exploding and Mapping Course Details
    combined_df_acc = combined_acc_list.explode("Eligible_Courses")
    #combined_df_acc = combined_df_acc.dropna(subset=["Eligible_Courses"])
    combined_df_acc["AREA_OF_STUDY"] = combined_df_acc['Eligible_Courses'].map(courses_acc.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_acc["COURSE_OF_STUDY"] = combined_df_acc['Eligible_Courses'].map(courses_acc.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_acc['Eligible_Courses'] = combined_df_acc['Eligible_Courses'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_acc['Future_Eligible_Courses_List'] = combined_df_acc.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses'], set(row['Eligible_Courses']), prerequisites_acc), axis=1)
    combined_df_acc['Total_Future_Eligible_Courses'] = combined_df_acc['Future_Eligible_Courses_List'].apply(len)   

    combined_df_acc['Future_Eligible_Courses_List_Special'] = combined_df_acc.apply(
    lambda row: find_additional_eligibilities_special(row['Eligible_Courses'], set(row['Eligible_Courses']), row, prerequisites_special_acc, conditions_acc, is_eligible_special_acc_), axis=1)
    combined_df_acc['Total_Future_Eligible_Courses_Special'] = combined_df_acc['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_acc["Future_Eligible_Courses"] = combined_df_acc["Future_Eligible_Courses_List"] + combined_df_acc["Future_Eligible_Courses_List_Special"]
    combined_df_acc['Course_Score'] = combined_df_acc['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_acc = combined_df_acc.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses_cba(group)})).reset_index()
    combined_df_acc = combined_df_acc.merge(recommended_courses_acc, on=['Student_ID', 'Semester'])
    #recommended_courses_acc_explode = recommended_courses_acc.explode("Recommended_Courses")


    return combined_df_acc,combined_acc_list,recommended_courses_acc

def process_data_ib(cba_data, ib_data, major_data):
    # Filtering and Sorting Data
    ib_data = cba_data[cba_data['Major'] == 'International Business']
    ib_data = ib_data.sort_values(by=['Student_ID', 'Semester'])

    cba_list = major_data["CBA_list"]
    ib_list = cba_list[cba_list["Major"] == "INTL BUSIN"]

    cba_special_cases = major_data["CBA_Special_Cases"]
    ib_special_cases = cba_special_cases[cba_special_cases["Major"] == "INTL BUSIN"]

    # Combining DataFrames
    courses_ib = pd.concat([ib_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           ib_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_ib = courses_ib.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_ib = ib_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_ib = ib_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_ib = ib_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_ib = ib_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_ib = []

    for student_id, group in ib_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_ib.keys() if is_eligible(course, cumulative_courses, prerequisites_ib) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_ib.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_ib = pd.DataFrame(final_results_ib)

    # Processing for Special Eligibility
    final_results_special_ib = []

    for student_id, group in ib_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_ib.keys() if is_eligible_special_ib(course, cumulative_courses, student_info,prerequisites_special_ib,conditions_ib) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_ib.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_ib = pd.DataFrame(final_results_special_ib)

    # Combine Eligible Courses from Both DataFrames
    combined_ib_list = combine_eligible_courses(final_results_df_ib, final_results_special_df_ib)

    # Exploding and Mapping Course Details
    combined_df_ib = combined_ib_list.explode("Eligible_Courses")
    #combined_df_ib = combined_df_ib.dropna(subset=["Eligible_Courses"])
    combined_df_ib["AREA_OF_STUDY"] = combined_df_ib['Eligible_Courses'].map(courses_ib.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_ib["COURSE_OF_STUDY"] = combined_df_ib['Eligible_Courses'].map(courses_ib.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_ib['Eligible_Courses'] = combined_df_ib['Eligible_Courses'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_ib['Future_Eligible_Courses_List'] = combined_df_ib.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses'], set(row['Eligible_Courses']), prerequisites_ib), axis=1)
    combined_df_ib['Total_Future_Eligible_Courses'] = combined_df_ib['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_ib['Future_Eligible_Courses_List_Special'] = combined_df_ib.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses'], set(row['Eligible_Courses']), row, prerequisites_special_ib, conditions_ib, is_eligible_special_ib_), axis=1)
    combined_df_ib['Total_Future_Eligible_Courses_Special'] = combined_df_ib['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_ib["Future_Eligible_Courses"] = combined_df_ib["Future_Eligible_Courses_List"] + combined_df_ib["Future_Eligible_Courses_List_Special"]
    combined_df_ib['Course_Score'] = combined_df_ib['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_ib = combined_df_ib.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses_cba(group)})).reset_index()
    combined_df_ib = combined_df_ib.merge(recommended_courses_ib, on=['Student_ID', 'Semester'])

    return combined_df_ib,combined_ib_list,recommended_courses_ib

def process_data_mob(cba_data, mob_data, major_data):
    # Filtering and Sorting Data
    mob_data = cba_data[cba_data['Major'] == 'Mgmt & Organizational Behavior']
    mob_data = mob_data.sort_values(by=['Student_ID', 'Semester'])

    cba_list = major_data["CBA_list"]
    mob_list = cba_list[cba_list["Major"] == "MANAGEMENT"]

    cba_special_cases = major_data["CBA_Special_Cases"]
    mob_special_cases = cba_special_cases[cba_special_cases["Major"] == "MANAGEMENT"]

    # Combining DataFrames
    courses_mob = pd.concat([mob_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           mob_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_mob = courses_mob.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_mob = mob_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_mob = mob_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_mob = mob_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_mob = mob_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_mob = []

    for student_id, group in mob_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_mob.keys() if is_eligible(course, cumulative_courses, prerequisites_mob) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_mob.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_mob = pd.DataFrame(final_results_mob)

    # Processing for Special Eligibility
    final_results_special_mob = []

    for student_id, group in mob_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_mob.keys() if is_eligible_special_mob(course, cumulative_courses, student_info,prerequisites_special_mob,conditions_mob) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_mob.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_mob = pd.DataFrame(final_results_special_mob)

    # Combine Eligible Courses from Both DataFrames
    combined_mob_list = combine_eligible_courses(final_results_df_mob, final_results_special_df_mob)

    # Exploding and Mapping Course Details
    combined_df_mob = combined_mob_list.explode("Eligible_Courses")
    #combined_df_mob = combined_df_mob.dropna(subset=["Eligible_Courses"])
    combined_df_mob["AREA_OF_STUDY"] = combined_df_mob['Eligible_Courses'].map(courses_mob.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_mob["COURSE_OF_STUDY"] = combined_df_mob['Eligible_Courses'].map(courses_mob.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_mob['Eligible_Courses'] = combined_df_mob['Eligible_Courses'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_mob['Future_Eligible_Courses_List'] = combined_df_mob.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses'], set(row['Eligible_Courses']), prerequisites_mob), axis=1)
    combined_df_mob['Total_Future_Eligible_Courses'] = combined_df_mob['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_mob['Future_Eligible_Courses_List_Special'] = combined_df_mob.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses'], set(row['Eligible_Courses']), row, prerequisites_special_mob, conditions_mob, is_eligible_special_mob_), axis=1)
    combined_df_mob['Total_Future_Eligible_Courses_Special'] = combined_df_mob['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_mob["Future_Eligible_Courses"] = combined_df_mob["Future_Eligible_Courses_List"] + combined_df_mob["Future_Eligible_Courses_List_Special"]
    combined_df_mob['Course_Score'] = combined_df_mob['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_mob = combined_df_mob.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses_cba(group)})).reset_index()
    combined_df_mob = combined_df_mob.merge(recommended_courses_mob, on=['Student_ID', 'Semester'])

    return combined_df_mob,combined_mob_list,recommended_courses_mob

def process_data_mis(cba_data, mis_data, major_data):
    # Filtering and Sorting Data
    mis_data = cba_data[cba_data['Major'] == 'Management Information Systems']
    mis_data = mis_data.sort_values(by=['Student_ID', 'Semester'])

    cba_list = major_data["CBA_list"]
    mis_list = cba_list[cba_list["Major"] == "MIS"]

    cba_special_cases = major_data["CBA_Special_Cases"]
    mis_special_cases = cba_special_cases[cba_special_cases["Major"] == "MIS"]

    # Combining DataFrames
    courses_mis = pd.concat([mis_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           mis_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_mis = courses_mis.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_mis = mis_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_mis = mis_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_mis = mis_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_mis = mis_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_mis = []

    for student_id, group in mis_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_mis.keys() if is_eligible(course, cumulative_courses, prerequisites_mis) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_mis.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_mis = pd.DataFrame(final_results_mis)

    # Processing for Special Eligibility
    final_results_special_mis = []

    for student_id, group in mis_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_mis.keys() if is_eligible_special_mis(course, cumulative_courses, student_info,prerequisites_special_mis,conditions_mis) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_mis.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_mis = pd.DataFrame(final_results_special_mis)

    # Combine Eligible Courses from Both DataFrames
    combined_mis_list = combine_eligible_courses(final_results_df_mis, final_results_special_df_mis)

    # Exploding and Mapping Course Details
    combined_df_mis = combined_mis_list.explode("Eligible_Courses")
    #combined_df_mis = combined_df_mis.dropna(subset=["Eligible_Courses"])
    combined_df_mis["AREA_OF_STUDY"] = combined_df_mis['Eligible_Courses'].map(courses_mis.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_mis["COURSE_OF_STUDY"] = combined_df_mis['Eligible_Courses'].map(courses_mis.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_mis['Eligible_Courses'] = combined_df_mis['Eligible_Courses'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_mis['Future_Eligible_Courses_List'] = combined_df_mis.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses'], set(row['Eligible_Courses']), prerequisites_mis), axis=1)
    combined_df_mis['Total_Future_Eligible_Courses'] = combined_df_mis['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_mis['Future_Eligible_Courses_List_Special'] = combined_df_mis.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses'], set(row['Eligible_Courses']), row, prerequisites_special_mis, conditions_mis, is_eligible_special_mis_), axis=1)
    combined_df_mis['Total_Future_Eligible_Courses_Special'] = combined_df_mis['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_mis["Future_Eligible_Courses"] = combined_df_mis["Future_Eligible_Courses_List"] + combined_df_mis["Future_Eligible_Courses_List_Special"]
    combined_df_mis['Course_Score'] = combined_df_mis['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_mis = combined_df_mis.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses_cba(group)})).reset_index()
    combined_df_mis = combined_df_mis.merge(recommended_courses_mis, on=['Student_ID', 'Semester'])

    return combined_df_mis,combined_mis_list,recommended_courses_mis

def process_data_mrkt(cba_data, mrkt_data, major_data):
    # Filtering and Sorting Data
    mrkt_data = cba_data[cba_data['Major'] == 'Marketing']
    mrkt_data = mrkt_data.sort_values(by=['Student_ID', 'Semester'])

    cba_list = major_data["CBA_list"]
    mrkt_list = cba_list[cba_list["Major"] == "MARKETING2"]

    cba_special_cases = major_data["CBA_Special_Cases"]
    mrkt_special_cases = cba_special_cases[cba_special_cases["Major"] == "MARKETING2"]

    # Combining DataFrames
    courses_mrkt = pd.concat([mrkt_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           mrkt_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_mrkt = courses_mrkt.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_mrkt = mrkt_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_mrkt = mrkt_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_mrkt = mrkt_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_mrkt = mrkt_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_mrkt = []

    for student_id, group in mrkt_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_mrkt.keys() if is_eligible(course, cumulative_courses, prerequisites_mrkt) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_mrkt.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_mrkt = pd.DataFrame(final_results_mrkt)

    # Processing for Special Eligibility
    final_results_special_mrkt = []

    for student_id, group in mrkt_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_mrkt.keys() if is_eligible_special_mrkt(course, cumulative_courses, student_info,prerequisites_special_mrkt,conditions_mrkt) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_mrkt.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_mrkt = pd.DataFrame(final_results_special_mrkt)

    # Combine Eligible Courses from Both DataFrames
    combined_mrkt_list = combine_eligible_courses(final_results_df_mrkt, final_results_special_df_mrkt)

    # Exploding and Mapping Course Details
    combined_df_mrkt = combined_mrkt_list.explode("Eligible_Courses")
    #combined_df_mrkt = combined_df_mrkt.dropna(subset=["Eligible_Courses"])
    combined_df_mrkt["AREA_OF_STUDY"] = combined_df_mrkt['Eligible_Courses'].map(courses_mrkt.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_mrkt["COURSE_OF_STUDY"] = combined_df_mrkt['Eligible_Courses'].map(courses_mrkt.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_mrkt['Eligible_Courses'] = combined_df_mrkt['Eligible_Courses'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_mrkt['Future_Eligible_Courses_List'] = combined_df_mrkt.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses'], set(row['Eligible_Courses']), prerequisites_mrkt), axis=1)
    combined_df_mrkt['Total_Future_Eligible_Courses'] = combined_df_mrkt['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_mrkt['Future_Eligible_Courses_List_Special'] = combined_df_mrkt.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses'], set(row['Eligible_Courses']), row, prerequisites_special_mrkt, conditions_mrkt, is_eligible_special_mrkt_), axis=1)
    combined_df_mrkt['Total_Future_Eligible_Courses_Special'] = combined_df_mrkt['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_mrkt["Future_Eligible_Courses"] = combined_df_mrkt["Future_Eligible_Courses_List"] + combined_df_mrkt["Future_Eligible_Courses_List_Special"]
    combined_df_mrkt['Course_Score'] = combined_df_mrkt['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_mrkt = combined_df_mrkt.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses_cba(group)})).reset_index()
    combined_df_mrkt = combined_df_mrkt.merge(recommended_courses_mrkt, on=['Student_ID', 'Semester'])

    return combined_df_mrkt,combined_mrkt_list,recommended_courses_mrkt

def process_data_fin(cba_data, fin_data, major_data):
    # Filtering and Sorting Data
    fin_data = cba_data[cba_data['Major'] == 'Finance']
    fin_data = fin_data.sort_values(by=['Student_ID', 'Semester'])

    cba_list = major_data["CBA_list"]
    fin_list = cba_list[cba_list["Major"] == "FINANCE"]

    cba_special_cases = major_data["CBA_Special_Cases"]
    fin_special_cases = cba_special_cases[cba_special_cases["Major"] == "FINANCE"]

    # Combining DataFrames
    courses_fin = pd.concat([fin_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           fin_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_fin = courses_fin.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_fin = fin_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_fin = fin_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_fin = fin_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_fin = fin_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_fin = []

    for student_id, group in fin_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_fin.keys() if is_eligible(course, cumulative_courses, prerequisites_fin) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_fin.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_fin = pd.DataFrame(final_results_fin)

    # Processing for Special Eligibility
    final_results_special_fin = []

    for student_id, group in fin_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_fin.keys() if is_eligible_special_fin(course, cumulative_courses, student_info,prerequisites_special_fin,conditions_fin) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_fin.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_fin = pd.DataFrame(final_results_special_fin)

    # Combine Eligible Courses from Both DataFrames
    combined_fin_list = combine_eligible_courses(final_results_df_fin, final_results_special_df_fin)

    # Exploding and Mapping Course Details
    combined_df_fin = combined_fin_list.explode("Eligible_Courses")
    #combined_df_fin = combined_df_fin.dropna(subset=["Eligible_Courses"])
    combined_df_fin["AREA_OF_STUDY"] = combined_df_fin['Eligible_Courses'].map(courses_fin.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_fin["COURSE_OF_STUDY"] = combined_df_fin['Eligible_Courses'].map(courses_fin.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_fin['Eligible_Courses'] = combined_df_fin['Eligible_Courses'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_fin['Future_Eligible_Courses_List'] = combined_df_fin.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses'], set(row['Eligible_Courses']), prerequisites_fin), axis=1)
    combined_df_fin['Total_Future_Eligible_Courses'] = combined_df_fin['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_fin['Future_Eligible_Courses_List_Special'] = combined_df_fin.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses'], set(row['Eligible_Courses']), row, prerequisites_special_fin, conditions_fin, is_eligible_special_fin_), axis=1)
    combined_df_fin['Total_Future_Eligible_Courses_Special'] = combined_df_fin['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_fin["Future_Eligible_Courses"] = combined_df_fin["Future_Eligible_Courses_List"] + combined_df_fin["Future_Eligible_Courses_List_Special"]
    combined_df_fin['Course_Score'] = combined_df_fin['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_fin = combined_df_fin.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses_cba(group)})).reset_index()
    combined_df_fin = combined_df_fin.merge(recommended_courses_fin, on=['Student_ID', 'Semester'])

    return combined_df_fin,combined_fin_list,recommended_courses_fin

def process_data_cs(cas_data, cs_data, major_data):
    # Filtering and Sorting Data
    cs_data = cas_data[cas_data['Major'] == 'Computer Science']
    cs_data = cs_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cas_list = major_data["CAS_list"]
    cs_list = cas_list[cas_list["Major"] == "COMSCIENCE"]

    cas_special_cases = major_data["CAS_Special_Cases"]
    cs_special_cases = cas_special_cases[cas_special_cases["Major"] == "COMSCIENCE"]

    cas_co = major_data["CAS_CO"]
    cs_co = cas_co[cas_co["Major"] == "COMSCIENCE"]

    # Process 'REQUISITES_LIST'
    cs_co = cs_co.copy()
    cs_co.loc[:, 'REQUISITES_LIST'] = cs_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_cs = pd.concat([cs_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           cs_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           cs_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_cs = courses_cs.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_cs = cs_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_cs = cs_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_cs = cs_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_cs = cs_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_cs = []

    for student_id, group in cs_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_cs.keys() if is_eligible(course, cumulative_courses, prerequisites_cs) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_cs.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_cs = pd.DataFrame(final_results_cs)

    # Processing for Special Eligibility
    final_results_special_cs = []

    for student_id, group in cs_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_cs.keys() if is_eligible_special_cs(course, cumulative_courses, student_info,prerequisites_special_cs,conditions_cs) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_cs.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_cs = pd.DataFrame(final_results_special_cs)

    # Combine Eligible Courses from Both DataFrames
    combined_cs_list = combine_eligible_courses(final_results_df_cs, final_results_special_df_cs)

    # Find Course Combinations for Co-requisites
    combined_cs_list = combined_cs_list.apply(create_combined_courses, axis=1, co=cs_co)

    # Exploding and Mapping Course Details
    combined_df_cs = combined_cs_list.explode("Eligible_Courses_CO")
    #combined_df_cs = combined_df_cs.dropna(subset=["Eligible_Courses_CO"])
    combined_df_cs["AREA_OF_STUDY"] = combined_df_cs['Eligible_Courses_CO'].map(courses_cs.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_cs["COURSE_OF_STUDY"] = combined_df_cs['Eligible_Courses_CO'].map(courses_cs.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_cs['Eligible_Courses_CO'] = combined_df_cs['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_cs['Future_Eligible_Courses_List'] = combined_df_cs.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_cs), axis=1)
    combined_df_cs['Total_Future_Eligible_Courses'] = combined_df_cs['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_cs['Future_Eligible_Courses_List_Special'] = combined_df_cs.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_cs, conditions_cs, is_eligible_special_cs_), axis=1)
    combined_df_cs['Total_Future_Eligible_Courses_Special'] = combined_df_cs['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_cs["Future_Eligible_Courses"] = combined_df_cs["Future_Eligible_Courses_List"] + combined_df_cs["Future_Eligible_Courses_List_Special"]
    combined_df_cs['Course_Score'] = combined_df_cs['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_cs = combined_df_cs.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_cs = combined_df_cs.merge(recommended_courses_cs, on=['Student_ID', 'Semester'])

    return combined_df_cs,combined_cs_list,recommended_courses_cs

def process_data_dmp(cas_data, dmp_data, major_data):
    # Filtering and Sorting Data
    dmp_data = cas_data[cas_data['Major'] == 'Digital Media Production']
    dmp_data = dmp_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cas_list = major_data["CAS_list"]
    dmp_list = cas_list[cas_list["Major"] == "DIGITALMED"]

    cas_special_cases = major_data["CAS_Special_Cases"]
    dmp_special_cases = cas_special_cases[cas_special_cases["Major"] == "DIGITALMED"]

    cas_co = major_data["CAS_CO"]
    dmp_co = cas_co[cas_co["Major"] == "DIGITALMED"]

    # Process 'REQUISITES_LIST'
    dmp_co = dmp_co.copy()
    dmp_co.loc[:, 'REQUISITES_LIST'] = dmp_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_dmp = pd.concat([dmp_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           dmp_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           dmp_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_dmp = courses_dmp.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_dmp = dmp_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_dmp = dmp_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_dmp = dmp_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_dmp = dmp_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_dmp = []

    for student_id, group in dmp_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_dmp.keys() if is_eligible(course, cumulative_courses, prerequisites_dmp) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_dmp.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_dmp = pd.DataFrame(final_results_dmp)

    # Processing for Special Eligibility
    final_results_special_dmp = []

    for student_id, group in dmp_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_dmp.keys() if is_eligible_special_dmp(course, cumulative_courses, student_info,prerequisites_special_dmp,conditions_dmp) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_dmp.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_dmp = pd.DataFrame(final_results_special_dmp)

    # Combine Eligible Courses from Both DataFrames
    combined_dmp_list = combine_eligible_courses(final_results_df_dmp, final_results_special_df_dmp)

    # Find Course Combinations for Co-requisites
    combined_dmp_list = combined_dmp_list.apply(create_combined_courses, axis=1, co=dmp_co)

    # Exploding and Mapping Course Details
    combined_df_dmp = combined_dmp_list.explode("Eligible_Courses_CO")
    #combined_df_dmp = combined_df_dmp.dropna(subset=["Eligible_Courses_CO"])
    combined_df_dmp["AREA_OF_STUDY"] = combined_df_dmp['Eligible_Courses_CO'].map(courses_dmp.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_dmp["COURSE_OF_STUDY"] = combined_df_dmp['Eligible_Courses_CO'].map(courses_dmp.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_dmp['Eligible_Courses_CO'] = combined_df_dmp['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_dmp['Future_Eligible_Courses_List'] = combined_df_dmp.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_dmp), axis=1)
    combined_df_dmp['Total_Future_Eligible_Courses'] = combined_df_dmp['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_dmp['Future_Eligible_Courses_List_Special'] = combined_df_dmp.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_dmp, conditions_dmp, is_eligible_special_dmp_), axis=1)
    combined_df_dmp['Total_Future_Eligible_Courses_Special'] = combined_df_dmp['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_dmp["Future_Eligible_Courses"] = combined_df_dmp["Future_Eligible_Courses_List"] + combined_df_dmp["Future_Eligible_Courses_List_Special"]
    combined_df_dmp['Course_Score'] = combined_df_dmp['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_dmp = combined_df_dmp.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_dmp = combined_df_dmp.merge(recommended_courses_dmp, on=['Student_ID', 'Semester'])

    return combined_df_dmp,combined_dmp_list,recommended_courses_dmp

def process_data_eng_lin(cas_data, eng_lin_data, major_data):
    # Filtering and Sorting Data
    eng_lin_data = cas_data[cas_data['Major'] == 'Eng- Linguistics - Translation']
    eng_lin_data = eng_lin_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cas_list = major_data["CAS_list"]
    eng_lin_list = cas_list[cas_list["Major"] == "LINGUISTIC"]

    cas_special_cases = major_data["CAS_Special_Cases"]
    eng_lin_special_cases = cas_special_cases[cas_special_cases["Major"] == "LINGUISTIC"]

    cas_co = major_data["CAS_CO"]
    eng_lin_co = cas_co[cas_co["Major"] == "LINGUISTIC"]

    # Process 'REQUISITES_LIST'
    eng_lin_co = eng_lin_co.copy()
    eng_lin_co.loc[:, 'REQUISITES_LIST'] = eng_lin_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_eng_lin = pd.concat([eng_lin_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           eng_lin_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           eng_lin_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_eng_lin = courses_eng_lin.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_eng_lin = eng_lin_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_eng_lin = eng_lin_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_eng_lin = eng_lin_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_eng_lin = eng_lin_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_eng_lin = []

    for student_id, group in eng_lin_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_eng_lin.keys() if is_eligible(course, cumulative_courses, prerequisites_eng_lin) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_eng_lin.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_eng_lin = pd.DataFrame(final_results_eng_lin)

    # Processing for Special Eligibility
    final_results_special_eng_lin = []

    for student_id, group in eng_lin_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_eng_lin.keys() if is_eligible_special_eng_lin(course, cumulative_courses, student_info,prerequisites_special_eng_lin,conditions_eng_lin) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_eng_lin.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_eng_lin = pd.DataFrame(final_results_special_eng_lin)

    # Combine Eligible Courses from Both DataFrames
    combined_eng_lin_list = combine_eligible_courses(final_results_df_eng_lin, final_results_special_df_eng_lin)

    # Find Course Combinations for Co-requisites
    combined_eng_lin_list = combined_eng_lin_list.apply(create_combined_courses, axis=1, co=eng_lin_co)

    # Exploding and Mapping Course Details
    combined_df_eng_lin = combined_eng_lin_list.explode("Eligible_Courses_CO")
    #combined_df_eng_lin = combined_df_eng_lin.dropna(subset=["Eligible_Courses_CO"])
    combined_df_eng_lin["AREA_OF_STUDY"] = combined_df_eng_lin['Eligible_Courses_CO'].map(courses_eng_lin.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_eng_lin["COURSE_OF_STUDY"] = combined_df_eng_lin['Eligible_Courses_CO'].map(courses_eng_lin.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_eng_lin['Eligible_Courses_CO'] = combined_df_eng_lin['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))


    # Find Additional Eligibilities
    combined_df_eng_lin['Future_Eligible_Courses_List'] = combined_df_eng_lin.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_eng_lin), axis=1)
    combined_df_eng_lin['Total_Future_Eligible_Courses'] = combined_df_eng_lin['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_eng_lin['Future_Eligible_Courses_List_Special'] = combined_df_eng_lin.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_eng_lin, conditions_eng_lin, is_eligible_special_eng_lin_), axis=1)
    combined_df_eng_lin['Total_Future_Eligible_Courses_Special'] = combined_df_eng_lin['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_eng_lin["Future_Eligible_Courses"] = combined_df_eng_lin["Future_Eligible_Courses_List"] + combined_df_eng_lin["Future_Eligible_Courses_List_Special"]
    combined_df_eng_lin['Course_Score'] = combined_df_eng_lin['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_eng_lin = combined_df_eng_lin.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_eng_lin = combined_df_eng_lin.merge(recommended_courses_eng_lin, on=['Student_ID', 'Semester'])

    return combined_df_eng_lin,combined_eng_lin_list,recommended_courses_eng_lin

def process_data_eng_edu(cas_data, eng_edu_data, major_data):
    # Filtering and Sorting Data
    eng_edu_data = cas_data[cas_data['Major'] == 'English Education']
    eng_edu_data = eng_edu_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cas_list = major_data["CAS_list"]
    eng_edu_list = cas_list[cas_list["Major"] == "ENGLISH"]

    cas_special_cases = major_data["CAS_Special_Cases"]
    eng_edu_special_cases = cas_special_cases[cas_special_cases["Major"] == "ENGLISH"]

    cas_co = major_data["CAS_CO"]
    eng_edu_co = cas_co[cas_co["Major"] == "ENGLISH"]

    # Process 'REQUISITES_LIST'
    eng_edu_co = eng_edu_co.copy()
    eng_edu_co.loc[:, 'REQUISITES_LIST'] = eng_edu_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_eng_edu = pd.concat([eng_edu_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           eng_edu_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           eng_edu_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_eng_edu = courses_eng_edu.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_eng_edu = eng_edu_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_eng_edu = eng_edu_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_eng_edu = eng_edu_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_eng_edu = eng_edu_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_eng_edu = []

    for student_id, group in eng_edu_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_eng_edu.keys() if is_eligible(course, cumulative_courses, prerequisites_eng_edu) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_eng_edu.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_eng_edu = pd.DataFrame(final_results_eng_edu)

    # Processing for Special Eligibility
    final_results_special_eng_edu = []

    for student_id, group in eng_edu_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_eng_edu.keys() if is_eligible_special_eng_edu(course, cumulative_courses, student_info,prerequisites_special_eng_edu,conditions_eng_edu) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_eng_edu.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_eng_edu = pd.DataFrame(final_results_special_eng_edu)

    # Combine Eligible Courses from Both DataFrames
    combined_eng_edu_list = combine_eligible_courses(final_results_df_eng_edu, final_results_special_df_eng_edu)

    # Find Course Combinations for Co-requisites
    combined_eng_edu_list = combined_eng_edu_list.apply(create_combined_courses, axis=1, co=eng_edu_co)

    # Exploding and Mapping Course Details
    combined_df_eng_edu = combined_eng_edu_list.explode("Eligible_Courses_CO")
    #combined_df_eng_edu = combined_df_eng_edu.dropna(subset=["Eligible_Courses_CO"])
    combined_df_eng_edu["AREA_OF_STUDY"] = combined_df_eng_edu['Eligible_Courses_CO'].map(courses_eng_edu.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_eng_edu["COURSE_OF_STUDY"] = combined_df_eng_edu['Eligible_Courses_CO'].map(courses_eng_edu.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_eng_edu['Eligible_Courses_CO'] = combined_df_eng_edu['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))
    
    # Find Additional Eligibilities
    combined_df_eng_edu['Future_Eligible_Courses_List'] = combined_df_eng_edu.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_eng_edu), axis=1)
    combined_df_eng_edu['Total_Future_Eligible_Courses'] = combined_df_eng_edu['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_eng_edu['Future_Eligible_Courses_List_Special'] = combined_df_eng_edu.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_eng_edu, conditions_eng_edu, is_eligible_special_eng_edu_), axis=1)
    combined_df_eng_edu['Total_Future_Eligible_Courses_Special'] = combined_df_eng_edu['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_eng_edu["Future_Eligible_Courses"] = combined_df_eng_edu["Future_Eligible_Courses_List"] + combined_df_eng_edu["Future_Eligible_Courses_List_Special"]
    combined_df_eng_edu['Course_Score'] = combined_df_eng_edu['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_eng_edu = combined_df_eng_edu.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_eng_edu = combined_df_eng_edu.merge(recommended_courses_eng_edu, on=['Student_ID', 'Semester'])

    return combined_df_eng_edu,combined_eng_edu_list,recommended_courses_eng_edu

def process_data_eng_lit(cas_data, eng_lit_data, major_data):
    # Filtering and Sorting Data
    eng_lit_data = cas_data[cas_data['Major'] == 'English Literature']
    eng_lit_data = eng_lit_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cas_list = major_data["CAS_list"]
    eng_lit_list = cas_list[cas_list["Major"] == "LITERATURE"]

    cas_special_cases = major_data["CAS_Special_Cases"]
    eng_lit_special_cases = cas_special_cases[cas_special_cases["Major"] == "LITERATURE"]

    cas_co = major_data["CAS_CO"]
    eng_lit_co = cas_co[cas_co["Major"] == "LITERATURE"]

    # Process 'REQUISITES_LIST'
    eng_lit_co = eng_lit_co.copy()
    eng_lit_co.loc[:, 'REQUISITES_LIST'] = eng_lit_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_eng_lit = pd.concat([eng_lit_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           eng_lit_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           eng_lit_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_eng_lit = courses_eng_lit.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_eng_lit = eng_lit_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_eng_lit = eng_lit_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_eng_lit = eng_lit_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_eng_lit = eng_lit_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_eng_lit = []

    for student_id, group in eng_lit_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_eng_lit.keys() if is_eligible(course, cumulative_courses, prerequisites_eng_lit) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_eng_lit.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_eng_lit = pd.DataFrame(final_results_eng_lit)

    # Processing for Special Eligibility
    final_results_special_eng_lit = []

    for student_id, group in eng_lit_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_eng_lit.keys() if is_eligible_special_eng_lit(course, cumulative_courses, student_info,prerequisites_special_eng_lit,conditions_eng_lit) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_eng_lit.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_eng_lit = pd.DataFrame(final_results_special_eng_lit)

    # Combine Eligible Courses from Both DataFrames
    combined_eng_lit_list = combine_eligible_courses(final_results_df_eng_lit, final_results_special_df_eng_lit)

    # Find Course Combinations for Co-requisites
    combined_eng_lit_list = combined_eng_lit_list.apply(create_combined_courses, axis=1, co=eng_lit_co)

    # Exploding and Mapping Course Details
    combined_df_eng_lit = combined_eng_lit_list.explode("Eligible_Courses_CO")
    #combined_df_eng_lit = combined_df_eng_lit.dropna(subset=["Eligible_Courses_CO"])
    combined_df_eng_lit["AREA_OF_STUDY"] = combined_df_eng_lit['Eligible_Courses_CO'].map(courses_eng_lit.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_eng_lit["COURSE_OF_STUDY"] = combined_df_eng_lit['Eligible_Courses_CO'].map(courses_eng_lit.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_eng_lit['Eligible_Courses_CO'] = combined_df_eng_lit['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_eng_lit['Future_Eligible_Courses_List'] = combined_df_eng_lit.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_eng_lit), axis=1)
    combined_df_eng_lit['Total_Future_Eligible_Courses'] = combined_df_eng_lit['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_eng_lit['Future_Eligible_Courses_List_Special'] = combined_df_eng_lit.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_eng_lit, conditions_eng_lit, is_eligible_special_eng_lit_), axis=1)
    combined_df_eng_lit['Total_Future_Eligible_Courses_Special'] = combined_df_eng_lit['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_eng_lit["Future_Eligible_Courses"] = combined_df_eng_lit["Future_Eligible_Courses_List"] + combined_df_eng_lit["Future_Eligible_Courses_List_Special"]
    combined_df_eng_lit['Course_Score'] = combined_df_eng_lit['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_eng_lit = combined_df_eng_lit.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_eng_lit = combined_df_eng_lit.merge(recommended_courses_eng_lit, on=['Student_ID', 'Semester'])

    return combined_df_eng_lit,combined_eng_lit_list,recommended_courses_eng_lit

def process_data_pr(cas_data, pr_data, major_data):
    # Filtering and Sorting Data
    pr_data = cas_data[cas_data['Major'] == 'Public relations & Advertising']
    pr_data = pr_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cas_list = major_data["CAS_list"]
    pr_list = cas_list[cas_list["Major"] == "PR / ADV"]

    cas_special_cases = major_data["CAS_Special_Cases"]
    pr_special_cases = cas_special_cases[cas_special_cases["Major"] == "PR / ADV"]

    cas_co = major_data["CAS_CO"]
    pr_co = cas_co[cas_co["Major"] == "PR / ADV"]

    # Process 'REQUISITES_LIST'
    pr_co = pr_co.copy()
    pr_co.loc[:, 'REQUISITES_LIST'] = pr_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_pr = pd.concat([pr_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           pr_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           pr_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_pr = courses_pr.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_pr = pr_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_pr = pr_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_pr = pr_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_pr = pr_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_pr = []

    for student_id, group in pr_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_pr.keys() if is_eligible(course, cumulative_courses, prerequisites_pr) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_pr.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_pr = pd.DataFrame(final_results_pr)

    # Processing for Special Eligibility
    final_results_special_pr = []

    for student_id, group in pr_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_pr.keys() if is_eligible_special_pr(course, cumulative_courses, student_info,prerequisites_special_pr,conditions_pr) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_pr.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_pr = pd.DataFrame(final_results_special_pr)

    # Combine Eligible Courses from Both DataFrames
    combined_pr_list = combine_eligible_courses(final_results_df_pr, final_results_special_df_pr)

    # Find Course Combinations for Co-requisites
    combined_pr_list = combined_pr_list.apply(create_combined_courses, axis=1, co=pr_co)

    # Exploding and Mapping Course Details
    combined_df_pr = combined_pr_list.explode("Eligible_Courses_CO")
    #combined_df_pr = combined_df_pr.dropna(subset=["Eligible_Courses_CO"])
    combined_df_pr["AREA_OF_STUDY"] = combined_df_pr['Eligible_Courses_CO'].map(courses_pr.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_pr["COURSE_OF_STUDY"] = combined_df_pr['Eligible_Courses_CO'].map(courses_pr.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_pr['Eligible_Courses_CO'] = combined_df_pr['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_pr['Future_Eligible_Courses_List'] = combined_df_pr.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_pr), axis=1)
    combined_df_pr['Total_Future_Eligible_Courses'] = combined_df_pr['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_pr['Future_Eligible_Courses_List_Special'] = combined_df_pr.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_pr, conditions_pr, is_eligible_special_pr_), axis=1)
    combined_df_pr['Total_Future_Eligible_Courses_Special'] = combined_df_pr['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_pr["Future_Eligible_Courses"] = combined_df_pr["Future_Eligible_Courses_List"] + combined_df_pr["Future_Eligible_Courses_List_Special"]
    combined_df_pr['Course_Score'] = combined_df_pr['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_pr = combined_df_pr.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_pr = combined_df_pr.merge(recommended_courses_pr, on=['Student_ID', 'Semester'])

    return combined_df_pr,combined_pr_list,recommended_courses_pr

def process_data_vc(cas_data, vc_data, major_data):
    # Filtering and Sorting Data
    vc_data = cas_data[cas_data['Major'] == 'Visual Communication']
    vc_data = vc_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cas_list = major_data["CAS_list"]
    vc_list = cas_list[cas_list["Major"] == "VISUAL COM"]

    cas_special_cases = major_data["CAS_Special_Cases"]
    vc_special_cases = cas_special_cases[cas_special_cases["Major"] == "VISUAL COM"]

    cas_co = major_data["CAS_CO"]
    vc_co = cas_co[cas_co["Major"] == "VISUAL COM"]

    # Process 'REQUISITES_LIST'
    vc_co = vc_co.copy()
    vc_co.loc[:, 'REQUISITES_LIST'] = vc_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_vc = pd.concat([vc_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           vc_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           vc_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_vc = courses_vc.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_vc = vc_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_vc = vc_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_vc = vc_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_vc = vc_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_vc = []

    for student_id, group in vc_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_vc.keys() if is_eligible(course, cumulative_courses, prerequisites_vc) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_vc.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_vc = pd.DataFrame(final_results_vc)

    # Processing for Special Eligibility
    final_results_special_vc = []

    for student_id, group in vc_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_vc.keys() if is_eligible_special_vc(course, cumulative_courses, student_info,prerequisites_special_vc,conditions_vc) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_vc.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_vc = pd.DataFrame(final_results_special_vc)

    # Combine Eligible Courses from Both DataFrames
    combined_vc_list = combine_eligible_courses(final_results_df_vc, final_results_special_df_vc)

    # Find Course Combinations for Co-requisites
    combined_vc_list = combined_vc_list.apply(create_combined_courses, axis=1, co=vc_co)

    # Exploding and Mapping Course Details
    combined_df_vc = combined_vc_list.explode("Eligible_Courses_CO")
    #combined_df_vc = combined_df_vc.dropna(subset=["Eligible_Courses_CO"])
    combined_df_vc["AREA_OF_STUDY"] = combined_df_vc['Eligible_Courses_CO'].map(courses_vc.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_vc["COURSE_OF_STUDY"] = combined_df_vc['Eligible_Courses_CO'].map(courses_vc.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_vc['Eligible_Courses_CO'] = combined_df_vc['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_vc['Future_Eligible_Courses_List'] = combined_df_vc.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_vc), axis=1)
    combined_df_vc['Total_Future_Eligible_Courses'] = combined_df_vc['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_vc['Future_Eligible_Courses_List_Special'] = combined_df_vc.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_vc, conditions_vc, is_eligible_special_vc_), axis=1)
    combined_df_vc['Total_Future_Eligible_Courses_Special'] = combined_df_vc['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_vc["Future_Eligible_Courses"] = combined_df_vc["Future_Eligible_Courses_List"] + combined_df_vc["Future_Eligible_Courses_List_Special"]
    combined_df_vc['Course_Score'] = combined_df_vc['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_vc = combined_df_vc.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_vc = combined_df_vc.merge(recommended_courses_vc, on=['Student_ID', 'Semester'])

    return combined_df_vc,combined_vc_list,recommended_courses_vc

def process_data_mgmt(cea_data, mgmt_data, major_data):
    # Filtering and Sorting Data
    mgmt_data = cea_data[cea_data['Major'] == 'Engineering Management']
    mgmt_data = mgmt_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cea_list = major_data["CEA_list"]
    mgmt_list = cea_list[cea_list["Major"] == "MGMTENG"]

    cea_special_cases = major_data["CEA_Special_Cases"]
    mgmt_special_cases = cea_special_cases[cea_special_cases["Major"] == "MGMTENG"]

    cea_co = major_data["CEA_CO"]
    mgmt_co = cea_co[cea_co["Major"] == "MGMTENG"]

    # Process 'REQUISITES_LIST'
    mgmt_co = mgmt_co.copy()
    mgmt_co.loc[:, 'REQUISITES_LIST'] = mgmt_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_mgmt = pd.concat([mgmt_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           mgmt_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           mgmt_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_mgmt = courses_mgmt.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_mgmt = mgmt_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_mgmt = mgmt_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_mgmt = mgmt_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_mgmt = mgmt_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_mgmt = []

    for student_id, group in mgmt_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_mgmt.keys() if is_eligible(course, cumulative_courses, prerequisites_mgmt) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_mgmt.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_mgmt = pd.DataFrame(final_results_mgmt)

    # Processing for Special Eligibility
    final_results_special_mgmt = []

    for student_id, group in mgmt_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_mgmt.keys() if is_eligible_special_mgmt(course, cumulative_courses, student_info,prerequisites_special_mgmt,conditions_mgmt) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_mgmt.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_mgmt = pd.DataFrame(final_results_special_mgmt)

    # Combine Eligible Courses from Both DataFrames
    combined_mgmt_list = combine_eligible_courses(final_results_df_mgmt, final_results_special_df_mgmt)

    # Find Course Combinations for Co-requisites
    combined_mgmt_list = combined_mgmt_list.apply(create_combined_courses, axis=1, co=mgmt_co)

    # Exploding and Mapping Course Details
    combined_df_mgmt = combined_mgmt_list.explode("Eligible_Courses_CO")
    #combined_df_mgmt = combined_df_mgmt.dropna(subset=["Eligible_Courses_CO"])
    combined_df_mgmt["AREA_OF_STUDY"] = combined_df_mgmt['Eligible_Courses_CO'].map(courses_mgmt.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_mgmt["COURSE_OF_STUDY"] = combined_df_mgmt['Eligible_Courses_CO'].map(courses_mgmt.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_mgmt['Eligible_Courses_CO'] = combined_df_mgmt['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_mgmt['Future_Eligible_Courses_List'] = combined_df_mgmt.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_mgmt), axis=1)
    combined_df_mgmt['Total_Future_Eligible_Courses'] = combined_df_mgmt['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_mgmt['Future_Eligible_Courses_List_Special'] = combined_df_mgmt.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_mgmt, conditions_mgmt, is_eligible_special_mgmt_), axis=1)
    combined_df_mgmt['Total_Future_Eligible_Courses_Special'] = combined_df_mgmt['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_mgmt["Future_Eligible_Courses"] = combined_df_mgmt["Future_Eligible_Courses_List"] + combined_df_mgmt["Future_Eligible_Courses_List_Special"]
    combined_df_mgmt['Course_Score'] = combined_df_mgmt['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_mgmt = combined_df_mgmt.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_mgmt = combined_df_mgmt.merge(recommended_courses_mgmt, on=['Student_ID', 'Semester'])

    return combined_df_mgmt,combined_mgmt_list,recommended_courses_mgmt

def process_data_elec(cea_data, elec_data, major_data):
    # Filtering and Sorting Data
    elec_data = cea_data[cea_data['Major'] == 'Electrical Engineering']
    elec_data = elec_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cea_list = major_data["CEA_list"]
    elec_list = cea_list[cea_list["Major"] == "ELECENG"]

    cea_special_cases = major_data["CEA_Special_Cases"]
    elec_special_cases = cea_special_cases[cea_special_cases["Major"] == "ELECENG"]

    cea_co = major_data["CEA_CO"]
    elec_co = cea_co[cea_co["Major"] == "ELECENG"]

    # Process 'REQUISITES_LIST'
    elec_co = elec_co.copy()
    elec_co.loc[:, 'REQUISITES_LIST'] = elec_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_elec = pd.concat([elec_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           cea_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           elec_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_elec = courses_elec.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_elec = elec_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_elec = elec_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_elec = cea_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_elec = cea_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_elec = []

    for student_id, group in elec_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_elec.keys() if is_eligible(course, cumulative_courses, prerequisites_elec) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_elec.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_elec = pd.DataFrame(final_results_elec)

    # Processing for Special Eligibility
    final_results_special_elec = []

    for student_id, group in elec_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_elec.keys() if is_eligible_special_elec(course, cumulative_courses, student_info,prerequisites_special_elec,conditions_elec) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_elec.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_elec = pd.DataFrame(final_results_special_elec)

    # Combine Eligible Courses from Both DataFrames
    combined_elec_list = combine_eligible_courses(final_results_df_elec, final_results_special_df_elec)

    # Find Course Combinations for Co-requisites
    combined_elec_list = combined_elec_list.apply(create_combined_courses, axis=1, co=elec_co)

    # Exploding and Mapping Course Details
    combined_df_elec = combined_elec_list.explode("Eligible_Courses_CO")
    #combined_df_elec = combined_df_elec.dropna(subset=["Eligible_Courses_CO"])
    combined_df_elec["AREA_OF_STUDY"] = combined_df_elec['Eligible_Courses_CO'].map(courses_elec.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_elec["COURSE_OF_STUDY"] = combined_df_elec['Eligible_Courses_CO'].map(courses_elec.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_elec['Eligible_Courses_CO'] = combined_df_elec['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_elec['Future_Eligible_Courses_List'] = combined_df_elec.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_elec), axis=1)
    combined_df_elec['Total_Future_Eligible_Courses'] = combined_df_elec['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_elec['Future_Eligible_Courses_List_Special'] = combined_df_elec.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_elec, conditions_elec, is_eligible_special_elec_), axis=1)
    combined_df_elec['Total_Future_Eligible_Courses_Special'] = combined_df_elec['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_elec["Future_Eligible_Courses"] = combined_df_elec["Future_Eligible_Courses_List"] + combined_df_elec["Future_Eligible_Courses_List_Special"]
    combined_df_elec['Course_Score'] = combined_df_elec['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_elec = combined_df_elec.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_elec = combined_df_elec.merge(recommended_courses_elec, on=['Student_ID', 'Semester'])

    return combined_df_elec,combined_elec_list,recommended_courses_elec

def process_data_comp(cea_data, comp_data, major_data):
    # Filtering and Sorting Data
    comp_data = cea_data[cea_data['Major'] == 'Computer Engineering']
    comp_data = comp_data.sort_values(by=['Student_ID', 'Semester'])
    
    # Extracting specific sheets and filtering based on 'COMSCIENCE'
    cea_list = major_data["CEA_list"]
    comp_list = cea_list[cea_list["Major"] == "COMPENG"]

    cea_special_cases = major_data["CEA_Special_Cases"]
    comp_special_cases = cea_special_cases[cea_special_cases["Major"] == "COMPENG"]

    cea_co = major_data["CEA_CO"]
    comp_co = cea_co[cea_co["Major"] == "COMPENG"]

    # Process 'REQUISITES_LIST'
    comp_co = comp_co.copy()
    comp_co.loc[:, 'REQUISITES_LIST'] = comp_co['REQUISITES_LIST'].apply(ast.literal_eval)

    # Combining DataFrames
    courses_comp = pd.concat([comp_list[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           comp_special_cases[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]],
                           comp_co[["Course_ID","AREA_OF_STUDY","COURSE_OF_STUDY"]]],
                          axis=0, ignore_index=True)
    courses_comp = courses_comp.drop_duplicates()

    # Grouping data by Student_ID and Semester
    grouped_data_comp = comp_data.groupby(['Student_ID', 'Semester'])['Course_ID'].apply(list).reset_index()

    # Creating Prerequisites Dictionary
    prerequisites_comp = comp_list.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    prerequisites_special_comp = comp_special_cases.set_index('Course_ID')['REQUISITES_LIST'].apply(ast.literal_eval).to_dict()
    conditions_comp = comp_special_cases.set_index('Course_ID')['Condition'].to_dict()

    # Processing for Standard Eligibility
    final_results_comp = []

    for student_id, group in comp_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_comp.keys() if is_eligible(course, cumulative_courses, prerequisites_comp) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_comp.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': semester_group['Major'].iloc[0],
                'College': semester_group['College'].iloc[0],
                'Program': semester_group['Program'].iloc[0],
                'Passed Credits': semester_group['Passed Credits'].iloc[0],
                'Student_Level': semester_group['Student_Level'].iloc[0],
                'Eligible_Courses': not_taken_courses
            })

    final_results_df_comp = pd.DataFrame(final_results_comp)

    # Processing for Special Eligibility
    final_results_special_comp = []

    for student_id, group in comp_data.groupby('Student_ID'):
        cumulative_courses = set()
        for semester, semester_group in group.groupby('Semester'):
            student_info = semester_group.iloc[0]
            taken_courses = set(semester_group['Course_ID'].tolist())
            
            cumulative_courses.update(taken_courses)
            
            eligible_courses = {course for course in prerequisites_special_comp.keys() if is_eligible_special_comp(course, cumulative_courses, student_info,prerequisites_special_comp,conditions_comp) and course not in cumulative_courses}
            
            not_taken_courses = [course for course in eligible_courses if course not in taken_courses]
            
            final_results_special_comp.append({
                'Student_ID': student_id,
                'Semester': semester,
                'Major': student_info['Major'],
                'College': student_info['College'],
                'Program': student_info['Program'],
                'Passed Credits': student_info['Passed Credits'],
                'Student_Level': student_info['Student_Level'],
                'Eligible_Courses': not_taken_courses
            })

    final_results_special_df_comp = pd.DataFrame(final_results_special_comp)

    # Combine Eligible Courses from Both DataFrames
    combined_comp_list = combine_eligible_courses(final_results_df_comp, final_results_special_df_comp)

    # Find Course Combinations for Co-requisites
    combined_comp_list = combined_comp_list.apply(create_combined_courses, axis=1, co=comp_co)

    # Exploding and Mapping Course Details
    combined_df_comp = combined_comp_list.explode("Eligible_Courses_CO")
    #combined_df_comp = combined_df_comp.dropna(subset=["Eligible_Courses_CO"])
    combined_df_comp["AREA_OF_STUDY"] = combined_df_comp['Eligible_Courses_CO'].map(courses_comp.set_index('Course_ID')['AREA_OF_STUDY'])
    combined_df_comp["COURSE_OF_STUDY"] = combined_df_comp['Eligible_Courses_CO'].map(courses_comp.set_index('Course_ID')['COURSE_OF_STUDY'])
    combined_df_comp['Eligible_Courses_CO'] = combined_df_comp['Eligible_Courses_CO'].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    # Find Additional Eligibilities
    combined_df_comp['Future_Eligible_Courses_List'] = combined_df_comp.apply(lambda row: find_additional_eligibilities(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), prerequisites_comp), axis=1)
    combined_df_comp['Total_Future_Eligible_Courses'] = combined_df_comp['Future_Eligible_Courses_List'].apply(len)

    # Special Additional Eligibilities
    combined_df_comp['Future_Eligible_Courses_List_Special'] = combined_df_comp.apply(lambda row: find_additional_eligibilities_special(row['Eligible_Courses_CO'], set(row['Eligible_Courses_CO']), row, prerequisites_special_comp, conditions_comp, is_eligible_special_comp_), axis=1)
    combined_df_comp['Total_Future_Eligible_Courses_Special'] = combined_df_comp['Future_Eligible_Courses_List_Special'].apply(len)

    # Combine Future Eligible Courses
    combined_df_comp["Future_Eligible_Courses"] = combined_df_comp["Future_Eligible_Courses_List"] + combined_df_comp["Future_Eligible_Courses_List_Special"]
    combined_df_comp['Course_Score'] = combined_df_comp['Future_Eligible_Courses'].apply(len)

    # Find Best Courses
    recommended_courses_comp = combined_df_comp.groupby(['Student_ID', 'Semester']).apply(lambda group: pd.Series({'Recommended_Courses': find_best_courses(group)})).reset_index()
    combined_df_comp = combined_df_comp.merge(recommended_courses_comp, on=['Student_ID', 'Semester'])

    return combined_df_comp,combined_comp_list,recommended_courses_comp

major_processing_functions = {
    "Accounting": process_data_acc,
    "International Business": process_data_ib,
    "Mgmt & Organizational Behavior": process_data_mob,
    "Management Information Systems": process_data_mis,
    "Marketing": process_data_mrkt,
    "Finance": process_data_fin,
    "Computer Science": process_data_cs,
    "Digital Media Production": process_data_dmp,
    "Eng- Linguistics - Translation": process_data_eng_lin,
    "English Education": process_data_eng_edu,
    "English Literature": process_data_eng_lit,
    "Public relations & Advertising": process_data_pr,
    "Visual Communication": process_data_vc,
    "Engineering Management": process_data_mgmt,
    "Electrical Engineering": process_data_elec,
    "Computer Engineering": process_data_comp
}


if navigation == "User Guide":
    st.title("User Guide")
    st.write("Welcome to the User Guide. Please choose an option below to learn more:")
    
    guide_option = st.selectbox("Choose an option:", ["Please select the required page!","Course Eligibility and Recommendation System", "Quick Check"])
    
    
    if guide_option == "Please select the required page!":
        st.info("No Page selected")

    if guide_option == "Course Eligibility and Recommendation System":
        with st.expander("Steps for Course Eligibility and Recommendation System"):
            st.markdown("""
            ### Steps for "Course Eligibility and Recommendation System"
            1. **Select Major**: Choose the student's major from the dropdown.
            2. **Download Sample Data**: Download sample student data to understand the format.
            3. **Upload Student Data**: Upload the student data in CSV format.
            4. **View and Download Data**: Select which Data to view and download the data if needed.
                - Eligible Courses
                - Recommended Courses
                - Combined Data
            5. **Process Data**: Wait for the data processing to complete.
            """)
        
    elif guide_option == "Quick Check":
        with st.expander("Steps for Quick Check"):
            st.markdown("""
            ### Steps for "Quick Check"
            1. **Enter Number of Semesters**: Specify the number of semesters to add.
            2. **Enter Student Information**: For each semester, enter student ID, semester, college, passed credits, student level, program, major, and course IDs.
            3. **Process Data**: Click the "Process Manual Input Data" button.
            4. **View and Download Data**: Select which Data to view and download the data if needed.
                - Eligible Courses
                - Recommended Courses
                - Combined Data
            """)


elif navigation == "Course Eligibility and Recommendation System":
    st.title("Course Eligibility and Recommendation System")

    try:
        major_data = pd.read_excel("Majors.xlsx", sheet_name=None)
    except Exception as e:
        st.error(f"Error loading Major Sheet: {e}")

    st.header("Step 1: Select College & Major")
    selected_college = st.selectbox("Select College:", ["Please Select The Required College!","CBA", "CAS", "CEA"])

    if selected_college == "Please Select The Required College!":
        st.warning("No College Selected!")
        majors = ["No College Selected!"]
    elif selected_college == "CBA":
        majors = ["Accounting", "International Business", "Mgmt & Organizational Behavior", "Management Information Systems", "Marketing", "Finance"]
    elif selected_college == "CAS":
        majors = ["Computer Science", "Digital Media Production", "Eng- Linguistics - Translation", "English Education", "English Literature", "Public relations & Advertising", "Visual Communication"]
    elif selected_college == "CEA":
        majors = ["Electrical Engineering", "Computer Engineering", "Engineering Management"]

    selected_major = st.multiselect("Select Major:", majors)

    st.header("Step 2: Load Student Data")
    st.info("Please download the sample student data to understand the required format.")
    sample_data = create_sample_data()
    st.download_button(
        label="Download Sample Data",
        data=sample_data.to_csv(index=False),
        file_name='sample_student_data.csv',
        mime='text/csv',
    )
    student_file = st.file_uploader("Upload the Student Data (CSV)", type=["csv"])

    if student_file and selected_college != "Please Select The Required College!" and selected_major:
        # Reading student data
        try:
            data = pd.read_csv(student_file,dtype=str)
            data["Student_Level"] = data["Student_Level"].astype(int)
            data["Passed Credits"] = data["Passed Credits"].astype(int) 
            st.success("Student Data loaded successfully!")

            # Check for major mismatch
            majors_in_data = data['Major'].unique()
            college_major_map = {
                "CBA": ["Accounting", "International Business", "Mgmt & Organizational Behavior", "Management Information Systems", "Marketing", "Finance"],
                "CAS": ["Computer Science", "Digital Media Production", "Eng- Linguistics - Translation", "English Education", "English Literature", "Public relations & Advertising", "Visual Communication"],
                "CEA": ["Electrical Engineering", "Computer Engineering", "Engineering Management"]
            }

            valid_majors = college_major_map[selected_college]
            invalid_majors = [major for major in majors_in_data if major not in valid_majors]

            if invalid_majors:
                st.error(f"The data contains majors that do not match the selected college: {invalid_majors}")
            else:
                # Check if selected majors are in the data
                missing_majors = [major for major in selected_major if major not in majors_in_data]

                if missing_majors:
                    st.error(f"The selected majors are not present in the loaded data: {missing_majors}")
                else:
                    section = st.selectbox("Select Data to Display", ["None", "Eligible Courses", "Recommended Courses", "Combined Data"])

                    if section != "None":
                        combined_df_list = []
                        combined_list_list = []
                        recommended_courses_list = []

                        for major in selected_major:
                            st.write(f"Processing data for major: {major}")
                            major_data_subset = data[data['Major'] == major]

                            process_function = major_processing_functions.get(major)

                            if process_function:
                                with st.spinner(f"Processing data for major: {major}..."):
                                    combined_df, combined_list, recommended_courses = process_function(major_data_subset, major_data_subset, major_data)

                                combined_df_list.append(combined_df)
                                combined_list_list.append(combined_list)
                                recommended_courses_list.append(recommended_courses)
                            else:
                                st.error(f"No processing function found for major: {major}")

                        # Combine the processed dataframes for all majors
                        if combined_df_list:
                            combined_df = pd.concat(combined_df_list, ignore_index=True)
                            combined_list = pd.concat(combined_list_list, ignore_index=True)
                            recommended_courses = pd.concat(recommended_courses_list, ignore_index=True)

                            st.success("Data processed successfully for all majors!")

                            if section == "Eligible Courses":
                                st.header("Eligible Courses Data")
                                st.dataframe(combined_list)

                                # Download the DataFrame as CSV
                                st.header("Download Eligible Courses Data")
                                csv = combined_list.to_csv(index=False)
                                st.download_button(
                                    label="Download Eligible Courses data as CSV",
                                    data=csv,
                                    file_name='combined_list.csv',
                                    mime='text/csv',
                                )
                            elif section == "Recommended Courses":
                                st.header("Recommended Courses Data")
                                st.dataframe(recommended_courses)

                                # Download the DataFrame as CSV
                                st.header("Download Recommended Courses Data")
                                csv = recommended_courses.to_csv(index=False)
                                st.download_button(
                                    label="Download recommended courses data as CSV",
                                    data=csv,
                                    file_name='recommended_courses.csv',
                                    mime='text/csv',
                                )
                            elif section == "Combined Data":
                                st.header("Combined Data")
                                st.dataframe(combined_df)

                                # Download the DataFrame as CSV
                                st.header("Download Combined Data")
                                csv = combined_df.to_csv(index=False)
                                st.download_button(
                                    label="Download data as CSV",
                                    data=csv,
                                    file_name='combined_df.csv',
                                    mime='text/csv',
                                )
                    else:
                        st.warning("Please Choose the required Data!")
        except Exception as e:
            st.error(f"Error loading student data: {e}")

if navigation == "Quick Check":
    st.title("Course Eligibility and Recommendation System")

    try:
        major_data = pd.read_excel("Majors.xlsx", sheet_name=None)
    except Exception as e:
        st.error(f"Error loading Major Sheet: {e}")
    
    try:
        course_list_df = pd.read_excel("Course_ID.xlsx")
        course_list = course_list_df['Course_ID'].tolist()
    except Exception as e:
        st.error(f"Error loading course list: {e}")
    
    num_semesters = st.number_input("Number of Semesters to Add:", min_value=1, value=1, step=1)
    student_info_list = []

    for i in range(num_semesters):
        st.subheader(f"Semester {i + 1} Information")

        student_id = st.text_input(f"Student ID (Semester {i + 1}):")
        semester = st.text_input(f"Semester (Semester {i + 1}):")
        college = st.selectbox(f"College (Semester {i + 1}):", ["Please Select The Required College!", "CBA", "CAS", "CEA"], key=f"college_{i}")

        if college == "Please Select The Required College!":
            st.warning("No College Selected!")
            programs = ["No College Selected!"]
            majors = ["No Program Selected!"]
        elif college == "CBA":
            programs = ["Please Choose the required program!", "Accounting", "Finance", "Marketing", "Management Information Systems", "Business Administration"]
        elif college == "CAS":
            programs = ["Please Choose the required program!", "Computer Science", "English", "Mass Communication"]
        elif college == "CEA":
            programs = ["Please Choose the required program!", "Computer Engineering", "Electrical Engineering", "Engineering Management"]

        program = st.selectbox(f"Program (Semester {i + 1}):", programs, key=f"program_{i}")

        if college == "CBA":
            if program == "Please Choose the required program!":
                st.warning("Please Choose the required program!")
                majors = ["No Program Selected!"]
            elif program == "Accounting":
                majors = ["Accounting"]
            elif program == "Finance":
                majors = ["Finance"]
            elif program == "Marketing":
                majors = ["Marketing"]
            elif program == "Management Information Systems":
                majors = ["Management Information Systems"]
            elif program == "Business Administration":
                majors = ["Mgmt & Organizational Behavior", "International Business"]
        elif college == "CAS":
            if program == "Please Choose the required program!":
                st.warning("Please Choose the required program!")
                majors = ["No Program Selected!"]
            elif program == "Computer Science":
                majors = ["Computer Science"]
            elif program == "English":
                majors = ["English Education", "Eng- Linguistics - Translation", "English Literature"]
            elif program == "Mass Communication":
                majors = ["Public relations & Advertising", "Digital Media Production", "Visual Communication"]
        elif college == "CEA":
            if program == "Please Choose the required program!":
                st.warning("Please Choose the required program!")
                majors = ["No Program Selected!"]
            elif program == "Computer Engineering":
                majors = ["Computer Engineering"]
            elif program == "Electrical Engineering":
                majors = ["Electrical Engineering"]
            elif program == "Engineering Management":
                majors = ["Engineering Management"]

        major = st.selectbox(f"Major (Semester {i + 1}):", majors, key=f"major_{i}")
        passed_credits = st.number_input(f"Passed Credits (Semester {i + 1}):", value=0, min_value=0)
        student_level = st.selectbox(f"Student Level (Semester {i + 1}):", ["Freshman", "Sophomore", "Junior", "Senior"])

        # Ensure that course IDs are selected
        course_id = st.multiselect(f"Course ID (Semester {i + 1}):", course_list, key=f"course_id_{i}")
        
        if not course_id:
            st.warning("Please select at least one Course ID.")

        student_info = {
            'Student_ID': student_id,
            'Semester': semester,
            'College': college,
            'Passed Credits': passed_credits,
            'Student_Level': student_level,
            'Program': program,
            'Major': major,
            'Course_ID': course_id
        }
        student_info_list.append(student_info)

    if st.checkbox("Process Manual Input Data"):
        valid_input = True
        # Validate input
        for info in student_info_list:
            if info['College'] == "Please Select The Required College!" or info['Program'] == "Please Choose the required program!" or not info['Course_ID']:
                valid_input = False

        if valid_input:
            combined_df_list = []
            combined_list_list = []
            recommended_courses_list = []

            # Combine all student info into a single DataFrame
            combined_data = pd.DataFrame(student_info_list)
            combined_data = combined_data.explode("Course_ID")
            combined_data["College"] = combined_data["College"].replace("CEA","COE")
            combined_data["Student_Level"] = combined_data["Student_Level"].replace({"Freshman": 1, "Sophomore": 2, "Junior": 3, "Senior": 4})

            st.success("Manual Data entered successfully!")
            st.table(combined_data)

            for major in combined_data['Major'].unique():
                process_function = major_processing_functions.get(major)
                if process_function:
                    major_data_ = combined_data[combined_data['Major'] == major]
                    combined_df, combined_list, recommended_courses = process_function(major_data_, major_data_, major_data)
                    combined_df_list.append(combined_df)
                    combined_list_list.append(combined_list)
                    recommended_courses_list.append(recommended_courses)
                    # Combine the processed dataframes for different majors
                    combined_df = pd.concat(combined_df_list, ignore_index=True)
                    combined_list = pd.concat(combined_list_list, ignore_index=True)
                    recommended_courses = pd.concat(recommended_courses_list, ignore_index=True)

                    st.success("Data processed successfully!")
                    section = st.selectbox("Select Data to Display", ["None", "Eligible Courses", "Recommended Courses", "Combined Data"])

                    if section == "None":
                        st.warning("Please Choose the required Data!")
                    elif section == "Eligible Courses":
                        st.header("Eligible Courses Data")
                        st.dataframe(combined_list)
                        
                        # Download the DataFrame as CSV
                        st.header("Download Eligible Courses Data")
                        csv = combined_list.to_csv(index=False)
                        st.download_button(
                            label="Download Eligible Courses data as CSV",
                            data=csv,
                            file_name='combined_list.csv',
                            mime='text/csv'
                        )
                    elif section == "Recommended Courses":
                        st.header("Recommended Courses Data")
                        st.table(recommended_courses)
                        
                        # Download the DataFrame as CSV
                        st.header("Download Recommended Courses Data")
                        csv = recommended_courses.to_csv(index=False)
                        st.download_button(
                            label="Download recommended courses data as CSV",
                            data=csv,
                            file_name='recommended_courses.csv',
                            mime='text/csv',
                        )
                    elif section == "Combined Data":
                        st.header("Combined Data")
                        st.table(combined_df)
                        
                        # Download the DataFrame as CSV
                        st.header("Download Combined Data")
                        csv = combined_df.to_csv(index=False)
                        st.download_button(
                            label="Download data as CSV",
                            data=csv,
                            file_name='combined_df.csv',
                            mime='text/csv',
                        )
                else:
                    st.error(f"No processing function found for major: {major}")
        else:
            st.error("Please fill in all required fields correctly before processing.")