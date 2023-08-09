"""This Project demonstrates a Streamlit Project For Data Entry."""

import streamlit as st
import pandas as pd
import  sqlite3



# Create separate DataFrames to store employee and department data
employee_data = pd.DataFrame(columns=['Empno', 'Ename', 'Job', 'Deptno'])
department_data = pd.DataFrame(columns=['Deptno', 'Dname', 'Loc'])

# Streamlit app
def main():
    """This is a main Function."""
    st.title("Employee and Department Data Management")

    # Add navigation to different pages
    menu = ["Employee Data Entry", "Department Data Entry", "Data Visualization"]
    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Employee Data Entry":
        employee_data_entry()
    elif choice == "Department Data Entry":
        department_data_entry()
    elif choice == "Data Visualization":
        visualize_data()


# Page for entering employee data
def employee_data_entry():
    """This function takes an employee data and saves to database name data.db"""
    # Connect to the SQLite database
    conn = sqlite3.connect('./data/data.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employee (
            empno INTEGER PRIMARY KEY,
            ename TEXT,
            job TEXT,
            deptno Integer
        );
    """)

    st.header("Employee Data Entry")

    empno = st.text_input("Employee Number (Empno)")
    ename = st.text_input("Employee Name (Ename)")
    job = st.text_input("Job")
    deptno = st.text_input("Department Number (Deptno)")

    if st.button("Submit Employee Data"):
        if empno and ename and job and deptno:
            cursor.execute("INSERT INTO employee (empno, ename, job, deptno) VALUES (?, ?, ?, ?)",
                           (empno, ename, job, deptno))
            conn.commit()
            st.success("Employee data submitted successfully!")
        else:
            st.error("All fields are required!")

    conn.close()

# Page for entering department data
def department_data_entry():
    """This function takes an department data from user and saves to database named data.db"""
    conn = sqlite3.connect('./data/data.db')
    cursor = conn.cursor()

    # Create department table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS department (
            deptno INTEGER PRIMARY KEY,
            dname TEXT,
            loc TEXT
        );
    """)
    conn.commit()

    st.header("Department Data Entry")

    deptno = st.text_input("Department Number (Deptno)")
    dname = st.text_input("Department Name (Dname)")
    loc = st.text_input("Location (Loc)")

    if st.button("Submit Department Data"):
        if deptno and dname and loc:
            cursor.execute("INSERT INTO department (deptno, dname, loc) VALUES (?, ?, ?)",
                           (deptno, dname, loc))
            conn.commit()
            st.success("Department data submitted successfully!")
        else:
            st.error("All fields are required!")

    conn.close()

# Page for visualizing joined data
def visualize_data():
    """This is a function which display a data from data.dbgit """
    conn = sqlite3.connect('./data/data.db')
    cursor = conn.cursor()

    st.header("Data Visualization")

    # Query to join employee and department data based on 'Deptno'
    cursor.execute("""
        SELECT e.empno, e.ename, e.job, e.deptno, d.dname, d.loc
        FROM employee AS e
        INNER JOIN department AS d ON e.deptno = d.deptno
    """)
    joined_data = cursor.fetchall()

    if joined_data:
        df = pd.DataFrame(joined_data, columns=["Empno", "Ename", "Job", "Deptno", "Dname", "Loc"])
        st.dataframe(df)
    else:
        st.warning("No joined data available for visualization.")

    conn.close()


# Run the app
if __name__ == "__main__":
    main()
