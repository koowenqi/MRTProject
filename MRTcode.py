from datetime import datetime, timedelta

mrt = [] #Stores each line from MRT.txt into a list (raw data) (e.g. 1;CC1 Dhoby Ghaut <-> CC2 Bras Basah;Circle;0.6;0607;2357;0554;0003)
lines = [] #Stores all the different lines (e.g. Circle, North East)
stations = [] #Stores all the different stations (e.g. dhoby ghaut, bras basah)
mrtlines = [] #Stores the line each station corresponds with (e.g. ["Dhoby Ghaut", "Circle"])
stationcat = {} #Assigns the line each MRT code corresponds with (e.g. "CC1": "Circle")
mrtdict = {} #Assigns each MRT code to the station (e.g. "CC1": "Dhoby Ghaut")
speeddict = {} #speed of each line
fares = {"adult": [], "senior": [], "student": []} #Fare for each age category (e.g. adult = [0.0, 3.2, 119])

line_prefixes = {
    "CC": "Circle",
    "NS": "North-South",
    "EW": "East-West",
    "DT": "Downtown",
    "NE": "North East",
    "TE": "Thomson-East Coast"
}
choices = ["1", "2", "3", "4", "5", "6"] #All the possible choices the user can make

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

    speedfile = open("MRT speed.txt", "r")
    speedfile.seek(0)
    for line in speedfile:
        i = line.split(";")
        speeddict[i[0]] = int(i[1].strip())
    speedfile.close()

    farefile = open("Fare Structure.txt", "r")
    farefile.seek(0)
    current_cat = None
    for line in farefile:
        i = line.strip()
        if not i or i.endswith(":"):
            continue
        if "Adult" in line:
            current_cat = "adult"
            continue
        if "Senior" in line:
            current_cat = "senior"
            continue
        if "Student" in line:
            current_cat = "student"
            continue

        if current_cat and ";" in line:
            distance, fare = line.split(";")
            if fare.isdigit():
                fare = int(fare)
                if "Up to" in distance:
                    upper = float(distance.split(" ")[-2])
                    fares[current_cat].append(0.0, upper, fare)
                if "Over" in distance:
                    lower = float(distance.split(" ")[-2]) + 0.1
                    fares[current_cat].append((lower, float("inf"), fare))
                else:
                    lower, upper = distance.split(" - ")
                    fare[current_cat].append(float(lower), float(upper), fare)

#Function to sort the stations
def sort_key(item):
     # Extract the prefix and numeric part
    prefix = item[0][:2]
    number = 0  # Default number for prefixes with no number (e.g. "CG")
    
    # Check if the prefix has a numeric part after it (e.g. CC1)
    if len(item[0]) > 2 and item[0][2:].isdigit():
        number = int(item[0][2:])
    return (prefix, number)

#Function to check user input for line
def recogniseline(user):
    user = user.strip()
    if user.upper() in line_prefixes:
        return line_prefixes[user.upper()]
    if user.lower().capitalize() in lines:
        return user.lower().capitalize()
    return None

#Function to check if the user input is valid for MRT code and station
def recogniseinput(user): #Recognises user input if it is MRT code or the name
    user = user.strip()
    if user.upper() in mrtdict:
        return mrtdict[user.upper()]
    if user.lower() in stations:
        return user.lower().capitalize()
    return None

#Function to get all the codes for a given station
def get_all_station_code(name):
    codes = []
    for code in mrtdict:
        if mrtdict[code].lower() == name.lower():
            codes.append(code)
    return "/".join(codes) if codes else None

#Function to get the distance between side by side stations
def get_distance_between(s1, s2):
    for i in mrt:
        s = i[1].split(" <-> ")
        name1 = s[0].split(" ", 1)[1]
        name2 = s[1].split(" ", 1)[1]
        if (s1 == name1 and s2 == name2) or (s1 == name2 and s2 == name1):
            return float(i[3]), i[2]  # distance, line
    return 0.0, None

