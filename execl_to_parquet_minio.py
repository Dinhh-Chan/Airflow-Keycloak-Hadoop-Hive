import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from minio import Minio
import io
import os

# Đọc file Excel
def excel_to_parquet(excel_file_path, parquet_file_name):
    # Đọc file Excel vào DataFrame
    df = pd.read_excel(excel_file_path)
    
    # Tạo buffer trong bộ nhớ để lưu file Parquet
    parquet_buffer = io.BytesIO()
    
    # Chuyển đổi DataFrame thành bảng Arrow
    table = pa.Table.from_pandas(df)
    
    # Ghi bảng Arrow vào buffer dưới dạng Parquet
    pq.write_table(table, parquet_buffer)
    
    # Đặt con trỏ về đầu buffer
    parquet_buffer.seek(0)
    
    return parquet_buffer

# Kết nối và upload lên MinIO
def upload_to_minio(parquet_buffer, bucket_name, object_name):
    # Thiết lập kết nối tới MinIO
    minio_client = Minio(
        "localhost:9000",  # Địa chỉ MinIO server
        access_key="minioadmin",  # Thay đổi theo cấu hình của bạn
        secret_key="minioadmin",  # Thay đổi theo cấu hình của bạn
        secure=False  # Đặt True nếu bạn sử dụng HTTPS
    )
    
    # Kiểm tra và tạo bucket nếu chưa tồn tại
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    
    # Upload file từ buffer vào MinIO
    minio_client.put_object(
        bucket_name,
        object_name,
        parquet_buffer,
        length=parquet_buffer.getbuffer().nbytes,
        content_type="application/octet-stream"
    )
    
    print(f"File đã được upload thành công đến s3://{bucket_name}/{object_name}")

if __name__ == "__main__":
    # Đường dẫn đến file Excel
    excel_file_path = "LLM HÓA HỌC CƠ SỞ .xlsx"
    
    # Tên bucket và object name trên MinIO
    bucket_name = "parquet-files"
    object_name = "data/data.parquet"
    
    # Chuyển đổi Excel thành Parquet
    parquet_buffer = excel_to_parquet(excel_file_path, object_name)
    
    # Upload lên MinIO
    upload_to_minio(parquet_buffer, bucket_name, object_name)