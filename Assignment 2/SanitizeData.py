import statistics
import pandas
import os


def sanitize_data():
    largest_cost = 0
    training_data = []
    training_data_directory = os.getcwd() + "\\trainingData"
    for name in os.listdir(training_data_directory):
        partial_data = pandas.read_pickle(training_data_directory + "\\" + name)
        for data in partial_data:
            features = []
            board = data[0]
            astar_cost = data[1]

            # Create features, first 12 are row of queen in column, weight of queen in row
            totalWeight = 0
            totalAttackWeight = 0
            numAttQueens = 0
            rowPos = []
            heaviestAttacking = 0

            for i in range(len(board)):
                for j in range(len(board)):
                    if board[j][i] != 0:
                        features.append(j / len(board))
                        features.append(board[j][i])
                        totalWeight += board[j][i]
                        rowPos.append(j)

            for i in range(len(board)):
                myRow = rowPos[i]
                # check for attacks
                for j in range(i + 1, 6):
                    if rowPos[j] == myRow or rowPos[j] == myRow + (j - i) or rowPos[j] == myRow - (j - i):
                        numAttQueens += 1
                        heaviestAttacking = max(heaviestAttacking, board[myRow][i], board[rowPos[j]][j])
                        totalAttackWeight += board[myRow][i] + board[rowPos[j]][j]

            # Add last 5 derived features
            features.append(totalAttackWeight / totalWeight)
            features.append(numAttQueens)
            features.append(statistics.stdev(rowPos))
            features.append(heaviestAttacking)
            features.append(totalWeight)

            if astar_cost > largest_cost:
                largest_cost = astar_cost

            sanitized_data = [features, astar_cost]
            training_data.append(sanitized_data)

    # for i in range(len(training_data)):
    #    training_data[i][1] = round(training_data[i][1] / largest_cost, 3)

    return training_data, largest_cost