#Function to print the mainscreen
def mainscreen():
    print("\nWelcome to the MRT Information Centre!")
    print("What would you like to enquire about?")
    print("1. List every station in an MRT line")
    print("2. Find the best route between two stations")
    print("3. Distance and time of travel between two stations")
    print("4. Whether there is a train running and if it will arrive at your destination station before the last train time")
    print("5. What MRT line is your station on")
    print("6. Find the fare required from Station A to B")

#List every station of an MRT line
def opt1(): 
    templist = []
    print("\nWhat is the MRT line you would like to enquire about?")
    print("Here is a list of lines that you can inquire about:")
    for i in lines:
        print(f"{i.capitalize()} - {next(k for k, v in line_prefixes.items() if v.lower() == i)}")
    line = None
    while not line:
        user = input("\n>>> ").strip()
        print(user)
        line = recogniseline(user)
        if not line:
            print("\nThat is not a valid option!")
            print("Please try again! >_<")
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

#Maps every station to the next station it will go to and vice versa
def stationconnect(): 
    connect = {}
    for i in mrt:
        station = i[1].split(" <-> ")
        s1_name = station[0].split(" ", 1)[1]
        s2_name = station[1].split(" ", 1)[1]
        distance = float(i[3])
        if s1_name not in connect:
            connect[s1_name] = []
        if s2_name not in connect:
            connect[s2_name] = []
        if s1_name not in [s for s, _ in connect[s2_name]]:
            connect[s2_name].append((s1_name, distance))
        if s2_name not in [s for s, _ in connect[s1_name]]:
            connect[s1_name].append((s2_name, distance))
    return(connect)

#Finding the shortest path to the destination
def shortest_path(connect, start, end):
    unvisited = list(connect.keys())
    distance = {station: float('inf') for station in connect} #initialises every station to infinity because I dont know how far the station is yet
    previous = {station: None for station in connect} #tracks the previous station you came from (previous["Bishan"] = "Marymount" means we reached Bishan from Marymount)
    distance[start] = 0 #we start at 0 distance
    while unvisited:
        current = None
        current_dist = float("inf")
        for station in unvisited:
            if distance[station] < current_dist:
                current = station
                current_dist = distance[station]
        if current is None or current == end:
            break

        unvisited.remove(current)

        for nextstation, dist in connect[current]:
            if nextstation in unvisited:
                new_dist = distance[current] + dist
                if new_dist < distance[nextstation]:
                    distance[nextstation] = new_dist
                    previous[nextstation] = current

    path = []
    curr = end
    while curr:
        path.insert(0, curr)
        curr = previous[curr]
    
    return path, distance[end]

#Function to take in startstation and end station and calculate shortest path
def calcbestroute():
    print("\nPlease enter the station you want to start at")
    startstation = None
    while not startstation:
        user = input("Start Station: ").strip()
        startstation = recogniseinput(user)
        if not startstation:
            print("That station does not exist!")
            print("Please try again! >_<")
    print(f"Start Station selected: {startstation}")
    
    print("\nPlease enter the station you want to end at")
    endstation = None
    while not endstation:
        user = input("End Station: ").strip()
        endstation = recogniseinput(user)
        if not endstation or startstation.lower() == endstation.lower():
            if startstation.lower() == endstation.lower():
                print("\nYou cannot end at the same station!")
                print("Please select another end station!")
            else:
                print("That station does not exist!")
                print("Please try again! >_<")
            endstation = None
    print(f"End Station selected: {endstation}")

    connected = stationconnect()
    path, total_distance = shortest_path(connected, startstation.title(), endstation.title())

    if not path:
        print(f"No path was found from {startstation.title()} to {endstation.title()}")
        return
    
    return startstation, endstation, path, total_distance

#Parses time in HHMM format to datetime.time
def parse_time(t):
    return datetime.strptime(t.strip(), "%H%M").time()

