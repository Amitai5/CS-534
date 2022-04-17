import csv
import sys
from part1_Q import Agent
import numpy
import pandas as pd
# from oby import Obaro


def main():
    if len(sys.argv) != 6:
        print("Format: rl.py <filename> <reward> <gamma> <time to learn> <movement probability>")
        exit(1)
    else:
        file = sys.argv[1]
        reward_per_action = float(sys.argv[2])
        gamma = float(sys.argv[3])
        time_to_learn = float(sys.argv[4])
        prob_of_moving = float(sys.argv[5])
    print("This program will read in", file)
    print("It will run for", time_to_learn, "seconds")
    print("Its decay rate is", gamma, "and the reward per action is", reward_per_action)
    print("Its transition model will move the agent properly with p =", prob_of_moving)

    #with open(file, newline='') as csvfile:
     #   reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     #   for row in reader:
     #       print(', '.join(row))

    #arr = numpy.genfromtxt(file, delimiter='\t', dtype='str')
    #print(arr)

    # Call your function or Class
    # me = Obaro(file, reward_per_action, gamma, time_to_learn, prob_of_moving)
    # print(me.get_height())
    agent = Agent(file, reward_per_action, gamma, time_to_learn, prob_of_moving)
    agent.play(time_to_learn)




if __name__ == '__main__':
    main()


