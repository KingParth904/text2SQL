# import sqlite3
# #connection
# connection = sqlite3.connect("student.db")
# #create cursor (points the databse)
# cursor = connection.cursor()
# #create table

# table_info="""
# Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
# SECTION VARCHAR(25),MARKS INT);

# """
# cursor.execute(table_info)

# cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
# cursor.execute('''Insert Into STUDENT values('Sudhanshu','Data Science','B',100)''')
# cursor.execute('''Insert Into STUDENT values('Darius','Data Science','A',86)''')
# cursor.execute('''Insert Into STUDENT values('Vikash','DEVOPS','A',50)''')
# cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')

# #display

# print("The inserted records are ")

# data = cursor.execute(''' Select * from STUDENT''')

# for row in data:
#     print(row)

# #close connection 
# connection.commit()
# connection.close ()   

import sqlite3
import pandas as pd

# Function to load CSV data into SQLite
def load_csv_to_sqlite(file_path, table_name, connection):
    df = pd.read_csv(file_path)
    df.to_sql(table_name, connection, if_exists='replace', index=False)

# Function to load Excel data into SQLite
def load_excel_to_sqlite(file_path, table_name, connection):
    df = pd.read_excel(file_path)
    df.to_sql(table_name, connection, if_exists='replace', index=False)

# Connect to SQLite database
connection = sqlite3.connect("company.db")

# Load data from CSV and Excel into the database
load_csv_to_sqlite("QVI_purchase_behaviour.csv", "PURCHASE_BEHAVIOUR", connection)
load_excel_to_sqlite("QVI_transaction_data.xlsx", "TRANSACTION_DATA", connection)

# Create a cursor to interact with the database
cursor = connection.cursor()

# Display the data in the PURCHASE_BEHAVIOUR table
print("The inserted records in the PURCHASE_BEHAVIOUR table are:")
purchase_data = cursor.execute('''SELECT * FROM PURCHASE_BEHAVIOUR''')
for row in purchase_data:
    print(row)

# Display the data in the TRANSACTION_DATA table
print("\nThe inserted records in the TRANSACTION_DATA table are:")
transaction_data = cursor.execute('''SELECT * FROM TRANSACTION_DATA''')
for row in transaction_data:
    print(row)

# Close connection
connection.commit()
connection.close()
