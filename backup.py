import os
import django
from django.db import connections
from django.conf import settings
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_ne.settings.development")  # Thay your_project_name bằng tên project của bạn
django.setup()

def backup_sqlite_to_mysql():
    try:
        # Lấy kết nối đến database SQLite
        sqlite_conn = connections['default']
        
        # Lấy kết nối đến database MySQL
        mysql_conn = connections['mysql_db']

        # Kiểm tra xem MySQL database đã tồn tại chưa, nếu chưa sẽ tạo bảng
        with mysql_conn.cursor() as mysql_cursor:
            # Lấy danh sách các bảng từ SQLite
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            sqlite_tables = sqlite_cursor.fetchall()
            
            for table in sqlite_tables:
                table_name = table[0]
                if table_name not in ['django_migrations', 'django_content_type', 'django_session', 'auth_permission', 'auth_group', 'auth_group_permissions', 'auth_user', 'auth_user_groups', 'auth_user_user_permissions', 'sqlite_sequence']:
                    
                    # Kiểm tra xem bảng đã tồn tại trong MySQL chưa
                    mysql_cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                    table_exists = mysql_cursor.fetchone()

                    if not table_exists:
                        print(f"Bảng '{table_name}' không tồn tại trong MySQL, tiến hành tạo...")
                        
                        # Lấy thông tin cột từ SQLite
                        sqlite_cursor.execute(f"PRAGMA table_info('{table_name}')")
                        columns_info = sqlite_cursor.fetchall()
                        
                        # Tạo câu lệnh CREATE TABLE cho MySQL
                        mysql_columns = []
                        for col_info in columns_info:
                            col_name = col_info[1]
                            col_type = col_info[2]
                            col_notnull = col_info[3]
                            col_pk = col_info[5]

                            mysql_type = col_type
                            if "INT" in col_type.upper():
                                mysql_type = "INT"
                            elif "TEXT" in col_type.upper():
                                mysql_type = "TEXT"
                            elif "REAL" in col_type.upper():
                                mysql_type = "DOUBLE"
                            elif "BLOB" in col_type.upper():
                                mysql_type = "BLOB"
                                
                            col_def = f"`{col_name}` {mysql_type}"
                            if col_notnull:
                                col_def += " NOT NULL"
                            if col_pk:
                                col_def += " PRIMARY KEY"

                            mysql_columns.append(col_def)

                        create_table_sql = f"CREATE TABLE `{table_name}` ({', '.join(mysql_columns)})"

                        # Tạo bảng trong MySQL
                        mysql_cursor.execute(create_table_sql)

                        print(f"Đã tạo bảng '{table_name}' trong MySQL thành công.")
                    
                    # Lấy dữ liệu từ SQLite
                    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
                    rows = sqlite_cursor.fetchall()

                    # Insert dữ liệu vào MySQL
                    if rows:
                        placeholders = ", ".join(["%s"] * len(rows[0]))
                        try:
                           mysql_cursor.executemany(f"INSERT INTO `{table_name}` VALUES ({placeholders})", rows)
                        except Exception as e:
                            print(f"Lỗi khi insert dữ liệu vào bảng {table_name}: {e}")
                            
                        print(f"Đã sao chép dữ liệu vào bảng '{table_name}' trong MySQL")
                    else:
                        print(f"Không có dữ liệu trong bảng '{table_name}' để sao chép")
                        
            mysql_conn.commit()  # Lưu thay đổi vào MySQL
            print("Sao lưu dữ liệu thành công!")

    except Exception as e:
        print(f"Lỗi khi sao lưu dữ liệu: {e}")
    finally:
        if 'sqlite_conn' in locals():
            sqlite_conn.close()
        if 'mysql_conn' in locals():
            mysql_conn.close()

if __name__ == "__main__":
    backup_sqlite_to_mysql()