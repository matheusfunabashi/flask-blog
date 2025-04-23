from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

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

        cursor = db.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM blog_users WHERE email = %s"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            cursor.fetchall()
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

        hashed_password = generate_password_hash(password)

        cursor = db.cursor()
        try:
            sql = "INSERT INTO blog_users (username, password, email) VALUES (%s, %s, %s)"
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
    
    cursor = db.cursor(dictionary=True)
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
    cursor = db.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM posts WHERE user_id = %s ORDER BY created_at DESC"
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
        
        cursor = db.cursor(dictionary=True)
        try:
            sql = "INSERT INTO posts (user_id, title, content) VALUES (%s, %s, %s)"
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

    cursor = db.cursor()
    try:
        sql = "DELETE FROM posts WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (post_id, user_id))
        db.commit()
    finally:
        cursor.close()

    return redirect('/profile')

@app.route('/search_users')
def search_users():
    query = request.args.get('query', '').strip()

    cursor = db.cursor(dictionary=True)
    try:
        sql = "SELECT id, username FROM blog_users WHERE username LIKE %s"
        cursor.execute(sql, (f'%{query}%',))
        results = cursor.fetchall()
    finally:
        cursor.close()

    return {'users': results}

@app.route('/user/<username>')
def user_profile(username):
    cursor = db.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM posts JOIN blog_users ON posts.user_id = blog_users.id WHERE blog_users.username = %s ORDER BY posts.created_at DESC"
        cursor.execute(sql, (username,))
        user_posts = cursor.fetchall()
    finally:
        cursor.close()

    return render_template('user_profile.html', username=username, posts=user_posts)



if __name__ == '__main__':
    app.run(debug=True)
