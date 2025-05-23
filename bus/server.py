from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

routes = {
    "R1": {"stops": ["ISBT", "CP", "AIIMS", "Saket"]},
    "R2": {"stops": ["Dwarka", "Janakpuri", "CP", "Noida"]},
    "R3": {"stops": ["Narela", "Mukherjee Nagar", "RK Ashram", "IGI Airport"]},
}

bus_schedule = []
peak_hours = [8, 9, 17, 18]

coords = {
    "ISBT": (28.66, 77.22), "CP": (28.63, 77.22), "AIIMS": (28.57, 77.21), "Saket": (28.52, 77.20),
    "Dwarka": (28.60, 77.04), "Janakpuri": (28.62, 77.08), "Noida": (28.53, 77.39),
    "Narela": (28.84, 77.09), "Mukherjee Nagar": (28.71, 77.21), "RK Ashram": (28.63, 77.21),
    "IGI Airport": (28.55, 77.10)
}

@app.route("/schedule")
def get_schedule():
    bus_schedule.clear()
    now = datetime.now()
    freq = 15 if now.hour in peak_hours else 30
    for rid, rdata in routes.items():
        for i in range(4):
            start_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=i * freq)
            bus_schedule.append({
                "bus_id": f"{rid}-B{i+1}",
                "route": rid,
                "start_time": start_time.isoformat(),
                "status": "Scheduled"
            })
    return jsonify(bus_schedule)

@app.route("/track/<bus_id>")
def track(bus_id):
    match = next((b for b in bus_schedule if b["bus_id"] == bus_id), None)
    if not match:
        return jsonify({"error": "Bus not found"}), 404
    location = random.choice(routes[match["route"]]["stops"])
    return jsonify({"bus_id": bus_id, "location": location, "coordinates": coords[location]})

if __name__ == "__main__":
    app.run(debug=True)
