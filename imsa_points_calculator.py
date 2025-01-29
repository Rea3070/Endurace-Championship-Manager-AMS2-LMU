import json
import os
from collections import defaultdict
from pathlib import Path

# IMSA Points System
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
INDY_POINTS = {
    1: 50,
    2: 40,
    3: 35,
    4: 32,
    5: 30,
    6: 28,
    7: 26,
    8: 24,
    9: 22,
    10: 20,
    11: 19,
    12: 18,
    13: 17,
    14: 16,
    15: 15,
    16: 14,
    17: 13,
    18: 12,
    19: 11,
    20: 10,
    21: 9,
    22: 8,
    23: 7,
    24: 6,
    25: 5
}

def assign_points(drivers):
    points = defaultdict(dict)
    class_name_map = {"LMDh_LD": "GTP","LMDh": "GTP", "LMP2_LD": "LMP2", "GT3_Gen2_LD": "GTD", "GT3_Gen2": "GTD"}  # Mapping class names to ordered names
    
    for driver in drivers:
        class_name = class_name_map.get(driver["ClassName"], driver["ClassName"])  # Convert to standardized class name
        driver_id = driver["DriverLongName"]
        position_in_class = driver["FinishingPositionInClass"]
        points_awarded = IMSA_POINTS.get(position_in_class, 100)  # Default to 0 if position is outside points range
        
        points[class_name][driver_id] = {
            "Points": points_awarded,
            "CarName": driver["CarName"].replace(" - Low Downforce", ""),
            "FinishStatus": driver["FinishStatus"],
            "InitialPositionInClass": driver["InitialPositionInClass"],
            "FinishingPosition": driver["FinishingPositionInClass"]
        }
    return points

def generate_html(standings, SessionRunTime,Track):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Race Standings</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                text-align: center;
            }
            .header {
                background-image: url('https://www.revolutionworld.com/wp-content/uploads/2022/08/IMSA-logo-600x400-1.png'); 
                background-size:  600px 400px;
                background-position: center;
                background-repeat: no-repeat;
                color: white;
                padding: 300px 20px 60px 20px;
                font-size: 2em;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            h1 {
                color: #333;
                margin-top: 50px;
                
            }
            h2 {
                color: #007BFF;
                margin-top: 30px;
            }
            table {
                width: 80%;
                margin: 20px auto;
                border-collapse: collapse;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                background-color: white;
            }
            th, td {
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #007BFF;
                color: white;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            .footer {
                margin-top: 40px;
                font-size: 0.9em;
                color: #777;
            }
        </style>
    </head>
    <body><div class="header">"""
    html_content += f"<h1>{Track} Standings</h1></div>"
  
    
    class_order = ["GTP", "LMP2", "GTD"]  # Define the desired order
    
    for class_name in class_order:
        if class_name in standings:
            html_content += f"<h2>Class: {class_name}</h2><table>"
            html_content += """
            <tr>
            <th width="10">Finish</th>
            <th width="10">Start</th>
            <th>Driver</th><th>Car</th>
            <th>Status</th>
            <th>Points</th>
            </tr>
            """
            sorted_drivers = sorted(standings[class_name].items(), key=lambda x: x[1]["Points"], reverse=True)

            for driver_id, details in sorted_drivers:
                html_content += f"""
                <tr>
                  
                    <td>{details['FinishingPosition']}</td>
                    <td>{details['InitialPositionInClass']}</td>
                    <td>{driver_id}</td>
                    <td>{details['CarName']}</td>
                    <td>{details['FinishStatus']}</td>
                    <td>{details['Points']}</td>

                   
                </tr>
                """
            html_content += "</table>"
    html_content += f"""
        <div class="footer">
            <p>Race Time: {SessionRunTime}</p>
        </div>
    </body>
    </html>
    """
    
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

   #Unused method for cumulative points


    # Generate and save HTML standings
    generate_html(race_points, SessionRunTime, track)
    save_standings(race_points)
if __name__ == "__main__":
    main()
