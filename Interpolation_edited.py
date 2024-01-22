'''
How the code works:
1. The data file is parsed to handle format errors in data (i.e. data is not in 44x44 matrices)
2. Deadspots are identified by their force of 0 in all frames
3. Interpolate data using average of surrounding cells
4. Calculate new force sums of interpolated frames
5. Plot
6. Options to get interpolated force sum of specific frame/max force sum of entire dataset (comment out if unwanted)
'''

import csv
import numpy as np
import matplotlib.pyplot as plt

def parse_data(file_path):
    """
    Parses csv/text file and ensures each frame is 44x44.
    Missing values are filled with zeros.
    """
    # CSV FILE start --------------------------------------------------------------------------------------------------------
    frames = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        current_frame = []
        for row in csvreader:
            if row and row[0].startswith('Frame'):
                if current_frame:
                    while len(current_frame) < 44:
                        current_frame.append([0] * 44)
                    frames.append(np.array(current_frame[:44]))
                    current_frame = []
            else:
                force_values = [int(value) if value.isdigit() else 0 for value in row]
                if len(force_values) < 44:
                    force_values.extend([0] * (44 - len(force_values)))
                if force_values:
                    current_frame.append(force_values[:44])
    # comment up to here if using text file                
    # TEXT FILE start -------------------------------------------------------------------------------------------------------
    # frames = []
    # with open(file_path, 'r') as file:
    #     current_frame = []
    #     for line in file:
    #         if line.startswith('Frame'):
    #             if current_frame:
    #                 while len(current_frame) < 44:
    #                     current_frame.append([0] * 44)
    #                 frames.append(np.array(current_frame[:44]))
    #                 current_frame = []
    #         else:
    #             # try-except block for non-numeric values
    #             force_values = []
    #             for value in line.strip().split(','):
    #                 try:
    #                     force_values.append(int(value))
    #                 except ValueError:
    #                     force_values.append(0)  # Replace non-numeric values with 0

    #             if len(force_values) < 44:
    #                 force_values.extend([0] * (44 - len(force_values)))
    #             current_frame.append(force_values[:44])
    # comment up to here if using csv file (keep below for both) ----------------------------------------------------------------
       
        if current_frame:
            while len(current_frame) < 44:
                current_frame.append([0] * 44)
            frames.append(np.array(current_frame[:44]))
    
    return frames

def find_deadspots(frames):
    """
    Identifies deadspots in the sensor data. 
    Deadspots are identified by their consistent force value of 0.
    """
    stacked_frames = np.stack(frames)
    deadspots = np.all(stacked_frames == 0, axis=0)
    return deadspots

def interpolate_frames(frames, deadspots):
    """
    Interpolates each frame for the deadspots using average of surrounding cells.
    Surrounding cells are top, bottom, left, right and diagonals.
    """
    interpolated_frames = []

    for frame in frames:
        interpolated_frame = np.copy(frame)
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if deadspots[i, j]:
                    surrounding = frame[max(i-1, 0):min(i+2, frame.shape[0]), max(j-1, 0):min(j+2, frame.shape[1])]
                    interpolated_frame[i, j] = np.mean(surrounding[surrounding != 0]) if np.any(surrounding != 0) else 0
        interpolated_frames.append(interpolated_frame)

    return interpolated_frames

def sum_interpolated_frames(interpolated_frames):
    """
    Calculates the sum of forces for each interpolated frame.
    """
    force_sums = [np.sum(frame) for frame in interpolated_frames]
    return force_sums

# MAIN EXECUTION

# keep 1 of the 2 data file paths below (comment the other one out)-----------------------------------
# data_file_path = '/Users/vanessachen/Documents/VS Code/F23 URA/data.txt' 
data_file_path = '/Users/vanessachen/Documents/VS Code/F23 URA/151L-hard-50j_M.csv'
frames = parse_data(data_file_path)
deadspots = find_deadspots(frames)
interpolated_frames = interpolate_frames(frames, deadspots)
force_sums = sum_interpolated_frames(interpolated_frames)

# Plotting the force sum vs frame number
plt.figure(figsize=(10, 6))
plt.plot(force_sums, marker='o')
plt.title('Force Sum vs Frame Number')
plt.xlabel('Frame Number')
plt.ylabel('Force Sum')
plt.grid(True)
plt.show()

# Get the force sum for a specific frame
frame_number = 531
frame_index = frame_number
if frame_index < len(force_sums):
    print(f"Force sum for frame {frame_number}: {force_sums[frame_index]}")
else:
    print(f"Frame {frame_number} is not available in the data.")

# Get max interpolated force sum from dataset
max_sum = max(force_sums)
maxsum_index = force_sums.index(max_sum)
print(f"Highest Interpolated Force Sum: {max_sum} (in frame {maxsum_index})")
