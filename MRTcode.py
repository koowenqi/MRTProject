from datetime import datetime, timedelta
import mrtturtle

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
choices = ["1", "2", "3", "4", "5", "6", "7", "8"] #All the possible choices the user can make

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
        if i[2].lower().title() not in lines:
            lines.append(i[2].lower().title())
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
        if "Adult" in i:
            current_cat = "adult"
            continue
        if "Senior" in i:
            current_cat = "senior"
            continue
        if "Student" in i:
            current_cat = "student"
            continue

        if current_cat and ";" in i:
            distance, fare = i.split(";")
            if fare.isdigit():
                fare = int(fare)
                if "Up to" in distance:
                    upper = float(distance.split(" ")[-2])
                    fares[current_cat].append((0.0, upper, fare))
                elif "Over" in distance:
                    lower = float(distance.split(" ")[-2]) + 0.1
                    fares[current_cat].append((lower, float("inf"), fare))
                else:
                    lower, upper = distance.split(" - ")
                    lower = lower.split(" ", 1)[0]
                    upper = upper.split(" ", 1)[0]
                    fares[current_cat].append((float(lower), float(upper), fare))

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
    if user.lower().title() in lines:
        return user.lower().title()
    return None

#Function to check if the user input is valid for MRT code and station
def recogniseinput(user): #Recognises user input if it is MRT code or the name
    user = user.strip()
    if user.upper() in mrtdict:
        return mrtdict[user.upper()]
    if user.lower() in stations:
        return user.lower().title()
    return None

#Function to get all the codes for a given station
def get_all_station_code(name):
    codes = []
    for code in mrtdict:
        if mrtdict[code].lower() == name.lower():
            codes.append(code)
    return "/".join(codes) if codes else None

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
    print("7. Show all interchange stations")
    print("8. First and last train timings for a line, station or all the stations")

#List every station of an MRT line
def opt1(): 
    templist = []
    print("\nWhat is the MRT line you would like to enquire about?")
    print("Here is a list of lines that you can inquire about:")
    for i in lines:
        print(f"{i} - {next(k for k, v in line_prefixes.items() if v == i)}")
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
    mrtturtle.draw_mrt_line(line, templist)

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
            print("\nThat station does not exist!")
            print("Please try again! >_<")
    print(f"Start Station selected: {startstation}")
    
    print("\nPlease enter the station you want to end at")
    endstation = None
    while not endstation:
        user = input("End Station: ").strip()
        endstation = recogniseinput(user)
        if not endstation:
            print("\nThat station does not exist!")
            print("Please try again! >_<")
        if endstation:
            if startstation.lower() == endstation.lower():
                print("\nYou cannot end at the same station!")
                print("Please select another end station!")
    print(f"End Station selected: {endstation}")

    connected = stationconnect()
    path, total_distance = shortest_path(connected, startstation.title(), endstation.title())

    if not path:
        print(f"No path was found from {startstation.title()} to {endstation.title()}")
        return
    
    return startstation, endstation, path, total_distance

#Find the shortest route between two stations
def opt2(draw=True): 
    startstation, endstation, path, total_distance = calcbestroute()
    print("\nRoute:")
    prev_line = None
    currentlinelist = []
    current_segment = []
    for i in range(len(path)):
        station = path[i]
        code = get_all_station_code(station)
        current_line = None

        if i < len(path) - 1:
            distance, current_line = get_distance_between(path[i], path[i + 1])
        elif i > 0:
            distance, current_line = get_distance_between(path[i - 1], path[i])

        currentlinelist.append(current_line)
        current_segment.append(f"{code} {station}")
        # If line changes or it's the last station, print the segment
        line_changed = current_line != prev_line and prev_line is not None
        is_last = i == len(path) - 1

        if line_changed or is_last:
            if prev_line is None:
                print(f"On {current_line} Line")
            else:
                print(f"\nTransfer to {prev_line} Line")

            print(" -> ".join(current_segment))
            current_segment = []

        prev_line = current_line
    if draw:
        mrtturtle.draw_bestroute(path, currentlinelist)
        mrtturtle.write_route_info(path, currentlinelist, startstation, endstation, None, None)
    return(path, total_distance, currentlinelist, startstation, endstation)

#Function to get the distance between side by side stations
def get_distance_between(s1, s2):
    for i in mrt:
        s = i[1].split(" <-> ")
        name1 = s[0].split(" ", 1)[1]
        name2 = s[1].split(" ", 1)[1]
        if (s1 == name1 and s2 == name2) or (s1 == name2 and s2 == name1):
            return float(i[3]), i[2]  # distance, line
    return 0.0, None

