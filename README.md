# *IMSA Championship Manager*
- ## *REQUIRES* the app "SecondMonitor" and its logs by Matus Celko. 
  - It can be downloaded [here](https://gitlab.com/winzarten/SecondMonitor/-/releases) (download the topmost .msi)


## Features
- **JSON Input**: Easily import race data in JSON format.
- **Dynamic Standings**: Automatically calculates and updates championship standings based on the provided data in the JSON file.
- **HTML Output**: Generates a HTML page displaying the current standings.
- **Custom AI Files**: I included my own AI edits for those who want to use the Apline LMDh as an Acura replacement. You must use [this](https://www.overtake.gg/downloads/imsa-expansion-skinpack-gtp-lmp2-g2-gt3-g2.74185/) skinpack for this to work.


# Setup
1. Put the ```.exe``` to its own folder. It will create some subfolders too hold the htmls for the points so its important to have its own folder.
2. This is intended for AMS 2 to be ran with LMDh, LMP2, or GT3 Gen2 Cars. Any other classes will work but have weird formating.
3. SecondMonitor needs to be running while doing a Race in AMS 2.
  
# Guide
## This is the order of events:
   - Open SecondMonitor and do an AMS2 Race.
   - Open Championship Manager and load the JSON file for the race at ```C:\Users\user\Documents\SecondMonitor\Reports``` using the top button to ADD.
   - Open the ```cumulative_standings.html``` file to see the standings.
   - Reapeat this proccess for as long as you wish.
### Things to Note 
  - Drivers can be added mid season.
  - Points are based on class then driver name
  - You can run in different classes and your points will still count and be sepereate in each class.

## Did you mess something up? Do this:
- Should you accidentally add a race twice or add the wrong JSON file, there is an "Undo Race" button.
    - All this does is subtract the points the driver earned in the event from the ```cumulative_standings.html```. So you can remove a race at any point in your season as long as you still have the JSON file
- Alternatively, you can edit the ```cumulative_standings.json```. Any edits to this file will take effect AFTER adding or subtracting another JSON Race Report. That is to say, changing this file will not change the HTML in real time.
    - Since you can edit any points before you add the next race, this method can also be used for pentaly points or to cheat. I won't tell if you don't.


## Reset or simultaneous Championships:
- To reset the championship, delete ```cumulative_standings.json```,```cumulative_standings.html```, and ```\Single Race Results```
- Since this program just edits the files in the folder the exe is located, you can run multiple championships if you want.
   - All you have to do is copy ```cumulative_standings.json```,```cumulative_standings.html```, and ```\Single Race Results``` To another location. The exe will only edit the files in its folder so moving these in and out can allow simultaneous championships.
