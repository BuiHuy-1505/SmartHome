import paho.mqtt.client as mqtt
import logging
from flask import Blueprint, session, redirect, url_for, render_template_string, request, jsonify

dieukhien2_bp = Blueprint('dieukhien2', __name__)

# Cấu hình MQTT
MQTT_BROKER = "10.10.10.1"
MQTT_PORT = 1883
MQTT_TOPIC_LIGHT1 = "rd-hc01/light1"
MQTT_TOPIC_LIGHT2 = "rd-hc01/light2"

# Tạo MQTT client
mqtt_client = mqtt.Client()
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    logging.error(f"Lỗi MQTT: {e}")

# Hàm gửi lệnh MQTT
def send_mqtt_command(topic, message):
    try:
        mqtt_client.publish(topic, message)
        return True
    except Exception as e:
        logging.error(f"Lỗi MQTT: {e}")
        return False

@dieukhien2_bp.route('/dieukhien2')
def dieukhien2():
    if 'ses_user' not in session:
        return redirect(url_for('login.login'))

    user_name = session.get('ses_name', 'Người dùng')

    dieukhien2_html = '''
    <!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Điều Khiển Căn Phòng</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }
        body {
            background: url('https://gitiho.com/caches/p_medium_large//uploads/315313/images/image_hinh-nen-powerpoint-tin-hoc-6.jpg') no-repeat center center fixed;
            background-size: cover;
            color: white;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh; /* Cho phép dài ra nếu có thêm nội dung */
            padding: 20px;
        }

        .wrapper {
            width: 90%;
            max-width: 800px;
            flex-grow: 1; /* Để wrapper mở rộng nếu cần thiết */
        }

        .container {
            position: absolute;
            top: 20px; /* Đẩy lên sát mép trên */
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 800px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 12px;
        }
        .device-container {
            display: flex;
            justify-content: center; /* Căn giữa cảm biến */
            gap: 80px; /* Tăng khoảng cách giữa hai cảm biến */
            margin-top: 100px;
        }

        .device {
            width: 80%; /* Tăng thêm chiều rộng */
            max-width: 700px; /* Giữ kích thước hợp lý trên màn hình lớn */
            height: 300px; /* Giữ nguyên chiều cao */
            background: rgba(0, 0, 0, 0.6);
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .light-wrapper img {
            width: 100%;
            height: 220px; /* Giới hạn chiều cao ảnh */
            object-fit: cover; /* Cắt ảnh nếu quá lớn */
            border-radius: 8px;
        }
        
        /* Popup */
        .popup-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(30, 144, 255, 0.6); /* Xanh dương nhạt với độ mờ 60% */
            display: none;
            justify-content: center;
            align-items: center;
            transition: opacity 0.3s ease-in-out;
        }
        .popup-content {
            background:rgb(238, 240, 245); /* Xanh đậm hơn */
            width: 450px; /* Tăng độ rộng */
            height: 300px; /* Tăng nhẹ chiều cao */
            display: flex;
            flex-direction: column;
            align-items: center;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5); /* Tăng độ đậm của viền */
            position: relative;
            transform: scale(0.8);
            transition: transform 0.3s ease-in-out;
            padding: 25px; /* Tăng padding để nội dung thoáng hơn */
            color: white;
        }
        .popup-overlay.active { opacity: 1; }
        .popup-overlay.active .popup-content { transform: scale(1); }

        .popup-title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }
        .rectangle {
            width: 220px;
            height: 110px;
            background: linear-gradient(145deg, #e0e0e0, #ffffff);
            border: 2px solid #ddd;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 12px;
            position: relative;
            box-shadow: inset 3px 3px 6px rgba(0, 0, 0, 0.2);
        }
        .circle {
            width: 40px;
            height: 40px;
            background: #3498db;
            border-radius: 50%;
            position: absolute;
            transition: all 0.2s;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            cursor: pointer;
        }
        .circle:hover { transform: scale(1.2); opacity: 0.8; }
        
        .top-left { top: -20px; left: -20px; background: #e74c3c; }
        .top-right { top: -20px; right: -20px; background: #2ecc71; }
        .bottom-left { bottom: -20px; left: -20px; background: #f1c40f; }
        .bottom-right { bottom: -20px; right: -20px; background: #9b59b6; }

        .close-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #ff4d4d;
            color: white;
            border: none;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
        }
        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            width: 10%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 20px;
        }

        .menu-title {
            font-size: 22px; /* To hơn */
            font-weight: bold; /* Đậm hơn */
            color: white;
            margin-bottom: 65px; /* Tạo khoảng cách với các menu bên dưới */
            text-align: center;
        }

        .sidebar a {
            color: white;
            text-decoration: none;
            padding: 12px;
            display: block;
            width: 100%;
            text-align: center;
            font-size: 18px; /* Nhỏ hơn tiêu đề */
            font-weight: normal; /* Không đậm bằng tiêu đề */
            transition: background 0.3s;
        }

        .sidebar a:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        .sidebar .back {
            display: block;
            position: absolute;
            bottom: 10px; /* Căn sát đáy sidebar */
            left: 50%; 
            transform: translateX(-50%); /* Căn giữa theo chiều ngang */
            padding: 5px 10px;
            font-size: 14px;
            color: white;
            text-align: center;
            text-decoration: none;
            border: 1px solid white;
            border-radius: 3px;
            background: rgba(0, 0, 0, 0.5);
            font-weight: bold;
            transition: background 0.3s ease;
            width: 80%; /* Giúp nút không quá rộng */
        }

        .sidebar .back:hover {
            background: rgba(255, 255, 255, 0.2);
        } 
        /* Popup Rèm */
    
html, body {
    height: 100%;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
}

.wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center; /* Giúp căn giữa nội dung nếu trang ít dữ liệu */
    width: 100%;
}
.main-footer {
    position: relative; 
    width: 1188px; 
    text-align: right;
    font-size: 16px;
    color: #fff;
    background: rgba(0, 0, 0, 0.6);
    padding: 15px;
    margin: 0; /* Loại bỏ khoảng cách thừa */
    left: 65px; 
    box-sizing: border-box; 
}

    </style>
</head>
<body>
    <div class="sidebar">
        <h2 class="menu-title">Menu tùy chọn</h2>
        <a href="/dieukhien">🔹 Công tắc đèn, rèm cửa</a>
        <a href="/dieukhien2">🔹 Các cảm biến</a>
        <a href="/ketnoi" class="back" >🔙 Quay lại</a>
    </div>
    
    <div class="wrapper">
        <div class="container">
            <h1>Xin chào, {{ user_name }}! 👋</h1>
            <p>Điều khiển thiết bị trong căn phòng</p>
        </div>
        <div class="device-container">
            <div class="device" onclick="openPopup('Đèn 001')">
                <h2>Cảm biến khói</h2>
                <div class="light-wrapper">
                    <img src="https://rangdong.com.vn/uploads/product/Smart/CB11.SM.WF/CB11.SM.WF-1.jpg">
                </div>
            </div>
            <div class="device" onclick="openPopup('Đèn 002')">
                <h2>Cảm biến cửa </h2>
                <div class="light-wrapper">
                    <img src="https://rangdong.com.vn/uploads/product/Smart/CB16.DO.BLE/CB16.DO.BLE-1.jpg">
                </div>
            </div>
        </div>
    </div>
    <!-- Popup -->
    <div id="popup" class="popup-overlay">
        <div class="popup-content">
            <button class="close-btn" onclick="closePopup()">×</button>
            
        </div>
    </div>

   <script>
    function openPopup(deviceName) {
        if (deviceName === 'curtain-popup') {
            openCurtainPopup();
            return;
        }
        document.getElementById("popup").style.display = "flex";
        document.querySelector(".popup-title").textContent = "Tùy Chọn " + deviceName;
        setTimeout(() => document.getElementById("popup").classList.add("active"), 10);
    }

    function closePopup() {
        document.getElementById("popup").classList.remove("active");
        setTimeout(() => document.getElementById("popup").style.display = "none", 300);
    }

    // Đóng popup khi bấm ra ngoài
    document.getElementById("popup").addEventListener("click", function(event) {
        if (event.target === this) {
            closePopup();
        }
    });

    document.getElementById("curtain-popup").addEventListener("click", function(event) {
        if (event.target === this) {
            closeCurtainPopup();
        }
    });
</script>
<footer class="main-footer">
    Liên hệ khi có sự cố: <b>09xxxx</b>
</footer>

</body>
</html>

    '''
    return render_template_string(dieukhien2_html, user_name=user_name)
