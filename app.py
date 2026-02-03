import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",   # change if your password is different
        database="school_db"
    )

# ---------------- ADD STUDENT ----------------
def add_student(roll, name, cls):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (roll_no, name, class) VALUES (%s, %s, %s)",
        (int(roll), name, cls)
    )
    conn.commit()
    conn.close()

# ---------------- FETCH STUDENTS ----------------
def get_students():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

# ---------------- MARK ATTENDANCE ----------------
def mark_attendance(student_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
        (int(student_id), date.today().strftime("%Y-%m-%d"), status)
    )
    conn.commit()
    conn.close()

# ---------------- ADD MARKS ----------------
def add_marks(student_id, subject, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO marks (student_id, subject, marks) VALUES (%s, %s, %s)",
        (int(student_id), subject, int(marks))
    )
    conn.commit()
    conn.close()

# ---------------- STREAMLIT UI ----------------
st.title("📘 Student Attendance & Marks Portal")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Student", "Mark Attendance", "Add Marks", "View Reports"]
)

# ---------------- ADD STUDENT ----------------
if menu == "Add Student":
    st.subheader("Add Student")

    with st.form("student_form"):
        roll = st.number_input("Roll No", min_value=1)
        name = st.text_input("Name")
        cls = st.selectbox("Class", ["10A", "10B", "11A", "11B"])
        submit = st.form_submit_button("Add Student")

        if submit:
            add_student(roll, name, cls)
            st.success("Student added successfully")

# ---------------- MARK ATTENDANCE ----------------
elif menu == "Mark Attendance":
    st.subheader("Mark Attendance")

    students = get_students()

    if students.empty:
        st.error("No students found")
    else:
        student_name = st.selectbox("Select Student", students["name"])
        status = st.radio("Attendance Status", ["Present", "Absent"])

        student_id = int(
            students[students["name"] == student_name]["id"].values[0]
        )

        if st.button("Mark Attendance"):
            mark_attendance(student_id, status)
            st.success("Attendance marked successfully")

# ---------------- ADD MARKS ----------------
elif menu == "Add Marks":
    st.subheader("Add Marks")

    students = get_students()

    if students.empty:
        st.error("No students found")
    else:
        student_name = st.selectbox("Student", students["name"])
        subject = st.selectbox("Subject", ["Maths", "Science", "English"])
        marks = st.number_input("Marks", min_value=0, max_value=100)

        student_id = int(
            students[students["name"] == student_name]["id"].values[0]
        )

        if st.button("Add Marks"):
            add_marks(student_id, subject, marks)
            st.success("Marks added successfully")

# ---------------- VIEW REPORTS ----------------
elif menu == "View Reports":
    st.subheader("Attendance & Marks Report")

    conn = get_connection()

    attendance_df = pd.read_sql(
        """
        SELECT s.name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        """,
        conn
    )

    marks_df = pd.read_sql(
        """
        SELECT s.name, m.subject, m.marks
        FROM marks m
        JOIN students s ON m.student_id = s.id
        """,
        conn
    )

    conn.close()

    st.write("📅 Attendance History")
    st.dataframe(attendance_df)

    st.write("📊 Marks Details")
    if not marks_df.empty:
        marks_df["Result"] = marks_df["marks"].apply(
            lambda x: "Pass" if x >= 40 else "Fail"
        )
        st.dataframe(marks_df)
    else:
        st.error("No marks records found")