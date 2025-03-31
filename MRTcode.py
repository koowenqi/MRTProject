mrt = []
lines = []
mrtlines = [] #["Dhoby Ghaut", "Circle"]
stationcat = {} #"CC1": "Circle"
mrtdict = {} #"CC1": "Dhoby Ghaut"
speeddict = {}

choices = ["1", "2", "3", "4", "5", "6"]

def sort_key(item):
    # Extract the prefix and numeric part
    prefix = item[0][:2]
    number = int(item[0][2:])
    return (prefix, number)

def readingfiles():
    mrtfile = open("MRT.txt", "r")
    mrtfile.seek(0)
    for position,line in enumerate(mrtfile):
        i = line.split(";")
        if position <= 4:
            continue
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
    print()

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
