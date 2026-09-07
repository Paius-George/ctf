from flask import Flask, request, render_template_string, make_response, redirect
import sqlite3
import os

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tracking (id INTEGER PRIMARY KEY, tracking_id TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    
    c.execute('DELETE FROM tracking')
    c.execute('DELETE FROM users')
    
    # Create a valid tracking ID
    c.execute("INSERT INTO tracking (tracking_id) VALUES ('base-tracking-id-123')")
    
    # Insert admin user with a 12 character password (lowercase + numbers)
    password = os.environ.get("ADMIN_PASSWORD", "a1b2c3d4e5f6")
    c.execute("INSERT INTO users (username, password) VALUES ('administrator', ?)", (password,))
    
    conn.commit()
    conn.close()

init_db()

CSS_STYLE = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        
        body { 
            background: radial-gradient(circle at center, #0a0f18 0%, #020408 100%);
            color: #c9d1d9; 
            font-family: 'Share Tech Mono', monospace; 
            margin: 0; 
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        
        /* Grid background effect */
        body::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: 
                linear-gradient(rgba(45, 212, 191, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(45, 212, 191, 0.05) 1px, transparent 1px);
            background-size: 30px 30px;
            z-index: -1;
        }

        .container {
            background: rgba(13, 17, 23, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(45, 212, 191, 0.2);
            border-radius: 12px;
            padding: 3rem 2.5rem;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.8), 0 0 15px rgba(45, 212, 191, 0.1) inset;
        }

        .logo {
            text-align: center;
            margin-bottom: 2rem;
        }

        .glitch {
            color: #2dd4bf;
            font-size: 2.5rem;
            text-transform: uppercase;
            letter-spacing: 4px;
            text-shadow: 0 0 10px rgba(45, 212, 191, 0.5);
            margin: 0;
        }
        
        .subtitle {
            color: #8b949e;
            font-size: 0.9rem;
            margin-top: 5px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .status-box {
            background: rgba(2, 4, 8, 0.6);
            border-left: 3px solid #f78166;
            padding: 1.2rem;
            font-size: 0.95rem;
            color: #8b949e;
            margin-bottom: 2.5rem;
            border-radius: 0 6px 6px 0;
            line-height: 1.6;
            transition: all 0.3s ease;
        }
        
        .status-box.active {
            border-left-color: #2dd4bf;
            background: rgba(45, 212, 191, 0.05);
        }

        .highlight {
            color: #2dd4bf;
            text-shadow: 0 0 8px rgba(45, 212, 191, 0.4);
        }

        .login-form {
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
        }
        
        .form-group {
            position: relative;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #8b949e;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        input {
            width: 100%;
            padding: 12px 15px;
            background: rgba(2, 4, 8, 0.8);
            border: 1px solid #30363d;
            border-radius: 6px;
            color: #c9d1d9;
            font-family: 'Share Tech Mono', monospace;
            box-sizing: border-box;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        input:focus {
            outline: none;
            border-color: #2dd4bf;
            box-shadow: 0 0 10px rgba(45, 212, 191, 0.2);
        }

        button {
            padding: 14px;
            background: transparent;
            color: #2dd4bf;
            border: 1px solid #2dd4bf;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1.1rem;
            font-family: 'Share Tech Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        
        button:hover { 
            background: rgba(45, 212, 191, 0.1); 
            box-shadow: 0 0 15px rgba(45, 212, 191, 0.3);
        }

        .error { 
            color: #f78166; 
            margin-top: 15px; 
            text-align: center; 
            font-size: 0.95rem;
            background: rgba(247, 129, 102, 0.1);
            padding: 10px;
            border-radius: 4px;
            border: 1px solid rgba(247, 129, 102, 0.2);
        }
        
        .success { 
            color: #3fb950; 
            font-size: 1.3rem; 
            text-align: center; 
            margin-top: 20px; 
            padding: 20px; 
            background: rgba(63, 185, 80, 0.1);
            border: 1px dashed #3fb950;
            border-radius: 6px;
            text-shadow: 0 0 10px rgba(63, 185, 80, 0.4);
        }
    </style>
"""

INDEX_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InvataCyber.ro</title>
    {CSS_STYLE}
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1 class="glitch">InvataCyber.ro</h1>
        </div>
        
        <div class="status-box {{ 'active' if welcome_back else '' }}">
            <div>> SYS_STATUS: <span style="color: #3fb950;">ONLINE</span></div>
            <div>> AUTH_MODULE: <span style="color: #f78166;">LOCKDOWN</span></div>
            <div style="margin-top: 10px;">
                {{% if welcome_back %}}
                <span class="highlight">>> [OK] Valid tracking signature detected.</span><br>
                <span class="highlight">>> Welcome back, authorized agent.</span>
                {{% else %}}
                <span style="color: #f78166;">>> [WARN] No valid tracking signature found.</span><br>
                <span>>> Guest mode restrictions applied.</span>
                {{% endif %}}
            </div>
        </div>
    </div>
</body>
</html>
"""

LOGIN_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InvataCyber Admin Override</title>
    {CSS_STYLE}
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1 class="glitch">InvataCyber.ro</h1>
            <div class="subtitle">Administrator Override Console</div>
        </div>

        {{% if flag %}}
            <div class="success">>> ACCESS GRANTED<br><br>{{{{ flag }}}}</div>
            <a href="/" style="display: block; text-align: center; color: #2dd4bf; margin-top: 20px; text-decoration: none; font-weight: bold; border: 1px solid #2dd4bf; padding: 10px; border-radius: 6px;">[ REBOOT SYSTEM / LOGOUT ]</a>
        {{% else %}}
            <form class="login-form" method="POST" action="/login">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" required autocomplete="off" spellcheck="false">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">Initialize Override</button>
            </form>

            {{% if login_error %}}
                <div class="error">>> {{{{ login_error }}}}</div>
            {{% endif %}}
        {{% endif %}}
    </div>
</body>
</html>
"""

def check_tracking(request):
    tracking_id = request.cookies.get('TrackingId')
    if not tracking_id:
        return False
        
    welcome_back = False
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # VULNERABLE BLIND SQLI
    query = f"SELECT tracking_id FROM tracking WHERE tracking_id = '{tracking_id}'"
    try:
        c.execute(query)
        if c.fetchone():
            welcome_back = True
    except:
        pass
    finally:
        conn.close()
        
    return welcome_back

@app.route('/')
def index():
    tracking_id = request.cookies.get('TrackingId')
    if not tracking_id:
        resp = make_response(render_template_string(INDEX_TEMPLATE, welcome_back=False))
        resp.set_cookie('TrackingId', 'base-tracking-id-123')
        return resp
        
    welcome_back = check_tracking(request)
    return render_template_string(INDEX_TEMPLATE, welcome_back=welcome_back)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template_string(LOGIN_TEMPLATE)
        
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Safe login query
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        return render_template_string(LOGIN_TEMPLATE, flag="InvataCyber{blind_sql}")
    else:
        return render_template_string(LOGIN_TEMPLATE, login_error="Access Denied. Invalid credentials.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
