import duckdb

# Kết nối đến DuckDB (sẽ tạo file nếu chưa tồn tại)
conn = duckdb.connect('warehouse/duck.db')

# Tạo view cho file Parquet
conn.execute("""
    CREATE OR REPLACE VIEW questions_data AS
    SELECT * FROM read_parquet('warehouse/processed_data/*.parquet');
""")

# Kiểm tra dữ liệu
result = conn.execute("SELECT * FROM questions_data LIMIT 5").fetchall()
print("Sample data:")
for row in result:
    print(row)

# Hiển thị danh sách các view
views = conn.execute("SHOW TABLES").fetchall()
print("\nAvailable views:")
for view in views:
    print(view[0])

# Đóng kết nối
conn.close()

print("\nView đã được tạo thành công. Bạn có thể kết nối Superset với DuckDB tại warehouse/duck.db")