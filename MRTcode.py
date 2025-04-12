mrt = [] #Stores each line from MRT.txt into a list (raw data) (e.g. 1;CC1 Dhoby Ghaut <-> CC2 Bras Basah;Circle;0.6;0607;2357;0554;0003)
lines = [] #Stores all the different lines (e.g. Circle, North East)
stations = [] #Stores all the different stations
mrtlines = [] #Stores the line each station corresponds with (e.g. ["Dhoby Ghaut", "Circle"])
stationcat = {} #Assigns the line each MRT code corresponds with (e.g. "CC1": "Circle")
mrtdict = {} #Assigns each MRT code to the station (e.g. "CC1": "Dhoby Ghaut")
speeddict = {} #

choices = ["1", "2", "3", "4", "5", "6"] #All the possible choices the user can make

#Function to sort the stations
def sort_key(item):
     # Extract the prefix and numeric part
    prefix = item[0][:2]
    number = 0  # Default number for prefixes with no number (e.g. "CG")
    
    # Check if the prefix has a numeric part after it (e.g. CC1)
    if len(item[0]) > 2 and item[0][2:].isdigit():
        number = int(item[0][2:])
    return (prefix, number)

def get_station_code(name):
    for code in mrtdict:
        if code == name:
            return True
    return False

def get_all_station_code(name):
    codes = []
    for code in mrtdict:
        if mrtdict[code].lower() == name.lower():
            codes.append(code)
    return "/".join(codes) if codes else None

#function to read into each file and stores the data into lists and dicts
def readingfiles():
    mrtfile = open("MRT.txt", "r")
    mrtfile.seek(0)
    for position,line in enumerate(mrtfile):
        i = line.split(";")
        if position <= 4:
            continue
        i[7] = i[7].strip()
        mrt.append(i)
        station = i[1].split(" <-> ")
        station1_code, station1_name = station[0].split(" ", 1)
        station2_code, station2_name = station[1].split(" ", 1)
        if station1_code not in mrtdict:
            mrtdict[station1_code] = station1_name
        if station2_code not in mrtdict:
            mrtdict[station2_code] = station2_name
        if [station1_name, i[2]] not in mrtlines:
            mrtlines.append([station1_name, i[2]])
        if [station2_name, i[2]] not in mrtlines:
            mrtlines.append([station2_name, i[2]])
        if station1_code not in stationcat:
            stationcat[station1_code] = i[2]
        if station2_code not in stationcat:
            stationcat[station2_code] = i[2]
        if i[2].lower() not in lines:
            lines.append(i[2].lower())
        if station1_name.lower() not in stations:
            stations.append(station1_name.lower())
        if station2_name.lower() not in stations:
            stations.append(station2_name.lower())
    mrtfile.close()

    # linesfile = open("MRT lines.txt", "r")
    # linesfile.seek(0)
    # for line in linesfile:
    #     i = line.split(";")
    #     mrtdict[i[0]] = i[1]
    #     mrtlines.append([i[1], i[2].strip()])
    #     stationcat[i[0]] = i[2].strip()
    # linesfile.close()

    speedfile = open("MRT speed.txt", "r")
    speedfile.seek(0)
    for line in speedfile:
        i = line.split(";")
        speeddict[i[0]] = int(i[1].strip())
    speedfile.close()

def mainscreen():
    print("\nWelcome to the MRT Information Centre!")
    print("What would you like to enquire about?")
    print("1. List every station in an MRT line")
    print("2. Find the best route between two stations")
    print("3. Distance and time of travel between two stations")
    print("4. Whether there is a train running and if it will arrive at your destination station before the last train time")
    print("5. What MRT line is your station on")
    print("6. Find the fare required from Station A to B during peak hours")

def opt1(): #list every station of an MRT line
    templist = []
    print("\nWhat is the MRT line you would like to enquire about?")
    print("Here is a list of lines that you can inquire about:")
    for i in lines:
        print(i.capitalize())
    print()
    line = input(">>> ")
    while str(line).lower() not in lines:
        print("\nThat is not a valid option!")
        print("Please try again! >_<")
        line = input("\n>>> ")
    print(f"\nHere is a list of station in the {line} line")
    for i in mrtlines: #["Dhoby Ghaut", "Circle"] this is an eg of i
        # print(i[1].lower(), line.lower())
        if line.lower() == i[1].lower():
            for k1, v1 in mrtdict.items(): #"CC1", "Dhoby Ghaut"
                for k2, v2 in stationcat.items(): #"CC1", "Circle"
                    if v1 == i[0] and v2.lower() == line.lower() and k1 == k2:
                        templist.append([k1, v1])
                        break
    templist.sort(key=sort_key)
    for i in templist:
        print(f"{i[0]} {i[1]}")

