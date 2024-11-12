FROM apache/airflow:2.8.2-python3.10
# Switch back to airflow user
USER airflow
COPY airflow.cfg /opt/airflow/
# COPY user_auth.py /opt/airflow/
# COPY webserver_config.py /opt/airflow/webserver_config.py
# COPY airflow.cfg /opt/airflow/

RUN pip install pyhive 
RUN pip install thrift
RUN pip install thrift_sasl 
USER airflow
RUN pip install hdfs