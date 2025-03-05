from flask import Flask
from login import login_bp  
from ketnoi import ketnoi_bp  
from trangchu import trangchu_bp  
from dieukhien import dieukhien_bp  # Import blueprint từ dieukhien.py
from dieukhien2 import dieukhien2_bp
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Đăng ký blueprint
app.register_blueprint(login_bp)
app.register_blueprint(ketnoi_bp)
app.register_blueprint(trangchu_bp)
app.register_blueprint(dieukhien_bp)  # Đăng ký trang điều khiển
app.register_blueprint(dieukhien2_bp)
if __name__ == '__main__':
    app.run(debug=True)

