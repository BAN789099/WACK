from flask import Flask, request, render_template, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# แก้ path ให้อยู่ใน current folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
IP_LOG_FILE = os.path.join(BASE_DIR, 'ip_log.txt')

# สร้างโฟลเดอร์ templates ถ้ายังไม่มี
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# สร้าง template index.html
index_html = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>Wack Shop - ดัก IP</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: url('https://img2.pic.in.th/pic/imaged2cf5c332e043411.png') no-repeat center center fixed;
            background-size: cover;
            color: #fff;
            text-shadow: 1px 1px 3px #000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        h1 {
            font-size: 48px;
            margin-bottom: 10px;
        }
        p {
            font-size: 24px;
            margin-bottom: 30px;
        }
        .btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid white;
            border-radius: 10px;
            padding: 10px 20px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            transition: 0.3s;
        }
        .btn:hover {
            background: rgba(255, 255, 255, 0.5);
        }
    </style>
</head>
<body>
    <h1>Wack Shop</h1>
    <p>🎯 คุณโดนดัก IP แล้วนะ!</p>
    <p>📡 IP ของคุณคือ: <strong>{{ ip }}</strong></p>
    <a class="btn" href="{{ url_for('login') }}">เข้าสู่ระบบแอดมิน</a>
</body>
</html>
'''
with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)

# สร้าง login.html
login_html = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>เข้าสู่ระบบแอดมิน</title>
</head>
<body>
    <h2>เข้าสู่ระบบแอดมิน</h2>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username"><br><br>
        <label>Password:</label>
        <input type="password" name="password"><br><br>
        <input type="submit" value="เข้าสู่ระบบ">
    </form>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <p style="color:red;">{{ messages[0] }}</p>
        {% endif %}
    {% endwith %}
</body>
</html>
'''
with open(os.path.join(TEMPLATES_DIR, 'login.html'), 'w', encoding='utf-8') as f:
    f.write(login_html)

# สร้าง admin.html
admin_html = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>Wack Shop Admin</title>
</head>
<body>
    <h2>คุณเข้าสู่ระบบในฐานะแอดมินแล้ว</h2>
    <a href="{{ url_for('view_ips') }}">ดูรายการ IP ทั้งหมด</a><br><br>
    <a href="{{ url_for('logout') }}">ออกจากระบบ</a>
</body>
</html>
'''
with open(os.path.join(TEMPLATES_DIR, 'admin.html'), 'w', encoding='utf-8') as f:
    f.write(admin_html)

# สร้าง view_ips.html
view_ips_html = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>IP ผู้เข้าชม</title>
</head>
<body>
    <h2>รายการ IP ที่เข้ามา</h2>
    <ul>
        {% for ip in ips %}
            <li>{{ ip }}</li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('admin') }}">กลับ</a>
</body>
</html>
'''
with open(os.path.join(TEMPLATES_DIR, 'view_ips.html'), 'w', encoding='utf-8') as f:
    f.write(view_ips_html)


@app.route('/')
def home():
    user_ip = request.remote_addr
    with open(IP_LOG_FILE, 'a') as log_file:
        log_file.write(user_ip + '\n')
    return render_template('index.html', ip=user_ip)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'WACKSHOP' and password == '123456789+':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render_template('login.html')


@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    return render_template('admin.html')


@app.route('/view_ips')
def view_ips():
    if not session.get('admin'):
        return redirect(url_for('login'))
    if os.path.exists(IP_LOG_FILE):
        with open(IP_LOG_FILE, 'r') as file:
            ips = file.read().splitlines()
    else:
        ips = []
    return render_template('view_ips.html', ips=ips)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
