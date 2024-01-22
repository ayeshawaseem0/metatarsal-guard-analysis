#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3

import sys
import pandas
import numpy as np
import re

def raw_Sum(text):
    pattern = r"Raw Sum=(\d+)"
    match = re.search(pattern, text)
    if match:
        number = int(match.group(1))
        # print(number)
        if number > 2009:
            return True

    return False


with open('data.txt') as file:
    content = file.readlines()
# print(content) # exist 31]

data = []  # list of frames that have raw sums greater than 20
num = 0
matrix = np.zeros((44, 44))
print(matrix)

for line in range(len(content)):
    if "Frame" in content[line] and raw_Sum(content[line]):
        num += 1
        # print(num)
        # print(content[line])
        frame = []
        for i in range(1, 45):
            # print(content[line+1])
            row = content[line+i].replace("0\n", "0").split(',')  # fixing up data and turning into array/list

            frame.append(row)

        frame = np.array(frame)
        frame = frame.astype(np.float64)
        matrix = np.add(matrix, frame)
        # print(matrix)
        # print(frame) 
        data.append(frame)

data = np.array(data)
data = data.astype(np.float64)

def fill_zeros_with_average(matrix):
    for i in range(1, 43):
        for j in range(1, 43):
            if matrix[i, j] == 0:
                neighbours = [matrix[i-1, j], matrix[i+1, j], matrix[i, j-1], matrix[i, j+1]]
                non_zero_neighbours = [x for x in neighbours if x is not None]
#               non_zero_neighbours = [x for x in neighbors if x != 0]
                if non_zero_neighbours:
                    matrix[i, j] = np.mean(non_zero_neighbours)
    return matrix

# fill zero cells with average of surrounding cells
matrix = fill_zeros_with_average(matrix)

# reshape and print the matrix
np.set_printoptions(threshold=np.inf)
reshaped_matrix = matrix.astype(int).reshape(44, 44)
# np.set_printoptions(threshold=np.inf)
np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=np.inf)
np.set_printoptions(formatter={'int': lambda x: f"{x:3}"})

print(reshaped_matrix)
print(len(data))

# for row in reshaped_matrix:
#     print('\t'.join(map(str, row)))


# for row in matrix.astype(int):
    
#     print('\t'.join('{:5}'.format(item) for item in row))
# print('\n'.join(' '.join(map(str, row)) for row in matrix.astype(int)))
# print(len(data))

# for row in matrix.astype(int):
#     print('\t'.join(map(str, row)))
# print(len(data))

# for line in matrix.astype(int):
#     np.set_printoptions(threshold=np.inf)
#     # np.set_printoptions(threshold=sys.maxsize)
#     print(line)
# print(len(data))  # correct length