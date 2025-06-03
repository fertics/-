from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# 打印调试信息
print("Debug - Environment variables:")
print(f"AMAP_KEY: {os.environ.get('AMAP_KEY')}")
print(f"AMAP_SECURITY_CODE: {os.environ.get('AMAP_SECURITY_CODE')}")
print("Debug - App config:")
print(f"AMAP_KEY: {app.config['AMAP_KEY']}")
print(f"AMAP_SECURITY_CODE: {app.config['AMAP_SECURITY_CODE']}")

# 用户登录管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 模拟用户数据库
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 模拟用户数据
users = {'admin': {'password': 'admin'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if username in users:
            flash('用户名已存在')
        elif password != confirm_password:
            flash('两次输入的密码不一致')
        elif len(password) < 6:
            flash('密码长度必须大于6位')
        else:
            users[username] = {'password': password}
            flash('注册成功，请登录')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user-interaction')
@login_required
def user_interaction():
    return render_template('user_interaction.html')

@app.route('/disaster-analysis')
@login_required
def disaster_analysis():
    return render_template('disaster_analysis.html')

@app.route('/building-safety')
@login_required
def building_safety():
    return render_template('building_safety.html')

@app.route('/disaster-comparison')
@login_required
def disaster_comparison():
    return render_template('disaster_comparison.html')

@app.route('/map')
@login_required
def map_display():
    return render_template('map_display.html')

@app.context_processor
def inject_map_key():
    return dict(
        amap_key=app.config['AMAP_KEY'],
        amap_security_code=app.config['AMAP_SECURITY_CODE']
    )

if __name__ == '__main__':
    # 开发环境配置
    if app.config['SERVER_NAME'] is None:
        app.run(debug=True, port=5002)
    # 生产环境配置
    else:
        app.run(host='0.0.0.0', port=80, debug=False) 