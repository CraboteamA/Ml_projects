# Habit Dashboard

Track your daily sleep, mood, weight, workouts, and coding practice in a sleek offline‑first web app.  
Built with **Flask • SQLite • Plotly**.

---

## ✨ Features
| Module | Highlights |
|--------|------------|
| **Daily entry** | Two‑column form with instant *Save / Update* |
| **Current streaks** | Counts consecutive days (breaks only after 7 missed days) for workouts & coding |
| **History view** | Dark‑themed table with inline *Edit* link per day |
| **Analytics** | • 7‑day rolling averages<br>• Sleep vs Mood scatter<br>• Mood vs Activity scatter |
| **Dark dashboard UI** | Soft‑shadow cards, accent colour token, hover‑lift |
| **JSON backup** | One‑command export / restore |
| **ML‑ready** | Schema & code structured for future forecasting, clustering, anomaly detection |

## 📂 Project layout
```text
habit-dashboard/
├─ app.py                # Flask routes
├─ models.py             # SQLAlchemy schema
├─ utils.py              # rolling avg + streak helpers
├─ templates/
│   ├─ layout.html
│   ├─ index.html
│   ├─ charts.html
│   └─ history.html
├─ static/
│   ├─ css/dark-dashboard.css
│   └─ js/
│       ├─ charts.js
│       └─ entry.js       # (AJAX + toast, optional)
├─ habit.db              # SQLite DB (auto‑created)
└─ requirements.txt
```

## 🚀 Quick‑start
### 1 · env
```conda create -n habits python=3.12 -y```
```conda activate habits```

### 2 · deps
```pip install -r requirements.txt```

### 3 · run
```python app.py # http://127.0.0.1:5000```

## 🧠 Future ML roadmap
- Month 1 (30 rows) – anomaly detection & client‑side cluster colours
- Month 3 (90 rows) – mood regression with SHAP explanations
- Month 6 (180 rows) – wearable import, time‑series forecasting
(I don't want to generate data and will use my own instead)
