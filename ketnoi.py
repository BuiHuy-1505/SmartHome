from flask import Blueprint, session, redirect, url_for, render_template_string, request, jsonify
import requests

ketnoi_bp = Blueprint('ketnoi', __name__)

# Định nghĩa địa chỉ HC01 (nên lấy từ DB hoặc file cấu hình)
HC01_IP = "http://10.10.10.1"  # Có thể thay đổi sau này

@ketnoi_bp.route('/ketnoi')
def ketnoi():
    if 'ses_user' not in session:
        return redirect(url_for('login.login'))
    
    user_name = session.get('ses_name', 'Người dùng')

    ketnoi_html = '''
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kết Nối Thiết Bị</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
                background: url('https://rangdong.com.vn/uploads/images/landingpage/showroom-ha-dinh/showroom-ha-dinh-3.JPG') no-repeat center center fixed;
                background-size: cover;
                color: white;
                text-align: center;
            }
            .container {
                background: rgba(0, 0, 0, 0.7);
                width: 80%;
                margin: 50px auto;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.3);
            }
            h1 {
                font-size: 32px;
                margin-bottom: 10px;
            }
            .connection-box {
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 10px;
                width: 300px;
                margin: 20px auto;
                text-align: center;
                box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.3);
            }
            .connection-box i {
                font-size: 50px;
                margin-bottom: 10px;
            }
            .status {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .connect-btn {
                background: #28a745;
                padding: 10px 20px;
                border-radius: 5px;
                color: white;
                text-decoration: none;
                font-size: 20px;
                display: inline-block;
                cursor: pointer;
                transition: 0.3s;
            }
            .connect-btn:hover {
                background: #218838;
            }
            .logout {
                position: absolute;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: red;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                text-decoration: none;
                font-size: 13px;
                transition: 0.3s;
            }
            .logout:hover {
                background: darkred;
            }
            .modal {
                display: none; /* Ẩn modal mặc định */
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5); /* Màu nền mờ */
                overflow: auto;
                padding-top: 60px;
            }

            .modal-content {
                background-color: #e2a183;
                margin: 5% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 300px;
                text-align: center;
                border-radius: 10px;
            }

            /* Style cho nút đóng (x) */
            .close {
                color: #aaa;
                font-size: 28px;
                font-weight: bold;
                position: absolute;
                top: 10px;
                right: 25px;
                padding: 5px;
            }

            .close:hover,
            .close:focus {
                color: black;
                text-decoration: none;
                cursor: pointer;
            }

            /* Style cho các nút OK và Hủy */
            button {
                background-color: #e07b35;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                margin: 10px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background-color: #45a049;
            }

            /* Nút Hủy */
            button:nth-child(2) {
                background-color: red;
            }

            button:nth-child(2):hover {
                background-color: darkred;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Xin chào, {{ user_name }}!</h1>
            <p>Hệ thống nhà thông minh Rạng Đông đang chờ kết nối.</p>

            <div class="connection-box">
                <i class="fas fa-wifi"></i>
                <p class="status">Chưa kết nối</p>
                <a href="#" class="connect-btn" onclick="connectDevice()">Kết Nối</a>
            </div>
            <a href="#" class="logout" onclick="showLogoutModal(event)">Đăng Xuất</a>

            <!-- Modal -->
            <div id="logoutModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">&times;</span>
                <p>Bạn có chắc muốn đăng xuất không?</p>
                <button onclick="confirmLogout()">OK</button>
                <button onclick="closeModal()">Hủy</button>
            </div>
            </div>
            <script>
            function showLogoutModal(event) {
                // Ngừng hành động mặc định của liên kết
                event.preventDefault();

                // Hiển thị modal
                document.getElementById("logoutModal").style.display = "block";
            }

            function closeModal() {
                // Ẩn modal khi đóng
                document.getElementById("logoutModal").style.display = "none";
            }

            function confirmLogout() {
                // Nếu người dùng xác nhận đăng xuất, chuyển hướng đến trang đăng nhập
                window.location.href = '{{ url_for("login.login") }}';  // Thay đổi theo URL đăng nhập của bạn
            }
            </script>

        </div>

        <script>
            function connectDevice() {
                let statusText = document.querySelector('.status');
                let connectBtn = document.querySelector('.connect-btn');
                statusText.textContent = "Đang kết nối...";

                fetch('/ketnoi/connect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'connect' })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        statusText.textContent = "Đã kết nối!";
                        statusText.style.color = "lightgreen";
                        
                        // Ẩn nút kết nối & hiển thị nút điều khiển
                        connectBtn.style.display = "none";
                        let controlBtn = document.createElement("a");
                        controlBtn.href = "/dieukhien";
                        controlBtn.textContent = "Điều khiển căn phòng";
                        controlBtn.className = "connect-btn";
                        document.querySelector('.connection-box').appendChild(controlBtn);
                    } else {
                        statusText.textContent = "Lỗi: " + data.message;
                        statusText.style.color = "red";
                    }
                })
                .catch(() => {
                    statusText.textContent = "Lỗi kết nối!";
                    statusText.style.color = "red";
                });
            }
        </script>

    </body>
    </html>
    '''
    return render_template_string(ketnoi_html, user_name=user_name)

@ketnoi_bp.route('/ketnoi/connect', methods=['POST'])
def connect_device():
    try:
        data = request.get_json()
        if not data or data.get('action') != 'connect':
            return jsonify({"success": False, "message": "Dữ liệu không hợp lệ!"}), 400
        
        # Gửi yêu cầu đến HC01
        response = requests.post(HC01_IP, json={"action": "connect"}, timeout=5)

        if response.status_code == 200:
            return jsonify({"success": True, "message": "Kết nối thành công!"})
        else:
            return jsonify({"success": False, "message": f"Lỗi từ HC01: {response.text}"}), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({"success": False, "message": "Không thể kết nối đến HC01. Kiểm tra IP hoặc mạng."}), 500
    except requests.exceptions.Timeout:
        return jsonify({"success": False, "message": "Kết nối đến HC01 bị timeout!"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi không xác định: {str(e)}"}), 500
