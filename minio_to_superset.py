import pandas as pd
import pyarrow.parquet as pq
import s3fs
from pyspark.sql import SparkSession

# Khởi tạo Spark Session (chỉ cơ bản, không cần tích hợp S3)
spark = SparkSession.builder \
    .appName("MinIO to Spark với s3fs") \
    .getOrCreate()

# Tạo kết nối S3 với s3fs
s3 = s3fs.S3FileSystem(
    endpoint_url='http://localhost:9000',
    key='minioadmin', 
    secret='minioadmin',
    use_ssl=False
)

# Thông tin về file Parquet
bucket_name = "parquet-files"
object_path = "data/data.parquet"
full_path = f"{bucket_name}/{object_path}"

# Đọc file Parquet từ MinIO
with s3.open(full_path, 'rb') as f:
    table = pq.read_table(f)
    # Chuyển đổi sang pandas DataFrame
    pandas_df = table.to_pandas()

# Chuyển đổi từ pandas DataFrame sang Spark DataFrame
spark_df = spark.createDataFrame(pandas_df)

# Hiển thị kết quả
print("Schema:")
spark_df.printSchema()

print("Dữ liệu mẫu:")
spark_df.show(5)

# Lưu kết quả vào warehouse (ví dụ: folder local)
warehouse_path = "warehouse/processed_data"
spark_df.write.mode("overwrite").parquet(warehouse_path)

print(f"Đã lưu dữ liệu vào: {warehouse_path}")

# Đóng Spark Session
spark.stop()