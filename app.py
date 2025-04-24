from flask import Flask, request, render_template, redirect, url_for, session, g, flash, jsonify
import sqlite3
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

DATABASE = 'blog.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row 
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['passw']

        db = get_db()
        cursor = db.cursor()
        try:
            sql = "SELECT * FROM blog_users WHERE email = ?"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
        finally:
            cursor.close()

        if result and check_password_hash(result['password'], password):
            session['user_id'] = result['id']
            session['email'] = result['email']
            session['username'] = result['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message=True)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        uname = request.form['uname']
        password = request.form['passw']
        try:
            valid = validate_email(email)
            email = valid.email 
        except EmailNotValidError as e:
            flash("Invalid Email", 'danger')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()
        try:
            sql = "INSERT INTO blog_users (username, password, email) VALUES (?, ?, ?)"
            cursor.execute(sql, (uname, hashed_password, email)) 
            db.commit()
            msg = Message("Welcome to UniLife 🎉",
                sender="theunilife.official@gmail.com",  # same as MAIL_USERNAME
                recipients=[email])
            msg.body = f"Hi {uname}, thanks for signing up for UniLife!"
            mail.send(msg)
        finally:
            cursor.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = get_db()
    cursor = db.cursor()
    try:
        sql = "SELECT posts.*, blog_users.username FROM posts JOIN blog_users ON posts.user_id = blog_users.id ORDER BY created_at DESC"
        cursor.execute(sql)
        posts = cursor.fetchall()
    finally:
        cursor.close()

    return render_template('dashboard.html', email=session['email'], username=session['username'], posts=posts)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    
    db = get_db()
    cursor = db.cursor()    
    try:
        sql = "SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC"
        cursor.execute(sql, (user_id,))
        user_posts = cursor.fetchall()
    finally:
        cursor.close()
    return render_template('profile.html', posts=user_posts)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']
        
        db = get_db()
        cursor = db.cursor()
        try:
            sql = "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)"
            cursor.execute(sql, (user_id, title, content))
            db.commit()
        finally:
            cursor.close()

        return redirect('/dashboard')

    return render_template('publish.html')

@app.route('/delete_post', methods=['POST'])
def delete_post():
    if 'user_id' not in session:
        return redirect('/login')

    post_id = request.form['post_id']
    user_id = session['user_id']

    db = get_db()
    cursor = db.cursor()
    try:
        sql = "DELETE FROM posts WHERE id = ? AND user_id = ?"
        cursor.execute(sql, (post_id, user_id))
        db.commit()
    finally:
        cursor.close()

    return redirect('/profile')

@app.route('/search_users')
def search_users():
    query = request.args.get('query', '').strip()

    db = get_db()
    cursor = db.cursor()
    try:
        sql = "SELECT id, username FROM blog_users WHERE username LIKE ?"
        cursor.execute(sql, (f'%{query}%',))
        results = cursor.fetchall()
        users = [{'id': row['id'], 'username': row['username']} for row in results]
    finally:
        cursor.close()

    return jsonify(users=users)

@app.route('/user/<username>')
def user_profile(username):
    db = get_db()
    cursor = db.cursor()
    try:
        sql = "SELECT * FROM posts JOIN blog_users ON posts.user_id = blog_users.id WHERE blog_users.username = ? ORDER BY posts.created_at DESC"
        cursor.execute(sql, (username,))
        user_posts = cursor.fetchall()
    finally:
        cursor.close()

    return render_template('user_profile.html', username=username, posts=user_posts)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # get port from Render
    app.run(host='0.0.0.0', port=port, debug=True)
