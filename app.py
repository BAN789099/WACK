from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "wackshop_secret_key"

ADMIN_USERNAME = "WACKSHOP"
ADMIN_PASSWORD = "123456789+"
IP_LOG_FILE = "ip_log.txt"

# ตรวจสอบการล็อกอิน
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# เข้าหน้าแรก
@app.route('/')
def home():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(IP_LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"{timestamp} - {user_ip}\n")
    return render_template('index.html', ip=user_ip)

# หน้าเข้าสู่ระบบ
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
    return render_template('login.html', error=error)

# หน้าแอดมิน
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

# แสดง IP ที่เข้าใช้งาน
@app.route('/view_ips')
@login_required
def view_ips():
    try:
        with open(IP_LOG_FILE, 'r', encoding='utf-8') as f:
            logs = f.readlines()
    except FileNotFoundError:
        logs = ["ยังไม่มีผู้เข้าใช้งาน"]
    return render_template('view_ips.html', logs=logs)

# ออกจากระบบ
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