#Returns the parsed time from s1 to s2
def get_train_time(s1, s2):
    for i in mrt:
        station = i[1].split(" <-> ")
        name1 = station[0].split(" ", 1)[1]
        name2 = station[1].split(" ", 1)[1]
        if (s1 == name1 and s2 == name2):
            return parse_time(i[4]), parse_time(i[5])
        elif (s1 == name2 and s2 == name1):
            return parse_time(i[6]), parse_time(i[7])
    return None, None

#Get the user input for their time of departure from start station
def get_user_time():
    while True:
        user_time = input("\nEnter your intended departure time in the 24-hours format: ").strip()
        if len(user_time) == 4 and user_time.isdigit():
            try:
                return datetime.strptime(user_time, "%H%M")
            except ValueError:
                pass
        print("You have entered an invalid timing, please try again!")

#Gets the fare for a certain distance and age category
def get_fare(distance, cat, fare):
    for lower, upper, price in fares[cat]:
        if lower <= distance <= upper:
            return price
    return None

#Find the shortest route between two stations
def opt2(): 
    startstation, endstation, path, total_distance = calcbestroute()
    
    print("\nRoute:")
    prev_line = None
    line_segment = []
    first_line_printed = False
    for i in range(len(path)):
        station = path[i]
        code = get_all_station_code(station)
        current_line = None

        if i < len(path) - 1:
            distance, current_line = get_distance_between(path[i], path[i + 1])
        elif i > 0:
            distance, current_line = get_distance_between(path[i - 1], path[i])

        if prev_line and (current_line != prev_line or i == len(path) - 1):
            if i == len(path) - 1:
                line_segment.append(f"{code} {station}")
            if not first_line_printed:
                print(f"On {prev_line} Line")
                first_line_printed = True
            else:
                print(f"\nTransfer to {prev_line} Line")
            print(" -> ".join(line_segment))
            line_segment = []
        
        if i == 0 or current_line == prev_line or prev_line is None:
            line_segment.append(f"{code} {station}")
        prev_line = current_line

    if not first_line_printed:
        print(f"On {prev_line} Line")
        print(" -> ".join(line_segment))
    elif line_segment:
        print(" -> ".join(line_segment))
    return(path, total_distance)

#Distance and time of travel between 2 stations
def opt3(): 
    path, distance = opt2()
    total_time = 0.0
    for i in range(len(path) - 1):
        d, line = get_distance_between(path[i], path[i + 1])
        prev_line = None
        if i > 0:
            _, prev_line = get_distance_between(path[i - 1], path[i])
        segment_time = 0.0
        if i < len(path) - 1:
            if line and line in speeddict and speeddict[line] != 0:
                total_time += d / speeddict[line] * 60 + 4 #include waiting time for alighting and boarding per station
        if prev_line and line != prev_line:
            segment_time += 3 #transfer from one line to another
        total_time += segment_time
    
    print(f"\nTotal distance: {distance:.2f}km")
    if total_time < 60:
        print(f"Estimated travel time: {total_time:.1f} minutes")
    else:
        print(f"Estimated travel time: {int(total_time // 60)} hour(s) and {int(total_time%60)} minute(s)")
    
