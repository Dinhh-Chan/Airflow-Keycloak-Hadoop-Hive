from airflow.models import Connection
from airflow import settings

def create_mysql_connection():
    # Tạo một kết nối MySQL
    conn = Connection(
        conn_id='mysql_conn',
        conn_type='mysql',
        host='localhost',
        schema='airflow_db',
        login='root',
        password='yourpassword',
        port=3306
    )
    
    session = settings.Session()
    session.add(conn)
    session.commit()
    session.close()

if __name__ == "__main__":
    create_mysql_connection()
