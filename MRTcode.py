mrttest = []
linesdict = {}

mrtfile = open("MRT schedule data.txt", "r")
mrtfile.seek(0)
for position,line in enumerate(mrtfile):
    if position <= 4:
        continue
    else:
        mrttest.append(line.split(";"))

linesfile = open("MRT lines.txt", "r")
linesfile.seek(0)
for line in linesfile:
    i = line.split(";")
    linesdict[i[0]] = i[1]




# print(mrttest)