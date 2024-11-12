from airflow import DAG
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator
from pyhive import hive
import pandas as pd
import datetime

# Khai báo biến toàn cục để lưu DataFrame
extracted_df = None

default_args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2023, 1, 1),
    'retries': 1,
}

def extract_from_mysql():
    global extracted_df
    mysql_hook = MySqlHook(mysql_conn_id='mysql_default')
    sql = "SELECT id, name FROM test_table"
    extracted_df = mysql_hook.get_pandas_df(sql)

def create_hive_table():
    conn = hive.Connection(host='172.16.9.72', port=10000, username='hive')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_table (
        id INT,
        name STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    ''')
    conn.close()

def load_data_into_hive():
    global extracted_df
    if extracted_df is not None:
        # Tạo tệp tạm thời từ DataFrame
        temp_csv_path = '/tmp/test_table.csv'
        extracted_df.to_csv(temp_csv_path, index=False, header=False)

        # Nạp dữ liệu vào Hive
        conn = hive.Connection(host='172.16.9.72', port=10000, username='hive')
        cursor = conn.cursor()
        cursor.execute(f"LOAD DATA LOCAL INPATH '{temp_csv_path}' INTO TABLE my_table")
        conn.close()

dag = DAG(
    'hive_etl',
    default_args=default_args,
    description='An ETL workflow to load data into Hive',
    schedule_interval='@daily',
)

start = DummyOperator(task_id='start', dag=dag)

extract_data = PythonOperator(
    task_id='extract_from_mysql',
    python_callable=extract_from_mysql,
    dag=dag,
)

create_table = PythonOperator(
    task_id='create_hive_table',
    python_callable=create_hive_table,
    dag=dag,
)

load_data = PythonOperator(
    task_id='load_data_into_hive',
    python_callable=load_data_into_hive,
    dag=dag,
)

end = DummyOperator(task_id='end', dag=dag)

start >> extract_data >> create_table >> load_data >> end
