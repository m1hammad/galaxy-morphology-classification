import pandas as pd
from sql_export import sql_connection, sql_connection_close

sql_query = "SELECT * FROM dbo.galaxy_target_values"
conn, cursor = sql_connection()
target_df = pd.read_sql(sql_query, conn)
print(target_df)
sql_connection_close()