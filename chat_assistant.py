import sqlite3
import re
import streamlit as st
from datetime import datetime

# Streamlit page configuration
st.set_page_config(page_title="Chat Assistant", layout="wide")

# Function to execute database queries
def execute_query(query, params=()):
    with sqlite3.connect("chat_assistant.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
    return results

# Extract department from query
def extract_department(query):
    match = re.search(r"in the (\w+) department", query, re.IGNORECASE)
    return match.group(1) if match else None

# Extract date from query
def extract_date(query):
    match = re.search(r"after (\d{4}-\d{2}-\d{2})", query)
    return match.group(1) if match else None

# Validate date format
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to process the query
def process_query(query):
    if not query:
        return "No query provided."

    if "Show me all employees in the" in query:
        department = extract_department(query)
        if not department:
            return "Please specify a valid department name."
        
        sql_query = "SELECT Name FROM Employees WHERE Department = ?"
        result = execute_query(sql_query, (department,))
        
        return f"Employees in {department}: {', '.join([row[0] for row in result])}." if result else f"No employees found in {department}."

    elif "Who is the manager of the" in query:
        department = extract_department(query)
        if not department:
            return "Please specify a valid department name."

        sql_query = "SELECT Manager FROM Departments WHERE Name = ?"
        result = execute_query(sql_query, (department,))
        
        return f"The manager of {department} is {result[0][0]}." if result else "No department found with this name."

    elif "List all employees hired after" in query:
        date = extract_date(query)
        if not date or not is_valid_date(date):
            return "Invalid date format. Please use YYYY-MM-DD."

        sql_query = "SELECT Name FROM Employees WHERE Hire_Date > ?"
        result = execute_query(sql_query, (date,))
        
        return f"Employees hired after {date}: {', '.join([row[0] for row in result])}." if result else "No employees hired after this date."

    elif "Show the highest-paid employee" in query:
        sql_query = "SELECT Name, Salary, Department FROM Employees ORDER BY Salary DESC LIMIT 1"
        result = execute_query(sql_query)
        
        return f"The highest-paid employee is {result[0][0]} from {result[0][2]} with a salary of ${result[0][1]}." if result else "No employee data available."

    elif "What is the total salary expense for the" in query:
        department = extract_department(query)
        if not department:
            return "Please specify a valid department name."

        sql_query = "SELECT SUM(Salary) FROM Employees WHERE Department = ?"
        result = execute_query(sql_query, (department,))
        
        return f"The total salary expense for {department} is ${result[0][0]}." if result and result[0][0] else f"No salary data found for the {department} department."
    
    else:
        return "Sorry, I couldn't understand the query. Please try again."

# Streamlit UI
st.title("💬 Employee Chat Assistant")
st.write("Ask me about employees, departments, managers, and salaries!")

# User input
query = st.text_input("Enter your query:")

# Process query when the user enters text
if query:
    with st.spinner('Processing your query...'):
        response = process_query(query)
        st.success(response)
