import mysql.connector
import pandas as pd

# Connect to MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="student"
)

cursor = connection.cursor()

# # Create a new database
# cursor.execute("CREATE DATABASE IF NOT EXISTS student")

# Use the created database
cursor.execute("USE student")

# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
# connection.close()


# Create a cursor object to execute SQL queries
cursor = connection.cursor()
# Create a new table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_details2 (
        Reg_Id VARCHAR(255),
        Name VARCHAR(255),
        SUB_CODE VARCHAR(255),
        SUB_NAME VARCHAR(255),
        Dept VARCHAR(255),
        Sem VARCHAR(255),
        Year VARCHAR(255)
    )
""")
# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

df1=pd.read_excel("N:/temp_ass/univDataBase/Elective Tracking/Elective Tracking/merged_file_updated.xlsx")
df1.shape

df1.drop(columns=['Unnamed: 0'], inplace=True)

df1=df1.rename({'Reg Id':'Reg_Id',"SUB CODE":"SUB_CODE","SUB NAME":"SUB_NAME"},axis=1)

df_dupli=df1.dropna()
df_dupli.shape

# Connect to MySQL server
host="localhost"
user="root"
password="root"
database="student"
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# # Create MySQL table based on DataFrame structure
table_name = 'student_details2'

for row1 in range(0,len(df_dupli)):
    col1=df_dupli.iloc[row1,0]
    col2=df_dupli.iloc[row1,1]
    col3=df_dupli.iloc[row1,2]
    col4=df_dupli.iloc[row1,3]
    col5=df_dupli.iloc[row1,4]
    col6=df_dupli.iloc[row1,5]
    col7=df_dupli.iloc[row1,6]
    insert_query = f"INSERT INTO {table_name} VALUES ('{col1}','{col2}','{col3}','{col4}','{col5}','{col6}','{col7}')"
    print(insert_query)
    cursor.execute(insert_query)


# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()