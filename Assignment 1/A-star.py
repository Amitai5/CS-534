import csv

#load board

with open('test.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    array = list(reader)

    size = len(array)

    print(array)
    print(size)
#add 1st node

#while not solved
while True:
    #open lowest cost

    #switch it to closed

    #Generate successors
    for i in range(1,size):
        print(i,array[i][i]);

    #If solved exit
    break