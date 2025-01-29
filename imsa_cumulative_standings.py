import json
import os
from collections import defaultdict

def load_existing_standings(filename="cumulative_standings.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return defaultdict(dict)

def save_standings(standings, filename="cumulative_standings.json"):
    with open(filename, "w") as file:
        json.dump(standings, file, indent=4)

def merge_standings(existing_standings, new_race_results):
    for class_name, drivers in new_race_results.items():
        if class_name not in existing_standings:
            existing_standings[class_name] = {}
        for driver_id, points in drivers.items():
            existing_standings[class_name][driver_id] = existing_standings[class_name].get(driver_id, 0) + points
    return existing_standings

def generate_html(standings, filename="cumulative_standings.html"):
    html_content = "<html><head><title>Cumulative Standings</title></head><body>"
    html_content += "<h1>Cumulative Race Standings</h1>"
    class_order = ["GTP", "LMP2", "GTD"]
    
    for class_name in class_order:
        if class_name in standings:
            html_content += f"<h2>Class: {class_name}</h2><table border='1'><tr><th>Driver</th><th>Points</th></tr>"
            sorted_drivers = sorted(standings[class_name].items(), key=lambda x: x[1], reverse=True)
            for driver_id, points in sorted_drivers:
                html_content += f"<tr><td>{driver_id}</td><td>{points}</td></tr>"
            html_content += "</table>"
    
    html_content += "</body></html>"
    
    with open(filename, "w") as file:
        file.write(html_content)
    
    print(f"Cumulative standings saved to {filename}")

def main():
    existing_standings = load_existing_standings()
    
    with open("Temp Race Results/race_standings.json", "r") as file:
        new_race_data = json.load(file)
    
    updated_standings = merge_standings(existing_standings, new_race_data)
    save_standings(updated_standings)
    generate_html(updated_standings)
    
if __name__ == "__main__":
    main()