import tkinter as tk
import requests
import sqlite3

# ------------------ DATABASE SETUP ------------------
conn = sqlite3.connect("travel_planner.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS trips (
    username TEXT,
    start TEXT,
    destination TEXT,
    budget INTEGER,
    weather TEXT,
    cost INTEGER,
    attractions TEXT
)
""")
conn.commit()

# ------------------ WEATHER FUNCTION ------------------
def get_weather(city):
    api_key = "fc422a10d55ebb61856d65449faf0b40"  # Your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data.get("main"):
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Weather in {city}: {temp}°C, {desc}"
    else:
        return "Weather data not available"

# ------------------ DISTANCE LOOKUP ------------------
distances = {
    ("Delhi", "Mumbai"): 1400,
    ("London", "Sydney"): 17000,
    ("Mumbai", "Sydney"): 10000,
    ("Paris", "London"): 350,
    ("New York", "London"): 5600,
    ("Dubai", "Mumbai"): 2000,
    ("Bengaluru", "Punjab"): 2400
}

def get_distance(start, destination):
    return distances.get((start.title(), destination.title()), 300)

# ------------------ ATTRACTIONS ------------------
attractions_data = {
    "Delhi": ["Red Fort", "Qutub Minar", "India Gate"],
    "Mumbai": ["Gateway of India", "Marine Drive", "Elephanta Caves"],
    "London": ["Big Ben", "London Eye", "Tower Bridge"],
    "Sydney": ["Sydney Opera House", "Harbour Bridge", "Bondi Beach"],
    "Bengaluru": ["Lalbagh Botanical Garden", "Cubbon Park", "Bangalore Palace"],
    "Punjab": ["Golden Temple (Amritsar)", "Jallianwala Bagh", "Wagah Border"],
    "Paris": ["Eiffel Tower", "Louvre Museum", "Notre Dame"],
    "New York": ["Statue of Liberty", "Central Park", "Times Square"],
    "Dubai": ["Burj Khalifa", "Palm Jumeirah", "Dubai Mall"]
}

def get_attractions(city):
    return attractions_data.get(city.title(), ["No attractions data available"])

# ------------------ LOGIN/SIGNUP ------------------
def signup():
    username = entry_username.get()
    password = entry_password.get()
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        status_label.config(text="✅ Signup successful! Please login.")
    except:
        status_label.config(text="⚠️ Username already exists.")

def login():
    username = entry_username.get()
    password = entry_password.get()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():
        status_label.config(text=f"✅ Welcome {username}! You can plan trips now.")
        global current_user
        current_user = username
    else:
        status_label.config(text="⚠️ Invalid login details.")

# ------------------ PLAN TRIP ------------------
def plan_trip():
    start = entry_start.get()
    destination = entry_destination.get()
    budget = entry_budget.get()
    
    # Weather
    weather_info = get_weather(destination)
    
    # Cost estimation
    distance = get_distance(start, destination)
    cost_per_km = 5
    estimated_cost = distance * cost_per_km
    
    # Budget check
    if budget.isdigit():
        budget_val = int(budget)
        if budget_val >= estimated_cost:
            budget_status = f"✅ Budget is sufficient (Estimated cost: ₹{estimated_cost})"
        else:
            budget_status = f"⚠️ Budget is insufficient (Estimated cost: ₹{estimated_cost})"
    else:
        budget_status = "Budget must be a number."
    
    # Attractions
    attractions = get_attractions(destination)
    attractions_text = "Attractions: " + ", ".join(attractions)
    
    # Save trip if logged in
    if current_user:
        cursor.execute("INSERT INTO trips VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (current_user, start, destination, budget, weather_info, estimated_cost, attractions_text))
        conn.commit()
    
    # Output
    output_label.config(
        text=f"Trip from {start} to {destination} with budget ₹{budget}\n{weather_info}\n{budget_status}\n{attractions_text}"
    )

# ------------------ VIEW TRIPS ------------------
def view_trips():
    if current_user:
        cursor.execute("SELECT * FROM trips WHERE username=?", (current_user,))
        trips = cursor.fetchall()
        if trips:
            trips_text = "\n".join([f"{t[1]} → {t[2]} | Budget: ₹{t[3]} | {t[4]} | Cost: ₹{t[5]} | {t[6]}" for t in trips])
            output_label.config(text=f"Saved Trips for {current_user}:\n{trips_text}")
        else:
            output_label.config(text="No trips saved yet.")
    else:
        output_label.config(text="⚠️ Please login first.")

# ------------------ GUI ------------------
root = tk.Tk()
root.title("Smart Travel Planner")
root.geometry("550x450")
root.configure(bg="#f0f8ff")

# Login/Signup Section
tk.Label(root, text="Username:", bg="#f0f8ff", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Password:", bg="#f0f8ff", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text="Signup", command=signup, bg="#90ee90").grid(row=2, column=0, pady=5)
tk.Button(root, text="Login", command=login, bg="#add8e6").grid(row=2, column=1, pady=5)

status_label = tk.Label(root, text="", bg="#f0f8ff", fg="blue")
status_label.grid(row=3, column=0, columnspan=2)

# Trip Planner Section
tk.Label(root, text="Start Location:", bg="#f0f8ff", font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=5)
entry_start = tk.Entry(root)
entry_start.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Destination:", bg="#f0f8ff", font=("Arial", 10)).grid(row=5, column=0, padx=10, pady=5)
entry_destination = tk.Entry(root)
entry_destination.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Budget (₹):", bg="#f0f8ff", font=("Arial", 10)).grid(row=6, column=0, padx=10, pady=5)
entry_budget = tk.Entry(root)
entry_budget.grid(row=6, column=1, padx=10, pady=5)

tk.Button(root, text="Plan Trip", command=plan_trip, bg="#ffa07a").grid(row=7, column=0, columnspan=2, pady=10)
tk.Button(root, text="View Trips", command=view_trips, bg="#d3d3d3").grid(row=8, column=0, columnspan=2, pady=5)

output_label = tk.Label(root, text="", justify="left", bg="#f0f8ff", font=("Arial", 10))
output_label.grid(row=9, column=0, columnspan=2, pady=10)

current_user = None

root.mainloop()
