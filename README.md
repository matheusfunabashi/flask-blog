# 📝 UniLife Blog

A beginner-friendly blog platform built with **Flask**, **MySQL**, and **Bootstrap**, featuring:
- 🔐 User authentication
- 📬 Email notifications on signup (Flask-Mail)
- ✍️ Post creation and deletion
- 🔍 Real-time user search
- 🧾 Individual profile pages
- 📸 Background images and responsive design

---

## 🚀 Live Demo

🖥️ Deployed at: _https://flask-blog-879o.onrender.com_

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, Bootstrap, JavaScript
- **Database**: MySQL (via MySQL Workbench)
- **Email**: Flask-Mail + Gmail SMTP
- **Other**: Jinja2, dotenv

---

## 🔧 Features

- ✅ Signup & login with password hashing
- ✅ Store and view posts from any user
- ✅ View your own profile with delete controls
- ✅ View other users' profiles via dynamic search
- ✅ Background images and styling with Bootstrap
- ✅ Sends welcome email to users after signup

---

## 💻 How to Run Locally

Clone the repo and install dependencies:

```bash
git clone https://github.com/matheusfunabashi/flask-blog.git
cd flask-blog
pip install -r requirements.txt
```

# 🔑 Create a .env file in the root folder with your credentials:

FLASK_SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=login_demo

# 🏁 Start the app:

python app.py

# 👨🏾‍💻 Author

Matheus Funabashi 💙
