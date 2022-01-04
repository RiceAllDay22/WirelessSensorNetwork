DIR = "test/assets/node_data/valid/test"
SIDE_LENGTH = 10
TIME_STEPS = 100

import os
os.chdir(DIR)

count = 0
for x in range(SIDE_LENGTH):
    for y in range(SIDE_LENGTH):
        os.mkdir(str(count))
        os.chdir(str(count))

        f = open("2020-01-01--00.csv", "w")
        f.write("UNIXTIME,CO2\n")

        for t in range(TIME_STEPS):
            f.write(str(1577836800+t)+","+str(int(1000-((x**2+y*2)+100)*.01*t))+"\n")

        count += 1
        os.chdir("../")
