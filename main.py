from sql_export import sql_connection, sql_create_table, sql_insert_csv, sql_connection_close
from blob_export import create_container, blob_upload_image
from concurrent import futures
from data_import import clean_up

training_container_id = "galaxy-zoo-training-images"
test_container_id = "galaxy-zoo-test-images"

def run_sql_pipeline():
    sql_connection()
    sql_create_table()
    sql_insert_csv()

def run_training_blob_pipeline():
    create_container(training_container_id)
    blob_upload_image(training_container_id)

def run_test_blob_pipeline():
    create_container(test_container_id)
    blob_upload_image(test_container_id)

if __name__ == "__main__":
    # Create a ThreadPoolExecutor with 3 workers
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        sql_pipeline = executor.submit(run_sql_pipeline)
        blob_training_pipeline = executor.submit(run_training_blob_pipeline)
        blob_test_pipeline = executor.submit(run_test_blob_pipeline)

        #Wait for all pipelines to complete
        futures.wait([sql_pipeline, blob_training_pipeline, blob_test_pipeline])

    print("Cleaning up local data...")
    clean_up()
    print("Local data clean complete.")
    
    sql_connection_close()

    print("SQL and Blob (training and testing) pipelines completed. Data has been populated")

### To add later, exception handling if any of the stats stop working, I have implemented exception handling in the individual files for
### all these functions. Should I add some exception handling here too? 