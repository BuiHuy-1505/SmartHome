from flask import Blueprint, render_template_string

# Tạo Blueprint cho trang chủ
trangchu_bp = Blueprint('trangchu', __name__)

@trangchu_bp.route('/')
def trang_chu():
    trangchu_html = '''
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nhà Thông Minh Rạng Đông</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <style>
            /* Thanh ngang cố định */
            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background-color: #333;
                color: white;
                z-index: 100;
            }

            .logo {
                display: flex;
                align-items: center;
                font-size: 24px;
            }

            .logo i {
                margin-right: 8px; /* Thêm khoảng cách giữa biểu tượng và chữ */
                font-size: 28px; /* Cỡ chữ icon */
            }

            .login-btn a {
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                background: #8ee663;
                border-radius: 5px;
                font-size: 18px;
            }
            .login-btn a:hover {
                background: #e68900;
            }
            body {
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
                background: url('https://hoanghamobile.com/tin-tuc/wp-content/uploads/2023/09/hinh-nen-vu-tru-12.jpg') no-repeat center center fixed;
                background-size: cover;
                color: white;
                text-align: center;
                padding-top: 60px; /* Để tránh bị che khuất bởi thanh ngang */
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
                font-size: 36px;
                margin-bottom: 10px;
            }
            .info {
                font-size: 18px;
                margin-bottom: 20px;
                line-height: 1.6;
            }
            .gallery {
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: wrap;
            }
            .gallery img {
                width: 300px;
                height: 200px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.3);
            }
            .about-us {
                background: rgba(0, 0, 0, 0.7);
                padding: 20px;
                margin-top: 40px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 20px;
                max-width: 900px;
                margin-left: auto;
                margin-right: auto;
            }
            .about-us h2 {
                font-size: 28px;
                margin-bottom: 15px;
            }
            .about-us p {
                font-size: 18px;
                line-height: 1.6;
                max-width: 400px;
            }
            .about-us img {
                width: 200px;
                height: 200px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.3);
            }
            .extra-gallery {
                margin-top: 40px;
            }
            .device-container {
                display: flex;
                flex-direction: column;
                gap: 30px;
            }
            .device-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 20px;
                margin-bottom: 30px;
                background: #5ec1ff;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.3);
                max-width: 1000px;
                margin-left: auto;
                margin-right: auto;
            }
            .device-item img {
                width: 200px;
                height: 200px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.3);
            }
            .device-info {
                max-width: 650px;
                font-size: 18px;
                line-height: 1.6;
            }
            .device-item.left {
                justify-content: flex-start;
                margin-left: 30px; /* Căn lề trái 15px */
                margin-right: auto; /* Để căn lề trái */
            }
            .device-item.right {
                justify-content: flex-start;
                margin-right: 30px; 
                margin-left: auto; 
            }
            .login-btn{
            margin-right: 10px;
            }
            footer {
                background-color: #02427f; /* Màu nền mới cho footer */
                color: white;
                padding: 20px 0;
                text-align: center;
                position: relative;
                bottom: 0;
                width: 100%;
            }

            .footer-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
            }

            .footer-left, .footer-right {
                flex: 1;
                padding: 0 20px;
            }

            footer p {
                margin: 5px 0;
                font-size: 16px;
            }

            footer a {
                color: #8ee663;
                text-decoration: none;
                display: flex;
                align-items: center;
                font-size: 18px;
            }

            footer a:hover {
                text-decoration: underline;
            }

            .facebook-icon {
                width: 30px;
                height: 30px;
                margin-right: 10px; /* Thêm khoảng cách giữa hình ảnh và chữ */
            }
            .about-us1{
                padding: 20px;
                margin-top: 20px;
                max-width: 900px;
                margin-left: auto;
                margin-right: auto;
                text-align: left; /* Để căn chỉnh nội dung về bên trái */
            }

            .about-us1 img{
                width: 550px;
                height: 250px;
                border-radius: 10px;
                box-shadow: none; /* Xóa bóng đổ */
            }

        </style>
    </head>
    <body>
        <div class="navbar">
            <div class="logo">
                <i class="fas fa-home"></i> Rạng Đông
            </div>
            <div class="login-btn">
                <a href="{{ url_for('login.login') }}">Đăng nhập</a>
            </div>
        </div>
        <script>
            // Khi người dùng nhấp vào logo (bao gồm cả biểu tượng và chữ)
            document.querySelector('.logo').addEventListener('click', function() {
                // Cuộn trang lên đầu
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        </script>

        <div class="container">
            <h1>Chào mừng đến với Nhà Thông Minh Rạng Đông</h1>
            <p class="info">
                Hệ thống nhà thông minh Rạng Đông mang đến sự tiện nghi, hiện đại và tiết kiệm năng lượng.<br>
                Điều khiển dễ dàng qua điện thoại, cảm biến ánh sáng, giọng nói, hẹn giờ tự động...
            </p>
            
            <div class="gallery">
                <img src="https://rangdong.com.vn/uploads/news/nha-thong-minh/he-thong-showroom/showroom-nha-thong-minh-Nha-Trang.jpg" alt="Nhà thông minh">
                <img src="https://rangdong.com.vn/uploads/news/nha-thong-minh/tien-ich-nha-thong-minh/banner-0.jpg" alt="Thiết bị thông minh">
                <img src="https://ledrangdong.com.vn/wp-content/uploads/2023/05/Mo-hinh-nha-thong-minh-Rang-dong-1.jpg" alt="Công nghệ hiện đại">
            </div>

        </div>

        <!-- Thêm phần giới thiệu về Rạng Đông -->
        <div class="about-us">
            <img src="https://cdn.haitrieu.com/wp-content/uploads/2022/08/logo-rang-dong-icon.png" alt="Logo Rạng Đông">
            <div>
                <h2>Giới thiệu về Rạng Đông</h2>
                <p>
                    Rạng Đông là một trong những thương hiệu hàng đầu tại Việt Nam trong lĩnh vực chiếu sáng và thiết bị điện. 
                    Với hơn 40 năm kinh nghiệm, chúng tôi mang đến cho người tiêu dùng các sản phẩm chiếu sáng thông minh 
                    với công nghệ hiện đại, giúp tiết kiệm năng lượng và bảo vệ môi trường.
                </p>
            </div>
        </div>

        <!-- Thêm bộ sưu tập ảnh và thông tin thiết bị -->
        <div class="extra-gallery">
            <div class="device-container">
                <div class="device-item left">
                    <img src="https://rangdong.com.vn/uploads/product/Smart/RLT02.BLE.CW-370-10W/RLT02.BLE.CW-370-10W-1.jpg" alt="Thiết bị 1">
                    <div class="device-info">
                        <a href="https://rangdong.com.vn/den-ray-led-thanh-thong-minh-pr2748.html" style="text-decoration: none; color: inherit;">
                            <h3>Đèn Ray LED thanh thông minh</h3>
                        </a>
                        <p style="font-size: 16px; line-height: 1.5; text-align: justify;">
                            Đèn Ray LED Thanh Thông Minh là loại đèn hiện đại, lắp trên thanh ray giúp di chuyển linh hoạt. 
                            Sản phẩm có thể điều khiển từ xa qua ứng dụng hoặc giọng nói, phù hợp với hệ thống smarthome. 
                            Công nghệ LED tiết kiệm điện, bền bỉ và cho ánh sáng chất lượng cao. 
                            Thích hợp cho nhà ở, showroom, cửa hàng, quán cà phê.
                        </p>    

                    </div>
                </div>

                <div class="device-item right">
                    <img src="https://rangdong.com.vn/uploads/product/LED/Led_Bluetooth/CB09.PIR.BLE/CB09.PIR.BLE-1.jpg" alt="Thiết bị 2">
                    <div class="device-info">
                        <a href="https://rangdong.com.vn/cam-bien-chuyen-dong-cb09-pir-pr2551.html" style="text-decoration: none; color: inherit;">
                        <h3>Cảm biến chuyển động CB09.PIR</h3>
                        </a>
                        <p style="font-size: 16px; line-height: 1.5; text-align: justify;">
                        Cảm biến chuyển động CB09.PIR giúp phát hiện chuyển động chính xác, tự động bật/tắt đèn và thiết bị điện.  
                        Sản phẩm sử dụng công nghệ PIR, tiết kiệm điện năng, có khả năng kết nối với các thiết bị trong hệ thống smarthome.
                        </p>
                    </div>
                </div>
                <div class="device-item left">
                    <img src="https://rangdong.com.vn/uploads/product/thiet-bi-dien/OCAT01/03.jpg" alt="Thiết bị 3">
                    <div class="device-info">
                        <a href="https://rangdong.com.vn/o-cam-am-tuong-chong-giat-pr2302.html" style="text-decoration: none; color: inherit;">
                        <h3>Ổ cắm âm tường chống giật. Model: OCAT01 1C/16A</h3>
                        </a>
                        <p style="font-size: 16px; line-height: 1.5; text-align: justify;">
                        Ổ cắm âm tường chống giật Model OCAT01 1C/16A được thiết kế an toàn, hiện đại, phù hợp cho mọi không gian. 
                        Sản phẩm có khả năng chống giật, bảo vệ người dùng trước các sự cố điện nguy hiểm. 
                        Chất liệu cao cấp, bền bỉ, đảm bảo tuổi thọ dài lâu. 
                        Thích hợp lắp đặt trong nhà ở, văn phòng, khách sạn và các công trình công cộng.
                        </p>
                    </div>
                </div>

                <div class="device-item right">
                    <img src="https://rangdong.com.vn/uploads/product/thiet-bi-dien/CT.04/RD-CT.04-1.jpg" alt="Thiết bị 4">
                    <div class="device-info">
                        <a href="https://rangdong.com.vn/cong-tac-cam-ung-4-nut-bam-pr2152.html" style="text-decoration: none; color: inherit;">
                        <h3>Công tắc cảm ứng 4 nút bấm. Model: RD-CT.04</h3>
                        </a>
                        <p style="font-size: 16px; line-height: 1.5; text-align: justify;">
                        Công tắc cảm ứng 4 nút bấm Model RD-CT.04 giúp điều khiển thiết bị điện dễ dàng và chính xác.  
                        Sản phẩm sử dụng công nghệ cảm ứng, thiết kế hiện đại, thẩm mỹ cao, dễ dàng lắp đặt trong mọi không gian.  
                        Tích hợp 4 nút bấm, hỗ trợ điều khiển nhiều thiết bị trong cùng một công tắc.  
                        Phù hợp cho nhà ở, văn phòng, khách sạn, và các công trình cao cấp.</p>
                    </div>
                </div>
            </div>
        </div>
        <!-- Thêm phần giới thiệu về Rạng Đông -->
        <div class="container">
            <div class="about-us1">
            <div style="text-align: center; margin-top: 0px;">
                <img src="https://vcdn1-kinhdoanh.vnecdn.net/2023/06/21/anh-edit-4899-1687317644.jpg?w=460&h=0&q=100&dpr=2&fit=crop&s=jLex399niiQwQ7eObHhJUg" alt="Logo Rạng Đông" style="width: 85%; height: 700; max-width: 1000px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
                
                <div style="max-width: 800px; margin: 20px auto;">
                    <h2 style="font-size: 28px; color: #ffffff; margin-bottom: 10px;">Tiết kiệm điện năng tối ưu</h2>
                    <p style="font-size: 16px; line-height: 1.8; font-family: 'Arial', sans-serif; color: #e0e0e0; text-align: justify;">
                        Hệ thống nhà thông minh Rạng Đông giúp tiết kiệm điện tối ưu nhờ vào công nghệ chiếu sáng LED tiên tiến và cảm biến thông minh. 
                        Các thiết bị tự động điều chỉnh ánh sáng và nhiệt độ theo nhu cầu sử dụng, giảm thiểu năng lượng thừa. 
                        Hệ thống điều khiển từ xa giúp người dùng dễ dàng tắt mở thiết bị khi không sử dụng. 
                        Công nghệ hẹn giờ và cảm biến chuyển động giúp tự động bật tắt đèn, tiết kiệm điện hiệu quả. 
                        Với nhà thông minh Rạng Đông, bạn không chỉ tiết kiệm chi phí mà còn góp phần bảo vệ môi trường.
                    </p>
                </div>
            </div>
            <div class="about-us1">
            <div style="text-align: center; margin-top: 0px;">
                <img src="https://i.ytimg.com/vi/XOqV4qNpqHc/maxresdefault.jpg" alt="Logo Rạng Đông" style="width: 85%; height: 700; max-width: 1000px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
                
                <div style="max-width: 800px; margin: 20px auto;">
                    <h2 style="font-size: 28px; color: #ffffff; margin-bottom: 10px;">Mang lại trải nghiệm thú vị</h2>
                    <p style="font-size: 16px; line-height: 1.8; font-family: 'Arial', sans-serif; color: #e0e0e0; text-align: justify;">
                        Nhà thông minh Rạng Đông mang lại trải nghiệm thú vị với các tính năng tự động hóa thông minh. Bạn có thể điều khiển thiết bị từ xa, tiết kiệm năng lượng hiệu quả và cải thiện chất lượng sống. Hệ thống sử dụng công nghệ chiếu sáng LED và cảm biến thông minh giúp tự động điều chỉnh ánh sáng và nhiệt độ. Điều khiển dễ dàng qua ứng dụng hoặc giọng nói. Tạo không gian sống tiện nghi, tiết kiệm và bảo vệ môi trường.
                    </p>
                </div>
            </div>
            </div>
        </div>
        </div>
        <footer>
            <div class="footer-container">
                <div class="footer-left">
                    <p><strong>Thông tin liên hệ:</strong></p>
                    <p>Email: @rangdong.com.vn</p>
                    <p>Điện thoại: +84...</p>
                    <p>Địa chỉ: </p>
                </div>
                <div class="footer-right">
                    <p><strong>Các trang thông tin của Rạng Đông</strong></p>
                    <a href="https://www.facebook.com/ralaco1961" target="_blank">
                        <img src="https://i.pinimg.com/474x/d3/66/b8/d366b8777ec11e741749f5472d1109f0.jpg" alt="Facebook" class="facebook-icon">
                        Trang Facebook Rạng Đông
                    </a>
                    <a href="https://www.tiktok.com/@rangdong.store.vn" target="_blank">
                        <img src="https://uptop.com.vn/wp-content/uploads/2021/12/logo-tik-tok.jpeg" alt="Facebook" class="facebook-icon">
                        Trang Tiktok Rạng Đông
                    </a>
                    <a href="https://rangdong.com.vn/" target="_blank">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSS_puf3pRHuZBb2zgzV9kLk1d8oMJwzx5itw&s" alt="Facebook" class="facebook-icon">
                        Websites củacủa Rạng Đông
                    </a>
                </div>
            </div>
        </footer>


    </body>
    </html>
    '''
    return render_template_string(trangchu_html)