#Whether there is a train running and if it will arrive at your destination station before the last train time
def opt4(): 
    startstation, endstation, path, total_distance = calcbestroute()
    currenttime = get_user_time()
    base_date = currenttime.date()
    print(f"\nChecking train availability from {startstation} to {endstation}...")
    total_time = 0.0

    for i in range(len(path) - 1):
        s1 = path[i]
        s2 = path[i+1]
        dist, line = get_distance_between(s1, s2)
        segment_time = 0.0
        if line in speeddict and speeddict[line] != 0:
            segment_time = dist / speeddict[line] * 60 + 4
        if i > 0:
            _, prev_line = get_distance_between(path[i - 1], s1)
            if prev_line != line:
                segment_time += 3 #additional transfer time

        firsttrain, lasttrain = get_train_time(s1, s2)
        firsttrain_dt = datetime.combine(base_date, firsttrain)
        lasttrain_dt = datetime.combine(base_date, lasttrain)
        if lasttrain < firsttrain:
            lasttrain_dt += timedelta(days=1)
        arrival_dt = currenttime + timedelta(minutes=total_time + segment_time)
        if currenttime < firsttrain_dt or currenttime > lasttrain_dt:
            print(f"No train running from {s1} to {s2} (Service hours: {firsttrain.strftime('%H:%M')} - {lasttrain.strftime('%H:%M')})")
            return
        if arrival_dt > lasttrain_dt:
            print(f"Journey cannot be completed: You will reach {s2} at {arrival_dt.strftime('%H:%M')}, but the last train departs at {lasttrain.strftime('%H:%M')}")
            print(f"This means the journey fails from: {s1} → {s2}")
            print("As a result, you cannot reach your destination on time.")
            delay = (arrival_dt - lasttrain_dt).seconds // 60
            print(f"You are {delay} minutes late for the last train to {s2}. Consider departing earlier.")
            latest_departure = lasttrain_dt - timedelta(minutes=segment_time)
            print(f"You must depart before {latest_departure.strftime('%H:%M')} to catch the last train to {s2}.")
            print(f"You can only reach up to {s1} based on your current departure time.")
            return
        
        total_time += segment_time

    final_arrival = (currenttime + timedelta(minutes=total_time)).time()
    print(f"A train is currently running, and you will reach {endstation} at around {final_arrival.strftime('%H:%M')} if you depart now.")

#What MRT line the station is at
def opt5(): 
    print("\nWhich station would you like to know about?")
    station = None
    while not station:
        user = input(">>> ").strip()
        station = recogniseinput(user)
        if not station:
            print("That station does not exist!")
            print("Please try again! >_<")
    possiblelines = []
    stationcodes = []
    for i in mrtlines:
        if i[0].lower() == station.lower():
            for code1, name in mrtdict.items():
                for code2, line in stationcat.items():
                    if name.lower() == station.lower() and code1 == code2 and line == i[1]:
                        stationcodes.append(code1)
                        possiblelines.append(line)
    print(f"\n{station} station belongs to the following line(s):")
    for i in range(len(possiblelines)):
        print(f"{possiblelines[i]} line ({stationcodes[i]})")

#Find the fare required from Station A to B
def opt6(): 
    start, end, path, distance = calcbestroute()
    print(fares)
    print("\nWhat is your age category (Adult, Student, Senior)?")
    cat = input("Enter age category: ").strip()
    while str(cat).lower() not in fares:
        print("\nThat is not a valid age category!")
        print("Please try again! >_<")
        cat = input("\nEnter age category: ").strip()
    print(f"Age Category selected: {cat.lower().capitalize()}")
    print("\nIs it peak or off peak hours? (y/n)")
    print("Peak hours: Before 7.45am")
    peak = input(">>> ").strip()
    while str(peak).lower() != "yes" and str(peak).lower() != "y" and str(peak).lower() != "no" and str(peak).lower() != "n":
        print("\nThat is not a valid option!")
        print("Please try again! >_<")
        peak = input(">>> ").strip()
    if "y" in peak.lower():
        peakh = True
    else:
        peakh = False

    fare = get_fare(distance, cat, fares)
    if peakh:
        fare -= 50.0
    if fare < 0.0:
        fare = 0.0
    if fare > 99:
        print(f"The total fare is: {fare//100} dollar(s) and {fare%100} cent(s)")
    else:
        print(f"The total fare is: {fare} cent(s)")

#The main function that compiles all the options together
def main():
    if len(mrt) == 0:
        readingfiles()
    mainscreen()
    choice = input(">>> ").strip()
    while choice not in choices:
        print("\nThat is not a valid option!")
        print("Please try again! >_<")
        choice = input(">>> ").strip()
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
    resume = input(">>> ").strip()
    while str(resume).lower() != "yes" and str(resume).lower() != "y" and str(resume).lower() != "no" and str(resume).lower() != "n":
        print("\nThat is not a valid option!")
        print("Please try again! >_<")
        resume = input(">>> ").strip()
    if "y" in resume.lower():
        continue
    else:
        break
