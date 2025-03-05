import mysql.connector

class Database:
    def __init__(self, host="localhost", user="root", password="", database="quan_ly_thiet_bi"):
        """Khởi tạo kết nối đến database"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        """Kết nối đến MySQL"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor(dictionary=True)
                print("✅ Kết nối thành công đến database!")
            else:
                print("❌ Kết nối thất bại!")
        except mysql.connector.Error as err:
            print(f"❌ Lỗi kết nối: {err}")

    def execute_query(self, query, params=None):
        """Thực thi truy vấn (INSERT, UPDATE, DELETE)"""
        if self.conn is None or self.cursor is None:
            print("⚠ Lỗi: Chưa kết nối đến database!")
            return None

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount
        except mysql.connector.Error as err:
            print(f"❌ Lỗi truy vấn: {err}")
            return None

    def fetch_data(self, query, params=None):
        """Lấy dữ liệu từ database (SELECT)"""
        if self.conn is None or self.cursor is None:
            print("⚠ Lỗi: Chưa kết nối đến database!")
            return None

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"❌ Lỗi truy vấn: {err}")
            return None

    def close(self):
        """Đóng kết nối"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("🔒 Đã đóng kết nối với database.")

# Ví dụ sử dụng
if __name__ == "__main__":
    db = Database(user="root", password="")  # Xóa password nếu XAMPP không đặt mật khẩu
    db.connect()

    # Kiểm tra danh sách thiết bị
    if db.conn and db.cursor:  # Đảm bảo đã kết nối trước khi truy vấn
        devices = db.fetch_data("SELECT * FROM thiet_bi")
        print(devices)
    
    db.close()
