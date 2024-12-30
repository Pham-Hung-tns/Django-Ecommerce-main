import os
import django
from django.db import connections
from django.conf import settings
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_ne.settings.development")  # Thay your_project_name bằng tên project của bạn
django.setup()

def restore_mysql_to_sqlite():
    try:
        # Lấy kết nối đến database SQLite
        sqlite_conn = connections['default']
        
        # Lấy kết nối đến database MySQL
        mysql_conn = connections['mysql_db']

        # Kiểm tra xem MySQL database đã tồn tại chưa, nếu chưa sẽ tạo bảng
        with sqlite_conn.cursor() as sqlite_cursor, mysql_conn.cursor() as mysql_cursor:
            # Lấy danh sách các bảng từ MySQL
            mysql_cursor.execute("SHOW TABLES;")
            mysql_tables = mysql_cursor.fetchall()

            for table in mysql_tables:
                table_name = table[0]
                if table_name not in ['django_migrations', 'django_content_type', 'django_session', 'auth_permission', 'auth_group', 'auth_group_permissions', 'auth_user', 'auth_user_groups', 'auth_user_user_permissions', 'sqlite_sequence']:

                    # Kiểm tra xem bảng đã tồn tại trong SQLite chưa
                    sqlite_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
                    table_exists = sqlite_cursor.fetchone()
                    
                    if not table_exists:
                        print(f"Bảng '{table_name}' không tồn tại trong SQLite, tiến hành tạo...")
                        
                        # Lấy thông tin cột từ MySQL
                        mysql_cursor.execute(f"DESCRIBE `{table_name}`")
                        columns_info = mysql_cursor.fetchall()

                        # Tạo câu lệnh CREATE TABLE cho SQLite
                        sqlite_columns = []
                        for col_info in columns_info:
                            col_name = col_info[0]
                            col_type = col_info[1]
                            col_notnull = "NOT NULL" if "NOT NULL" in col_info[2] else ""
                            col_pk = "PRIMARY KEY" if "PRI" in col_info[3] else ""

                            sqlite_type = col_type
                            if "int" in col_type.lower():
                                sqlite_type = "INTEGER"
                            elif "text" in col_type.lower() or "char" in col_type.lower():
                                sqlite_type = "TEXT"
                            elif "double" in col_type.lower() or "decimal" in col_type.lower() or "real" in col_type.lower():
                                sqlite_type = "REAL"
                            elif "blob" in col_type.lower():
                                sqlite_type = "BLOB"

                            sqlite_columns.append(f"`{col_name}` {sqlite_type} {col_notnull} {col_pk}")
                            
                        create_table_sql = f"CREATE TABLE `{table_name}` ({', '.join(sqlite_columns)});"
                        sqlite_cursor.execute(create_table_sql)

                        print(f"Đã tạo bảng '{table_name}' trong SQLite thành công.")

                    # Lấy dữ liệu từ MySQL
                    mysql_cursor.execute(f"SELECT * FROM `{table_name}`")
                    rows = mysql_cursor.fetchall()

                    # Insert dữ liệu vào SQLite
                    if rows:
                        placeholders = ", ".join(["?"] * len(rows[0]))
                        try:
                          sqlite_cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", rows)
                        except Exception as e:
                          print(f"Lỗi khi insert dữ liệu vào bảng {table_name}: {e}")

                        print(f"Đã sao chép dữ liệu vào bảng '{table_name}' trong SQLite")
                    else:
                        print(f"Không có dữ liệu trong bảng '{table_name}' để sao chép")
                        
            sqlite_conn.commit()  # Lưu thay đổi vào SQLite
            print("Khôi phục dữ liệu từ MySQL sang SQLite thành công!")

    except Exception as e:
         print(f"Lỗi khi khôi phục dữ liệu: {e}")
    finally:
        if 'sqlite_conn' in locals():
            sqlite_conn.close()
        if 'mysql_conn' in locals():
            mysql_conn.close()

if __name__ == "__main__":
    restore_mysql_to_sqlite()