from flask import Blueprint, session, redirect, url_for, render_template_string, request, jsonify
import requests

ketnoi_bp = Blueprint('ketnoi', __name__)

# 🔹 Cấu hình API Cloud Rạng Đông
DOMAIN = "https://rallismartv2.rangdong.com.vn"
DEVICE_LIST_URL = f"{DOMAIN}/rpc/iot-ebe/sync/list-device"
LOGIN_URL = f"{DOMAIN}/rpc/iot-ebe/account/login"

# 🔹 Tài khoản Cloud Rạng Đông
USERNAME = "0773342857"
PASSWORD = "Ngoc2403@"

# 🔹 ID nhà "Lab Đông Á"
DORMITORY_ID = "3040ad65-7c6b-4c70-b8c8-a7f9c1387e20"

# ✅ Đăng nhập để lấy token
def get_token():
    data = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(LOGIN_URL, json=data)
    if response.status_code == 200:
        return response.json().get("token")
    return None

# ✅ Lấy trạng thái thiết bị từ Cloud
def get_device_status():
    token = get_token()
    if not token:
        return "Không thể lấy trạng thái (Lỗi đăng nhập)"

    headers = {"Authorization": f"Bearer {token}", "X-DormitoryId": DORMITORY_ID}
    body = {
        "updatedAt": "1970-01-01T00:00:00.000Z",
        "skip": 0,
        "take": 1,  # Chỉ lấy trạng thái của 1 thiết bị đầu tiên
        "orderBy": "id",
        "orderType": "ASC"
    }

    response = requests.post(DEVICE_LIST_URL, headers=headers, json=body)
    if response.status_code == 200:
        devices = response.json()
        if devices:
            return "Đã kết nối!" if devices[0].get("isLightingDevice", False) else "Chưa kết nối"
        else:
            return "Không có thiết bị nào"
    
    return "Không thể lấy trạng thái"

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
            body { margin: 0; padding: 0; font-family: 'Arial', sans-serif; background: url('https://rangdong.com.vn/uploads/images/landingpage/showroom-ha-dinh/showroom-ha-dinh-3.JPG') no-repeat center center fixed; background-size: cover; color: white; text-align: center; }
            .container { background: rgba(0, 0, 0, 0.7); width: 80%; margin: 50px auto; padding: 20px; border-radius: 15px; box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.3); }
            h1 { font-size: 32px; margin-bottom: 10px; }
            .connection-box { background: rgba(255, 255, 255, 0.2); padding: 20px; border-radius: 10px; width: 300px; margin: 20px auto; text-align: center; box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.3); }
            .connection-box i { font-size: 50px; margin-bottom: 10px; }
            .status { font-size: 20px; font-weight: bold; margin-bottom: 10px; }
            .connect-btn { background: #28a745; padding: 10px 20px; border-radius: 5px; color: white; text-decoration: none; font-size: 20px; display: inline-block; cursor: pointer; transition: 0.3s; }
            .connect-btn:hover { background: #218838; }
            .control-btn { display: none; background: #007bff; padding: 10px 20px; border-radius: 5px; color: white; text-decoration: none; font-size: 20px; cursor: pointer; transition: 0.3s; }
            .control-btn:hover { background: #0056b3; }
            .logout { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: red; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-size: 13px; transition: 0.3s; }
            .logout:hover { background: darkred; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Xin chào, {{ user_name }}!</h1>
            <p>Hệ thống nhà thông minh Rạng Đông đang chờ kết nối.</p>

            <div class="connection-box">
                <i class="fas fa-wifi"></i>
                <p class="status" id="device-status">Chưa kết nối</p>
                <a href="#" class="connect-btn" id="connect-btn" onclick="connectDevice()">Kết Nối</a>
                <a href="/dieukhien" class="control-btn" id="control-btn">Điều khiển căn phòng</a>
            </div>
            <a href="#" class="logout" onclick="showLogoutModal(event)">Đăng Xuất</a>

            <script>
            function showLogoutModal(event) {
                event.preventDefault();
                alert("Bạn có chắc muốn đăng xuất không?");
                window.location.href = '{{ url_for("login.login") }}';
            }

            function connectDevice() {
                let statusText = document.getElementById('device-status');
                let connectBtn = document.getElementById('connect-btn');
                let controlBtn = document.getElementById('control-btn');

                statusText.textContent = "Đang lấy trạng thái...";

                fetch('/ketnoi/connect', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        statusText.textContent = "Đã kết nối!";
                        statusText.style.color = "lightgreen";

                        // Ẩn nút "Kết Nối" và hiển thị nút "Điều khiển căn phòng"
                        connectBtn.style.display = "none";
                        controlBtn.style.display = "inline-block";
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
        </div>
    </body>
    </html>
    '''
    return render_template_string(ketnoi_html, user_name=user_name)

@ketnoi_bp.route('/ketnoi/connect', methods=['POST'])
def connect_device():
    device_status = get_device_status()
    return jsonify({"success": True, "status": "Đã kết nối!" if "Đã kết nối!" in device_status else "Chưa kết nối"})