def stationconnect(): #maps every station to the next station it will go to and vice versa
    connect = {}
    for i in mrt:
        station = i[1].split(" <-> ")
        station1_code, station1_name = station[0].split(" ", 1)
        station2_code, station2_name = station[1].split(" ", 1)
        if station1_name not in connect:
            connect[station1_name] = []
        if station2_name not in connect:
            connect[station2_name] = []
        if station1_name not in connect[station2_name]:
            connect[station2_name].append(station1_name)
        if station2_name not in connect[station1_name]:
            connect[station1_name].append(station2_name)
    return(connect)

def bfs_shortest_path(connect, start, end): #Finding the shortest path to the destination
    queue = [[start]] #Holds the path
    visited = set() #Keeps track of visited stations
    while queue:
        path = queue.pop(0) #Gets the oldest path in the queue
        station = path[-1] #Gets the last station from the path
        if station == end:
            return path #Found the shortest path
        if station not in visited:
            visited.add(station)
            for nextstation in connect.get(station, []):
                if nextstation not in visited:
                    new_path = list(path) #list(path) == path + [nextstation]
                    new_path.append(nextstation)
                    queue.append(new_path)
    return None
        
def opt2(): #Find the best route between two stations
    print("\nPlease enter the station you want to start at")
    startstation = input("Start Station: ")
    while startstation.lower() not in stations:
        print("That station does not exist!")
        print("Please try again! >_<")
        startstation = input("\nStart Station: ")
    print("\nPlease enter the station you want to end at")
    endstation = input("End Station: ")
    while endstation.lower() not in stations:
        print("That station does not exist!")
        print("Please try again! >_<")
        endstation = input("\nEnd Station: ")
    while startstation.lower() == endstation.lower():
        print("\nYou cannot end at the same station!")
        print("Please select another end station!")
        endstation = input("\nEnd Station: ")
    connected = stationconnect()
    path = bfs_shortest_path(connected, startstation.title(), endstation.title())
    if path is None:
        print(f"No path was found from {startstation.title()} to {endstation.title()}")
    else:
        print("\nShortest path:")
        for station in path:
            code = get_all_station_code(station)
            print(f"{' -> ' if station != path[0] else ''}{code} {station}", end="")
        print()
    return(path)
    
def opt3(): #Distance and time of travel between 2 stations
    path = opt2()
    

def opt4(): #Whether there is a train running and if it will arrive at your destination station before the last train time
    print()

def opt5(): #What MRT line the station is at
    print("\nWhich station would you like to know about?")
    station = input(">>> ")
    while station.lower() not in stations:
        print("That station does not exist!")
        print("Please try again! >_<")
        station = input(">>> ")
    possiblelines = []
    for i in mrtlines:
        if i[0] == station.title():
            possiblelines.append(i[1])
    print(f"\n{station} station belongs to the following line(s):")
    for i in possiblelines:
        print(f"{i} line")

def opt6(): #Find the fare required from Station A to B during peak hours
    print()

def main():
    if len(mrt) == 0:
        readingfiles()
    mainscreen()
    choice = input(">>> ")
    while choice not in choices:
        print("\nThat is not a valid option!")
        print("Please try again! >_<")
        choice = input(">>> ")
    if choice == choices[0]:
        opt1()
    if choice == choices[1]:
        opt2()
    if choice == choices[2]:
        opt3()
    if choice == choices[3]:
        opt4()
    if choice == choices[4]:
        opt5()
    if choice == choices[5]:
        opt6()
    
while True:
    main()
    print("\nWould you like to continue? (y/n)")
    resume = input(">>> ")
    while str(resume).lower() != "yes" and str(resume).lower() != "y" and str(resume).lower() != "no" and str(resume).lower() != "n":
        print("\nThat is not a valid option!")
        print("Please try again! >_<")
        resume = input(">>> ")
    if "y" in resume:
        continue
    else:
        break
