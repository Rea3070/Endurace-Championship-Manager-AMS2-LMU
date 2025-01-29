import json
import os
from collections import defaultdict
from pathlib import Path

# IMSA Points System (Top 10 Positions Example, Adjust as Needed)
IMSA_POINTS = {
    1: 350,
    2: 320,
    3: 300,
    4: 280,
    5: 260,
    6: 250,
    7: 240,
    8: 230,
    9: 220,
    10: 210,
    11: 200,
    12: 190,
    13: 180,
    14: 170,
    15: 160,
    16: 150,
    17: 140,
    18: 130,
    19: 120,
    20: 110,
}

def assign_points(drivers):
    points = defaultdict(dict)
    class_name_map = {"LMDh_LD": "GTP","LMDh": "GTP", "LMP2_LD": "LMP2", "GT3_Gen2_LD": "GTD", "GT3_Gen2": "GTD"}  # Mapping class names to ordered names
    
    for driver in drivers:
        class_name = class_name_map.get(driver["ClassName"], driver["ClassName"])  # Convert to standardized class name
        driver_id = driver["DriverLongName"]
        position_in_class = driver["FinishingPositionInClass"]
        points_awarded = IMSA_POINTS.get(position_in_class, 0)  # Default to 0 if position is outside points range
        
        points[class_name][driver_id] = points_awarded
    return points

def merge_points(existing_points, new_points):
    for class_name, drivers in new_points.items():
        if class_name not in existing_points:
            existing_points[class_name] = {}
        for driver_id, points in drivers.items():
            existing_points[class_name][driver_id] = existing_points[class_name].get(driver_id, 0) + points
    return existing_points

def generate_html(standings, SessionRunTime,Track):
    html_content = "<html><head><title>Race Standings</title></head><body>"
    html_content += f"<h1>{Track} Standings</h1>"
    class_order = ["GTP", "LMP2", "GTD"]  # Define the desired order
    
    for class_name in class_order:
        if class_name in standings:
            html_content += f"<h2>Class: {class_name}</h2><table border='1'><tr><th>Driver</th><th>Points</th></tr>"
            sorted_drivers = sorted(standings[class_name].items(), key=lambda x: x[1], reverse=True)
            for driver_id, points in sorted_drivers:
                html_content += f"<tr><td>{driver_id}</td><td>{points}</td></tr>"
            html_content += "</table>"
    html_content += "</body></html>"
    
    Path("Single Race Results").mkdir(parents=True, exist_ok=True)
    with open("Single Race Results/"+Track+" Race Standings on "+SessionRunTime.replace(":","-")+".html", "w") as file:
        file.write(html_content)
    
    print("Standings saved to standings.html")


def save_standings(standings, filename="race_standings.json"):
    Path("Temp Race Results").mkdir(parents=True, exist_ok=True)
    with open("Temp Race Results/"+filename, "w") as file:
        json.dump(standings, file, indent=4)

def main(raceresult):
    # Load primary race data JSON file
    with open(raceresult, "r") as file:
        data = json.load(file)
    SessionRunTime = data["SessionRunTime"][:16]
    track = data["TrackInfo"]["TrackName"]

    race_points = assign_points(data["Drivers"])
    print("Initial Points:", race_points)
    
    # Load additional points JSON file (if provided)
    try:
        with open("additional_points.json", "r") as file:
            additional_data = json.load(file)
        race_points = merge_points(race_points, additional_data)
        print("Updated Points After Merging:", race_points)
    except FileNotFoundError:
        print("No additional points file found. Skipping merge.")
    
    # Generate and save HTML standings
    generate_html(race_points, SessionRunTime, track)
    save_standings(race_points)
if __name__ == "__main__":
    main()