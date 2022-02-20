#This is leftover, can remove afaik - Will
import csv

with open('BOARD.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    array = list(reader)

    print(array)