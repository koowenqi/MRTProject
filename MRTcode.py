mrt = []
lines = []
mrtlines = []
stationcat = {}
mrtdict = {}
speeddict = {}

choices = ["1", "2", "3", "4", "5", "6"]

def readingfiles():
    mrtfile = open("MRT.txt", "r")
    mrtfile.seek(0)
    for position,line in enumerate(mrtfile):
        i = line.split(";")
        if position <= 4:
            continue
        else:
            mrt.append(i)
        if i[2] not in lines:
            lines.append(i[2])
    mrtfile.close()

    linesfile = open("MRT lines.txt", "r")
    linesfile.seek(0)
    for line in linesfile:
        i = line.split(";")
        mrtdict[i[0]] = i[1]
        mrtlines.append([i[1], i[2].strip()])
        stationcat[i[0]] = i[2].strip()
    linesfile.close()

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
    print("\nWhat is the MRT line you would like to enquire about?")
    print("Here is a list of lines that you can inquire about:")
    for i in lines:
        print(i)
    line = input(">>> ")
    while line not in lines:
        print("\nThat is not a valid option!")
        print("Please try again! >_<")
        line = input(">>> ")
    print(f"Here is a list of station in the {line} line")
    for i in mrtlines:
        if line == i[1]:
            for k1, v1 in mrtdict.items():
                for k2, v2 in stationcat.items():
                    if v1 == i[0] and v2 == i[1] and k1 == k2:
                        print(f"{k1} {v1}")
                        break

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
