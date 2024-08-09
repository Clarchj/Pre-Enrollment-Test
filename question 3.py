import json
import sqlite3
from datetime import datetime

# Extract data from JSON file
def extract_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Transform data
def transform_data(data):
    transformed_data = []
    for employee in data:
        try:
            transformed_employee = {
                'id': int(employee['id']),
                'name': employee['name'],
                'department': employee['department'],
                'salary': int(employee['salary']),
                'join_date': datetime.strptime(employee['join_date'], '%Y-%m-%d').date()
            }
            transformed_data.append(transformed_employee)
        except (ValueError, KeyError) as e:
            print(f"Error transforming employee data: {employee}. Error: {e}")
    return transformed_data

# Load data into SQLite database
def load_data(data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary INTEGER,
        join_date DATE
    )
    ''')

    # Insert data
    for employee in data:
        try:
            cursor.execute('''
            INSERT INTO employees (id, name, department, salary, join_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                employee['id'],
                employee['name'],
                employee['department'],
                employee['salary'],
                employee['join_date']
            ))
        except sqlite3.IntegrityError as e:
            print(f"Error inserting employee {employee['id']}: {e}")

    conn.commit()
    conn.close()

# Main ETL process
def etl_process(json_file_path, db_path):
    # Extract
    raw_data = extract_data(json_file_path)
    
    # Transform
    transformed_data = transform_data(raw_data)
    
    # Load
    load_data(transformed_data, db_path)

    print("ETL process completed successfully.")

# Run the ETL process
etl_process('employees.json', 'employees.db')