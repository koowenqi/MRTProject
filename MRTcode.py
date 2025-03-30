mrttest = []

mrtfile = open("MRT schedule data.txt", "a+")
mrtfile.seek(0)
for position,line in enumerate(mrtfile):
    if position <= 4:
        continue
    else:
        mrttest.append(line)

print(mrttest)