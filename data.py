import sqlite3

connection = sqlite3.connect('chat_assistant.db')
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Employees;")
cursor.execute("DROP TABLE IF EXISTS Departments;")

cursor.execute('''
    CREATE TABLE Employees (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Department TEXT NOT NULL,
        Salary INTEGER NOT NULL,
        Hire_Date TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE Departments (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Manager TEXT NOT NULL
    );
''')

employees_data = [
    ('Alice', 'Sales', 50000, '2021-01-15'),
    ('Bob', 'Engineering', 70000, '2020-06-10'),
    ('Charlie', 'Marketing', 60000, '2022-03-20')
]

departments_data = [
    ('Sales', 'Alice'),
    ('Engineering', 'Bob'),
    ('Marketing', 'Charlie')
]

cursor.executemany('''
    INSERT INTO Employees (Name, Department, Salary, Hire_Date) 
    VALUES (?, ?, ?, ?);
''', employees_data)

cursor.executemany('''
    INSERT INTO Departments (Name, Manager) 
    VALUES (?, ?);
''', departments_data)

connection.commit()
connection.close()

print("Database initialized successfully!")