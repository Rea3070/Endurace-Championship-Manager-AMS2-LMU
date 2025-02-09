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

def merge_standings(existing_standings, new_race_results, param):
    for class_name, drivers in new_race_results.items():
        if class_name not in existing_standings:
            existing_standings[class_name] = {}
        
        for driver_id, details in drivers.items():
            if driver_id not in existing_standings[class_name]:
                # Initialize the driver's entry with the new format
                existing_standings[class_name][driver_id] = {
                    "Points": details["Points"],
                    "CarName": details["CarName"],
                    "FinishStatus": details["FinishStatus"],
                    "InitialPositionInClass": details["InitialPositionInClass"]
                }
            else:
                # Handle the case where existing standings might be in the old format (just points)
                if isinstance(existing_standings[class_name][driver_id], int):
                    # Convert old format to new format
                    existing_standings[class_name][driver_id] = {
                        "Points": existing_standings[class_name][driver_id],
                        "CarName": details["CarName"],  # Use the latest car name
                        "FinishStatus": details["FinishStatus"],  # Use the latest finish status
                        "InitialPositionInClass": details["InitialPositionInClass"]  # Use the latest initial position
                    }
                else:
                    # Update points and keep the existing additional fields
                    if param == "add":
                        existing_standings[class_name][driver_id]["Points"] += details["Points"]
                    else:
                        existing_standings[class_name][driver_id]["Points"] -= details["Points"]
    
    return existing_standings


def generate_html(standings, url2, filename="cumulative_standings.html" ):
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
            .header {"""
    html_content += f"background-image: url('{url2}');" 
    html_content += """background-size:  auto;
                background-position: center;
                background-repeat: no-repeat;
                color: white;
                padding: 200px 20px 60px 20px;
                font-size: 2em;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            h1 {
                color: #333;
                margin-top: 250px;
                
            }
            h2 {
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
    html_content += f"<h1>Overall Standings</h1></div>"
  
    
    class_order = ["GTP", "Hyper", "LMP2", "GTD", "GT3"]  # Define the desired order
    
    for class_name in class_order:
        if class_name in standings and class_name == "GTP":
            html_content += f"""<h2 style="color:black;">Class: {class_name}</h2><table>"""
            html_content += """
            <tr style="background-color: #000000">
            <th width="10">Position</th>
            <th>Driver</th>
            <th>Car</th>
            <th>Points</th>
            </tr>
            """
            sorted_drivers = sorted(standings[class_name].items(), key=lambda x: x[1]["Points"], reverse=True)
            i = 1
            for driver_id, details in sorted_drivers:
                html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{driver_id}</td>
                    <td>{details['CarName']}</td>
                    <td>{details['Points']}</td>
                </tr>
                """
                i += 1
            html_content += "</table>"
        elif class_name == "Hyper" and class_name in standings: 
            html_content += f"""<h2 style="color:red;">Class: {class_name}</h2><table>"""
            html_content += """
            <tr style="background-color: #ff0000">
            <th width="10">Position</th>
            <th>Driver</th>
            <th>Car</th>
            <th>Points</th>
            </tr>
            """
            sorted_drivers = sorted(standings[class_name].items(), key=lambda x: x[1]["Points"], reverse=True)
            i = 1
            for driver_id, details in sorted_drivers:
                html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{driver_id}</td>
                    <td>{details['CarName']}</td>
                    <td>{details['Points']}</td>
                </tr>
                """
                i += 1
            html_content += "</table>"
        elif class_name == "LMP2" and class_name in standings: 
            html_content += f"""<h2 style="color:#0051ff;">Class: {class_name}</h2><table>"""
            html_content += """
            <tr style="background-color: #0051ff">
            <th width="10">Position</th>
            <th>Driver</th>
            <th>Car</th>
            <th>Points</th>
            </tr>
            """
            sorted_drivers = sorted(standings[class_name].items(), key=lambda x: x[1]["Points"], reverse=True)
            i = 1
            for driver_id, details in sorted_drivers:
                html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{driver_id}</td>
                    <td>{details['CarName']}</td>
                    <td>{details['Points']}</td>
                </tr>
                """
                i += 1
            html_content += "</table>"
        elif class_name == "GTD" and class_name in standings: 
            html_content += f"""<h2 style="color:#3df011;">Class: {class_name}</h2><table>"""
            html_content += """
            <tr style="background-color: #3df011">
            <th width="10">Position</th>
            <th>Driver</th>
            <th>Car</th>
            <th>Points</th>
            </tr>
            """
            sorted_drivers = sorted(standings[class_name].items(), key=lambda x: x[1]["Points"], reverse=True)
            i = 1
            for driver_id, details in sorted_drivers:
                html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{driver_id}</td>
                    <td>{details['CarName']}</td>
                    <td>{details['Points']}</td>
                </tr>
                """
                i += 1
            html_content += "</table>"
        elif class_name == "GT3" and class_name in standings: 
            html_content += f"""<h2 style="color:#e0a309;">Class: {class_name}</h2><table>"""
            html_content += """
            <tr style="background-color: #e0a309">
            <th width="10">Position</th>
            <th>Driver</th>
            <th>Car</th>
            <th>Points</th>
            </tr>
            """
            sorted_drivers = sorted(standings[class_name].items(), key=lambda x: x[1]["Points"], reverse=True)
            i = 1
            for driver_id, details in sorted_drivers:
                html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{driver_id}</td>
                    <td>{details['CarName']}</td>
                    <td>{details['Points']}</td>
                </tr>
                """
                i += 1
            html_content += "</table>"
    html_content += f"""
    </body>
    </html>
    """
    
    with open(filename, "w") as file:
        file.write(html_content)
    
    print(f"Cumulative standings saved to {filename}")

def main(param, game):
    existing_standings = load_existing_standings()
    
    with open("Temp Race Results/race_standings.json", "r") as file:
        new_race_data = json.load(file)
    if game == "wec" or game == "wec_8hr" or game == "leman":
        url2 = "https://upload.wikimedia.org/wikipedia/en/thumb/f/fa/FIA_WEC_Logo_2019.svg/640px-FIA_WEC_Logo_2019.svg.png"   
    elif game == "imsa":
        url2 = "https://www.revolutionworld.com/wp-content/uploads/2022/08/IMSA-logo-600x400-1.png"
    updated_standings = merge_standings(existing_standings, new_race_data, param)
    save_standings(updated_standings)
    generate_html(updated_standings, url2)
    
if __name__ == "__main__":
    main()