# Task-Manager-App
# 🗂️ Task Manager App (Python + Kivy)

A fully featured, visually aesthetic **task management app** built using **Python and Kivy**, designed for personal productivity and goal tracking.

---

## 🚀 Purpose

I built this app to help myself:
- Write down and manage daily or one-time tasks
- Update task progress over time
- Track success rate using visual data
- Reflect on productivity and improve habits

This is not just a to-do list — it’s a **customized notepad + analytics dashboard**.

---

## 📱 Features

### ✅ Task Management
- Create **Daily Tasks** with durations
- Add **One-Time Tasks** with notes
- Update progress via slider or checkbox
- Delete or edit existing tasks
- Automatic progress tracking and completion detection

### 🗃️ Notes
- Add notes when creating or updating tasks
- Daily logs for each completed instance (Daily Tasks)
- Stored persistently in `tasks.json`

### 🌈 UI / UX
- Gradient background and color-themed widgets
- Responsive design and font scaling
- Floating Action Buttons for:
  - Add Task
  - View History
  - Send Suggestion
  - About Section
- Custom icons and fonts (Lobster, Font Awesome)

### 💾 Data Storage
- All task data saved in `tasks.json`
- Automatically updated on any task change

---

## 📊 Graphs & Analytics

Built-in charts using `matplotlib`, with scroll + zoom popups in Kivy:

| Chart | Description |
|-------|-------------|
| ✅ **Completion Ratio** | Pie chart of Completed vs Incomplete tasks |
| 📈 **Total Completion Over Time** | Line graph of cumulative completions |
| 📊 **Daily Completion Trends** | Bar graph of completions in past 10 days |
| 🧮 **Task Types Breakdown** | Doughnut chart of Daily vs One-Time tasks |
| 📶 **Cumulative Completion History** | Stacked bar chart of progress for last 10 tasks |

---

## 📂 Project Structure

```
├── Task manager app.py       # Main application code
├── tasks.json                # Persistent task storage (auto-created)
├── add.png / advice.png / ...# Icons used for FABs
└── fonts/
    └── Lobster-Regular.ttf   # Custom font for header
```

---

## ⚙️ Requirements

- Python 3.7+
- Kivy >= 2.0.0
- matplotlib
- numpy
- pandas

```bash
pip install kivy matplotlib numpy pandas
```

---


## 📌 Notes

- All tasks and notes are stored persistently
- Charts are generated on demand and auto-cleaned
- Suggestions popup supports user input with confirmation

---

## 💡 Future Improvements

- Sync with calendar (e.g., Google Tasks or iCal)
- Cloud storage support (e.g., Firebase)
- Login/auth system for multiple users
- Export tasks to CSV/Excel

---

## 🧑‍💻 Author

**Built for personal productivity and growth.**

This project was created by someone who needed a **better way to understand their own task completion habits** and **improve success rates** through self-analysis.

---

## 📜 License

This project is open-source and free to use for learning or personal productivity. Attribution appreciated.


