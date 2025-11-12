# 💰 AI-Powered Money Tracker

A full-featured **personal finance tracking web app** built with **Flask**, **SQLite**, and **Machine Learning**.  
It helps you monitor spending, set budgets, visualize insights, and automatically categorize expenses using an AI model trained on real data.

---

## 🚀 Features

### 🧑‍💻 User System
- Secure **sign-up, login, and logout** with Flask-Login  
- Passwords hashed using Werkzeug  
- Each user’s data is fully isolated  

### 💵 Expense Management
- Add, view, edit, and delete expenses  
- Smart **auto-categorization** using a trained ML model  
- Manual override option for custom categories  

### 🎯 Budget Management
- Define monthly category budgets  
- Dashboard shows remaining vs. spent amounts  
- Automatic color alerts when nearing or exceeding limits  

### 📊 Analytics Dashboard
- **Pie chart** for category-wise spending breakdown  
- **Line or bar chart** for daily expense trends  
- Filters for viewing any previous month or year  

### 🧠 Machine Learning Integration
- Trained on `training_data.csv` with **TF-IDF** + **Naive Bayes**  
- AI auto-suggests categories as you type notes  
- Admins can **retrain the model** from real user data with one click  

### ⚡ Tech Stack
| Layer | Technology |
|-------|-------------|
| Backend | Flask, SQLAlchemy, SQLite |
| Frontend | HTML, CSS, JS, Bootstrap, Chart.js |
| Machine Learning | scikit-learn (TF-IDF + Naive Bayes) |
| Authentication | Flask-Login, CSRFProtect |

---

## 🛠️ Project Structure

money-tracker/
│
├── app/
│ ├── init.py # Flask app, DB, blueprints
│ ├── models.py # SQLAlchemy models
│ ├── routes.py # Routes for dashboard & features
│ ├── forms.py # Flask-WTF forms
│ ├── ml_logic.py # ML model + prediction logic
│ ├── templates/ # HTML pages (dashboard, login, etc.)
│ └── static/ # CSS / JS / Chart.js assets
│
├── train_model.py # Retraining script for the ML model
├── training_data.csv # Initial labeled data for training
├── requirements.txt # All dependencies
├── run.py # App entry point
└── .gitignore


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/srujan096/money-tracker-ai.git
cd money-tracker-ai

2️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
flask db upgrade

5️⃣ Start the app
python run.py

Now open your browser → http://127.0.0.1:5000
