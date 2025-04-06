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

def opt1():
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

def opt2():
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
    firststation = []
    laststation = []
    for i in mrtlines:
        if i[0] == startstation.title():
            firststation.append(i)
        if i[0] == endstation.title():
            laststation.append(i)
    line1 = {i[1] for i in firststation}
    line2 = {i[1] for i in laststation}
    commonline = line1 & line2
    if commonline: #if they possess the same line (e.g. you want to go from Seragoon (North East) to Sengkang (North East))
        firststation = [i for i in firststation if i[1] in commonline]
        laststation = [item for item in laststation if item[1] in commonline]
        temp = []
        bestroute = []
        for i in mrt:
            station = i[1].split(" <-> ")
            station1_code, station1_name = station[0].split(" ", 1)
            station2_code, station2_name = station[1].split(" ", 1)
            line = i[2]
            if station1_name == firststation[0][0] and line == firststation[0][1]:
                temp.append(i)
        station = temp[0][1].split(" <-> ")
        station1_code, station1_name = station[0].split(" ", 1)
        station2_code, station2_name = station[1].split(" ", 1)
        bestroute.append([station1_code, station1_name])
        bestroute.append([station2_code, station2_name])
        while True:
            if bestroute[-1][1] == endstation.title():
                break
            for i in mrt:
                station = i[1].split(" <-> ")
                station1_code, station1_name = station[0].split(" ", 1)
                station2_code, station2_name = station[1].split(" ", 1)
                line = i[2]
                if station1_name == bestroute[-1][1] and line == firststation[0][1]:
                    bestroute.append([station2_code, station2_name])
                    break
        print("\nYour best route would be: ")
        for i in bestroute:
            print(f"{i[0]} {i[1]}")
    else: #if they dont possess the same line (e.g. you want to go from Sengkang (North East) to Little India (Downtown))
        print("Not implemented yet sorry!")

    # for i in mrt:
    #     station = i[1].split(" <-> ")
    #     station1_code, station1_name = station[0].split(" ", 1)
    #     if station1_name.lower() == startstation.lower():
    #         temp.append(i)
    # fastest = min(float(i[3]) for i in temp)
    # shortestroute = [i for i in temp if float(i[3]) == fastest]
    # station = shortestroute[0][1].split(" <-> ")
    # station1_code, station1_name = station[0].split(" ", 1)
    # station2_code, station2_name = station[1].split(" ", 1)
    # print(station1_name)
    # print(station2_name)
    # if len(bestroute) == 0:
    #     bestroute.append([station1_code, station1_name])
    #     bestroute.append([station2_code, station2_name])
    # else:
    #     bestroute.append([station2_code, station2_name])

    # while True:
    #     if bestroute[-1] == endstation:
    #         break
    #     temp = []
    #     for i in mrt:
    #         station = i[1].split(" <-> ")
    #         station1_code, station1_name = station[0].split(" ", 1)
    #         if station1_name.title() == bestroute[-1][1]:
    #             temp.append(i)
    #     fastest = min(float(i[3]) for i in temp)
    #     shortestroute = [i for i in temp if float(i[3]) == fastest]
    #     station = shortestroute[0][1].split(" <-> ")
    #     station1_code, station1_name = station[0].split(" ", 1)
    #     station2_code, station2_name = station[1].split(" ", 1)
    #     print(station1_name)
    #     print(station2_name)
    #     if len(bestroute) == 0:
    #         bestroute.append([station1_code, station1_name])
    #         bestroute.append([station2_code, station2_name])
    #     else:
    #         bestroute.append([station2_code, station2_name])
    # print(bestroute)

def opt3():
    print()

def opt4():
    print()

def opt5():
    print()

def opt6():
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
