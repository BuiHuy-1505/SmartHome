from flask import Blueprint, render_template_string, request, redirect, url_for, session
import mysql.connector

# Tạo Blueprint cho login
login_bp = Blueprint('login', __name__)

# Kết nối cơ sở dữ liệu
def get_db_connection():
    return mysql.connector.connect(host='localhost', user='root', password='', database='quan_ly_thiet_bi')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('ten_dang_nhap', '')
        password = request.form.get('mat_khau', '')

        if not username:
            error = "Bạn chưa nhập tên tài khoản."
        elif not password:
            error = "Bạn chưa nhập mật khẩu."
        else:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM nguoi_dung WHERE ten_dang_nhap=%s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and user['mat_khau'] == password:
                session['ses_user'] = user['ten_dang_nhap']
                session['ses_name'] = user['ho_ten']
                cursor.close()
                db.close()
                return redirect(url_for('dieukhien.dieukhien'))  # Đảm bảo tên endpoint chính xác ở đây
            else:
                error = "Tên truy cập hoặc mật khẩu không chính xác."
            cursor.close()
            db.close()

    return render_template_string(login_html, error=error)

# HTML cho giao diện đăng nhập
login_html = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trang Đăng Nhập</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css">
    <style>
        body {
            background-image: url('https://rangdong.com.vn/uploads/news/nha-thong-minh/nha-thong-minh-dan-nguon-cam-xuc/nha-thong-minh-11.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Tahoma, sans-serif;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            margin: 0;
        }
        .wrap {
            background: rgba(0, 0, 0, 0.6);
            padding: 40px;  /* Tăng padding để khung cao hơn */
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.3);
            text-align: center;
            width: 350px;  /* Chiều rộng cố định */
            min-height: 500px;  /* Đảm bảo khung có chiều cao tối thiểu */
            box-sizing: border-box;
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 40px;
            color: #FFFFFF;
            text-shadow: 4px 4px 4px rgba(0, 0, 0, 0.7);
        }
        .subtitle {
            font-size: 18px;
            margin-bottom: 10px;
            color: #FFFFFF;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
            box-sizing: border-box;
        }
        input {
            background: rgba(255, 255, 255, 0.8);
            font-size: 16px;
        }
        button {
            background: #ff9800;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s ease;
        }
        button:hover {
            background: #e68900;
            transform: scale(1.05);
        }
        .back-btn {
            background: #4C3888;
            color: white;
            font-size: 12px;
            padding: 8px;
            border-radius: 5px;
            text-decoration: none;
            display: inline-block;
            margin-top: 65px;
        }
        .back-btn:hover {
            background: #45a049;
        }
    </style>

</head>
<body>

    <div class="wrap">
        <div class="title">SMARTHOME RẠNG ĐÔNG</div>
        <div class="subtitle">Đăng nhập để vào nhà</div>

        <form method="post">
            <input type="text" name="ten_dang_nhap" placeholder="Tên tài khoản" required>
            <input type="password" name="mat_khau" placeholder="Mật khẩu" required>
            <button type="submit">Đăng Nhập</button>
        </form>

        {% if error %}
            <p style="color: red; font-size: 14px; margin-top: 15px;">{{ error }}</p>
        {% endif %}

        <!-- Thêm nút quay lại trang chủ -->
        <a href="{{ url_for('trangchu.trang_chu') }}" class="back-btn">Quay lại Trang Chủ</a>
    </div>

</body>
</html>

'''

