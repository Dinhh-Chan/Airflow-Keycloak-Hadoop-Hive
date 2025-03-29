from pyspark.sql import SparkSession

# Khởi tạo Spark Session
spark = SparkSession.builder \
    .appName("Create Tables") \
    .config("spark.sql.warehouse.dir", "/warehouse") \
    .enableHiveSupport() \
    .getOrCreate()

# Đặt log level để giảm thông báo không cần thiết
spark.sparkContext.setLogLevel("ERROR")

# Tạo database nếu chưa tồn tại
spark.sql("CREATE DATABASE IF NOT EXISTS default")
spark.sql("USE default")

# Đường dẫn đến file Parquet
parquet_path = "./warehouse/processed_data/1.parquet"

try:
    # Đọc dữ liệu Parquet
    df = spark.read.parquet(parquet_path)
    print("Đã đọc được dữ liệu Parquet")
    
    # Tạo temporary view
    df.createOrReplaceTempView("questions_temp")
    print("Đã tạo temporary view")
    
    # Xóa bảng cũ nếu tồn tại
    spark.sql("DROP TABLE IF EXISTS questions_data")
    
    # Tạo bảng
    spark.sql("""
    CREATE TABLE questions_data
    USING PARQUET
    AS SELECT * FROM questions_temp
    """)
    print("Đã tạo bảng questions_data")
    
    # Kiểm tra bảng
    tables = spark.sql("SHOW TABLES").collect()
    print("Danh sách bảng:")
    for table in tables:
        print(table[1])
    
    # Hiển thị dữ liệu mẫu
    print("\nDữ liệu mẫu:")
    spark.sql("SELECT * FROM questions_data LIMIT 5").show(truncate=False)
    
except Exception as e:
    print(f"Lỗi: {str(e)}")

# Đóng Spark Session
spark.stop()
print("Hoàn tất!")