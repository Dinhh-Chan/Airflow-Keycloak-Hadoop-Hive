from pyspark.sql import SparkSession

# Khởi tạo Spark Session
spark = SparkSession.builder \
    .appName("Create Spark SQL Table") \
    .enableHiveSupport() \
    .getOrCreate()

# Đường dẫn đến file Parquet
parquet_path = "./warehouse/processed_data"

# Đọc dữ liệu Parquet
df = spark.read.parquet(parquet_path)

# Tạo temporary view
df.createOrReplaceTempView("questions_temp")

# Tạo bảng nếu chưa tồn tại
spark.sql("""
CREATE TABLE IF NOT EXISTS questions_data
USING PARQUET
AS SELECT * FROM questions_temp
""")

# Hiển thị một số dữ liệu mẫu
spark.sql("SELECT * FROM questions_data LIMIT 5").show()

# Đóng Spark Session
spark.stop()