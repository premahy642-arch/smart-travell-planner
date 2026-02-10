# Smart Travel Planner

## 📖 Overview
Smart Travel Planner is a Python-based desktop application that helps users plan trips efficiently.  
It integrates **weather forecasting**, **cost estimation**, **tourist attractions**, and **trip storage** into a single interface.  
The application uses **Tkinter** for the GUI, **OpenWeather API** for live weather data, and **SQLite** for persistent storage.

---

## ✨ Features
- **User Authentication**: Signup and login system using SQLite.
- **Weather Integration**: Fetches real-time weather for the destination city.
- **Cost Estimation**: Calculates travel cost based on distance and budget.
- **Budget Check**: Verifies if the entered budget is sufficient.
- **Attractions**: Displays popular tourist attractions for major cities.
- **Trip Storage**: Saves planned trips to the database for each user.
- **View Trips**: Allows users to view all their saved trips.

---

## 🛠️ Technologies Used
- **Python 3.x**
- **Tkinter** (GUI)
- **SQLite3** (Database)
- **Requests** (API calls)
- **OpenWeather API**
  

---

## ⚙️ Installation & Setup
1. Clone or download the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
Get a free API key from OpenWeather.

Replace the API key in main.py inside the get_weather() function.

Run the application:python main.py
Signup/Login with a username and password.

Enter Start Location, Destination, and Budget.

Click Plan Trip to view weather, cost, budget sufficiency, and attractions.

Click View Trips to see all saved trips for your account.

📸 Screenshots
Login/Signup Screen

Trip Planning Screen

Weather & Attractions Output

View Trips Screen

---