#Distance and time of travel between 2 stations
def opt3(): 
    path, distance, currentlinelist, startstation, endstation = opt2(draw=False)
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
    
    mrtturtle.draw_bestroute(path, currentlinelist)
    mrtturtle.write_route_info(path, currentlinelist, startstation, endstation, total_time, distance)
    
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

#Whether there is a train running and if it will arrive at your destination station before the last train time
def opt4(): 
    startstation, endstation, path, total_distance = calcbestroute()
    currentlinelist = []
    prev_line = None
    for i in range(len(path)):
        if i < len(path) - 1:
            _, current_line = get_distance_between(path[i], path[i + 1])
        elif i > 0:
            _, current_line = get_distance_between(path[i - 1], path[i])
        else:
            current_line = None
        currentlinelist.append(current_line)
    currenttime = get_user_time()
    base_date = currenttime.date()
    print(f"\nChecking train availability from {startstation} to {endstation}...")
    cumulative_time = 0.0 #Cumulative time from start to current segment
    lasttrain_dt = None

    for i in range(len(path) - 1):
        s1 = path[i]
        s2 = path[i+1]
        dist, line = get_distance_between(s1, s2)
        segment_time = 0.0
        if line in speeddict and speeddict[line] != 0:
            segment_time = dist / speeddict[line] * 60 + 4 #+4 adds in alighting/boarding time
        if i > 0:
            _, prev_line = get_distance_between(path[i - 1], s1)
            if prev_line != line:
                segment_time += 3 #Additional transfer time
        cumulative_time += segment_time
        
        #Saves last train timing from first to second station
        if i == 0:
            firsttrain, lasttrain = get_train_time(s1, s2)
            lasttrain_dt = datetime.combine(base_date, lasttrain)
            if lasttrain < datetime.strptime("0400", "%H%M").time():
                lasttrain_dt += timedelta(days=1)

        #Projected arrival time to final station
    projected_arrival_time = currenttime+timedelta(minutes=cumulative_time)

    travel_hours = int(cumulative_time // 60)
    travel_minutes = int(cumulative_time % 60)
    time_msg = (
        f"{travel_hours} hour(s) and {travel_minutes} minute(s)"
        if travel_hours > 0 else
        f"{travel_minutes} minute(s)"
    )
    latest_departure = lasttrain_dt - timedelta(minutes=cumulative_time)
    if projected_arrival_time <= lasttrain_dt:
        ontime = True
        print(f"You will reach {endstation} at around {projected_arrival_time.strftime('%H:%M')}, which is within operating hours.")
        print(f"Total travel time: {time_msg}")
        mrtturtle.draw_limited_route(path, currentlinelist, len(path) - 1)
    else:
        ontime = False
        delay = (projected_arrival_time - lasttrain_dt).seconds // 60
        delay_hours = int(delay // 60)
        delay_minutes = int(delay % 60)
        delay_msg = (
            f"{delay_hours} hour(s) and {delay_minutes} minute(s)"
            if delay_hours > 0 else
            f"{delay_minutes} minute(s)"
        )
        print("The journery cannot be completed in time.")
        print(f"You will reach {endstation} at {projected_arrival_time.strftime('%H:%M')}, but the last train departs at {lasttrain_dt.strftime('%H:%M')}.")
        print(f"Total travel time needed: {time_msg}")
        print(f"You are {delay_msg} minutes late.")
        print(f"You must depart from {startstation} before {latest_departure.strftime('%H:%M')} to reach {endstation} on time.")
        reachable_index = 0
        current_time = currenttime
        for i in range(len(path) - 1):
            s1 = path[i]
            s2 = path[i + 1]
            d, line = get_distance_between(s1, s2)
            seg_time = d / speeddict[line] * 60 + 4
            if i > 0:
                _, prev_line = get_distance_between(path[i - 1], s1)
                if line != prev_line:
                    seg_time += 3
            current_time += timedelta(minutes=seg_time)
            if current_time <= lasttrain_dt:
                reachable_index = i + 1
            else:
                break
        mrtturtle.draw_limited_route(path, currentlinelist, reachable_index)
    mrtturtle.write_time_check_info(startstation, endstation, projected_arrival_time, lasttrain_dt, cumulative_time, latest_departure, ontime)

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

    mrtturtle.draw_station_info_graphics(station, possiblelines, stationcodes)

#Gets the fare for a certain distance and age category
def get_fare(distance, cat, fare):
    for lower, upper, price in fares[cat]:
        if lower <= distance <= upper:
            return price
    return None

#Find the fare required from Station A to B
def opt6():
    start, end, path, distance = calcbestroute()
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
    print(f"\nThe total distance is: {distance:.1f} km")
    if fare > 99:
        print(f"The total fare is: {fare//100:.0f} dollar(s) and {fare%100:.0f} cent(s)")
    else:
        print(f"The total fare is: {fare:.0f} cent(s)")
    
    mrtturtle.draw_fare_info(start, end, cat, peakh, distance, fare)

#Show all interchange stations
def opt7():
    print("\nDo you want to know a specific line's interchange or every interchange?")
    print("Enter the line name, code, or all for every interchange")
    allselected = False
    line = None
    while not line:
        user = input(">>> ").strip()
        if user.lower() == "all":
            allselected = True
            break
        line = recogniseline(user)
        if not line:
            print("\nThat is not a valid option!")
            print("Please try again! >_<")
    interchanges = []
    for i in stations:
        count = 0
        temp = []
        for x in mrtlines:
            if i == x[0].lower():
                count += 1
                temp.append(x[1])
        if count > 1:
            interchanges.append([i, temp])
    if allselected:
        print("\nHere is a list of all the interchange stations:")
        for i in interchanges:
            print(f" - {i[0].title()}: {', '.join(i[1])}")
        mrtturtle.draw_interchanges(interchanges)
    else:
        print(f"\nHere is a list of all the interchanges of {line} Line:")
        for i in interchanges:
            if line in i[1]:
                print(f" - {i[0].title()}: {', '.join(i[1])}")
        mrtturtle.draw_interchanges(interchanges, line_filter=line)

#Gets all the last train timing to and fro from every station
def get_train_last_timing(): #5 last s1 to s2, 7 last s2 to s1
    lasttraintime = {}
    for i in mrt:
        line = i[2]
        s1_to_s2 = i[5]
        s2_to_s1 = i[7]
        stations = i[1].split(" <-> ")
        s1_code, s1 = stations[0].split(" ", 1)
        s2_code, s2 = stations[1].split(" ", 1)
        if s1 not in lasttraintime:
            lasttraintime[s1] = {}
        if line not in lasttraintime[s1]:
            lasttraintime[s1][line] = []
        lasttraintime[s1][line].append([s2_code, s2, s1_to_s2, s2_to_s1])
        if s2 not in lasttraintime:
            lasttraintime[s2] = {}
        if line not in lasttraintime[s2]:
            lasttraintime[s2][line] = []
        lasttraintime[s2][line].append([s1_code, s1, s2_to_s1, s1_to_s2])
    return lasttraintime

#First and last train timings for a line, station or all the stations
def opt8():
    print("\nPlease input a line, a station, or all for all stations")
    option = None
    allselected = False
    stationselected = False
    lineselected = False
    while not option:
        user = input(">>> ").strip()
        if user.lower() == "all":
            allselected = True
            break
        if recogniseinput(user):
            stationselected = True
            option = recogniseinput(user)
            break
        if recogniseline(user):
            lineselected = True
            option = recogniseline(user)
            break
        if not option:
            print("\nThat is not a valid input!")
            print("Please try again! >_<")
    lasttraintiming = get_train_last_timing()
    if allselected:
        print("\nThe last train timings for all the stations are:")
        for station in lasttraintiming:
            print(f"- {station}:")
            for line in lasttraintiming[station]:
                for i in lasttraintiming[station][line]:
                    to_code, to_station, to_time, from_time = i
                    print(f" - {line}: To {to_code} {to_station} at {to_time[:2]}:{to_time[2:]}, From {to_code} {to_station} at {from_time[:2]}{from_time[2:]}")
        mrtturtle.draw_last_train_info(lasttraintiming, option_type="all")
    if stationselected:
        print(f"\nThe last train timing(s) for {option} is:")
        print(f"- {option}:")
        for station in lasttraintiming:
            if station == option:
                for line in lasttraintiming[station]:
                    for i in lasttraintiming[station][line]:
                        to_code, to_station, to_time, from_time = i
                        print(f" - {line}: To {to_code} {to_station} at {to_time[:2]}:{to_time[2:]}, From {to_code} {to_station} at {from_time[:2]}{from_time[2:]}")
        mrtturtle.draw_last_train_info(lasttraintiming, option_type="station", option_value=option)
    if lineselected:
        print(f"\n The last train timings for {option} Line is:")
        print(f"- {option} Line:")
        for station in lasttraintiming:
            for line in lasttraintiming[station]:
                if line == option:
                    for i in lasttraintiming[station][line]:
                        to_code, to_station, to_time, from_time = i
                        print(f" - {station}: To {to_code} {to_station} at {to_time[:2]}:{to_time[2:]}, From {to_code} {to_station} at {from_time[:2]}{from_time[2:]}")
        mrtturtle.draw_last_train_info(lasttraintiming, option_type="line", option_value=option)

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
    if choice == choices[6]:
        opt7()
    if choice == choices[7]:
        opt8()
    
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
        print("\nRemember to click on the graphics interface to close it!")
        break
import turtle
turtle.exitonclick()
