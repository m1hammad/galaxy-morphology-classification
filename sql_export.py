import pyodbc as odbc
import os
from data_import import import_target_values
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={os.getenv('SERVER_ADDRESS')};"
    f"Database={os.getenv('DATABASE_NAME')};"
    f"Uid={os.getenv('SQL_USERNAME')};"
    f"Pwd={os.getenv('SQL_PASSWORD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Define table name
table_name = "galaxy_target_values"

# SQL commad to create table
# Here 'U' means user defined table or object
sql_table_target_val = f'''
IF (OBJECT_ID('dbo.{table_name}', 'U') IS NOT NULL AND (SELECT COUNT(*) FROM dbo.{table_name}) > 0)
BEGIN
    PRINT 'Table exists and is not empty. Will not recreate table.';
END
ELSE
BEGIN
    IF OBJECT_ID('dbo.{table_name}', 'U') IS NOT NULL
        DROP TABLE dbo.{table_name};
    CREATE TABLE dbo.{table_name} (
        GalaxyID INT PRIMARY KEY,
        [Class1.1] FLOAT, [Class1.2] FLOAT, [Class1.3] FLOAT,
        [Class2.1] FLOAT, [Class2.2] FLOAT,
        [Class3.1] FLOAT, [Class3.2] FLOAT,
        [Class4.1] FLOAT, [Class4.2] FLOAT,
        [Class5.1] FLOAT, [Class5.2] FLOAT, [Class5.3] FLOAT, [Class5.4] FLOAT,
        [Class6.1] FLOAT, [Class6.2] FLOAT,
        [Class7.1] FLOAT, [Class7.2] FLOAT, [Class7.3] FLOAT,
        [Class8.1] FLOAT, [Class8.2] FLOAT, [Class8.3] FLOAT, [Class8.4] FLOAT, [Class8.5] FLOAT, [Class8.6] FLOAT, [Class8.7] FLOAT,
        [Class9.1] FLOAT, [Class9.2] FLOAT, [Class9.3] FLOAT,
        [Class10.1] FLOAT, [Class10.2] FLOAT, [Class10.3] FLOAT,
        [Class11.1] FLOAT, [Class11.2] FLOAT, [Class11.3] FLOAT, [Class11.4] FLOAT, [Class11.5] FLOAT, [Class11.6] FLOAT
    );
END;
'''

# Prep the csv file and create SQL command to insert data
def sql_csv_export():
    csv_path = import_target_values()
    df = pd.read_csv(csv_path)
    columns = df.columns
    #In pyodbc, the ? is used as a parameter placeholder in SQL queries. For example, if there are 3 columns, this line produces:
    placeholders = ", ".join(["?"]*len(columns))
    #Enclosing column names in square brackets is a common practice in SQL Server to handle column names that might contain spaces or special characters
    columns_formatted =  ", ".join([f"[{col}]" for col in columns])
    #converts the DataFrame into a NumPy array then then converts each row to a tuple
    #The cursor.executemany() function expects a list of tuples (each tuple corresponding to one row’s values). This conversion ensures that your data is in the correct format for bulk insertion into the SQL table.
    # data = [tuple(row) for row in df.to_numpy()]      # do not uncomment this, this is was the original slow way of exporting csv data
    sql_insert = f"INSERT INTO dbo.{table_name} ({columns_formatted}) VALUES ({placeholders})"
    # clean_up()
    # return sql_insert, data, df
    return sql_insert, df



def sql_connection(conn_string = connection_string):
    try:
        conn = odbc.connect(conn_string)
        print("Connection to SQL server successful.")
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        return conn, cursor
    except Exception as e:
        cursor.close()
        conn.close()
        return f"Connection failed: {str(e)}"
    
def sql_connection_close():
    conn, cursor = sql_connection()
    try:
        cursor.close()
        conn.close()
        print("SQL connection closed.")
    except Exception as e:
        print("Error closing connection:", e)

def sql_create_table():
    try:
        conn, cursor = sql_connection()
        cursor.execute(sql_table_target_val)
        conn.commit()
        print("Table 'galaxy_target_values' created successfully in Azure SQL Database.")

    except Exception as e:
        print("Error creating table:", e)
        cursor.close()
        conn.close()
        exit(1)




def sql_insert_csv():
    existing_id = set() #set of IDs existing in the current Database table
    conn, cursor = sql_connection()

    try:
        query, df = sql_csv_export() 

        # Get all the GalaxyIDs
        cursor.execute(f"SELECT GalaxyID FROM {table_name}") 
        rows = cursor.fetchall()
        for row in rows:
            existing_id.add(row[0])
        
        # check if the IDs in the CSV already exist in the Database
        df_new_ids = df[~df['GalaxyID'].isin(existing_id)]
        #If they do then do not update and close connection
        if df_new_ids.shape[0] == 0:
            print(f"Table {table_name} is up-to-date.")
            cursor.close()
            conn.close()
        # If they don't then 
        else:
            data = [tuple(row) for row in df_new_ids.to_numpy()]
            try:
        
                # print(query)
                cursor.executemany(query, data)
                conn.commit()
            except Exception as e:
                print(f"Error inserting CSV to DB Table: {e}")
                cursor.close()
                conn.close()
                exit(1)

    except Exception as e:
        print("Error fetching existing GalaxyIDs:", e)
        cursor.close()
        conn.close()
        exit(1)



if __name__ == "__main__":
    sql_connection()
    sql_create_table()
    sql_insert_csv()
    sql_connection_close()
