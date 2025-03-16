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

# print(connection_string)

conn = odbc.connect(connection_string)