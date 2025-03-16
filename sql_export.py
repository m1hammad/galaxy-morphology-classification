import pyodbc as odbc
import os
from data_import import import_target_values, clean_up
from dotenv import load_dotenv, dotenv_values

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

# here U means user-defined table or object
sql_table_target_val = '''
IF OBJECT_ID('galaxy_target_values', 'U') is NOT NULL
    DROP TABLE galaxy_target_values;
CREATE TABLE galaxy_target_values (
    GalxyID INT PRIMARY KEY,
    [Class1.1] FLOAT,
    [Class1.2] FLOAT,
    [Class1.3] FLOAT,
    [Class2.1] FLOAT,
    [Class2.2] FLOAT,
    [Class3.1] FLOAT,
    [Class3.2] FLOAT,
    [Class4.1] FLOAT,
    [Class4.2] FLOAT,
    [Class5.1] FLOAT,
    [Class5.2] FLOAT,
    [Class5.3] FLOAT,
    [Class5.4] FLOAT,
    [Class6.1] FLOAT,
    [Class6.2] FLOAT,
    [Class7.1] FLOAT,
    [Class7.2] FLOAT,
    [Class7.3] FLOAT,
    [Class8.1] FLOAT,
    [Class8.2] FLOAT,
    [Class8.3] FLOAT,
    [Class8.4] FLOAT,
    [Class8.5] FLOAT,
    [Class8.6] FLOAT,
    [Class8.7] FLOAT,
    [Class9.1] FLOAT,
    [Class9.2] FLOAT,
    [Class9.3] FLOAT,
    [Class10.1] FLOAT,
    [Class10.2] FLOAT,
    [Class10.3] FLOAT,
    [Class11.1] FLOAT,
    [Class11.2] FLOAT,
    [Class11.3] FLOAT,
    [Class11.4] FLOAT,
    [Class11.5] FLOAT,
    [Class11.6] FLOAT

);
'''

try:
    conn = odbc.connect(connection_string)
    print("Connection to SQL server successful.")

    # conn.close()

except Exception as e:
    print(f"Connection failed: {str(e)}")
    exit(1)

try:
    cursor = conn.cursor()

    # cursor.execute("SELECT @@VERSION")
    cursor.execute(sql_table_target_val)
    conn.commit()
    print("Table 'galaxy_target_values' created successfully in Azure SQL Database.")

except Exception as e:
    print("Error creating table:", e)
    cursor.close()
    conn.close()
    exit(1)



# import_target_values()

