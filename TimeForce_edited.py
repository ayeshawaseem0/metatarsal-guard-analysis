import re #import regular expression model, lets you search for words/patterns in text
import numpy as np #import NumPy, lets you operate on big arrays/matrices
import matplotlib.pyplot as plt #import matplotlib, lets you create plots/graphs
import os

#Opens file, reads its lines into a list 
file_path = r"C:\Users\ayesh\OneDrive\BME 3A\URA work\Metatarsal_Guard_Project\Files_with_edits\151L-hard-50j_M.csv"
with open(file_path) as f:
    lines = f.readlines()
    
# match one or more digits, and optimally decimal point and decimal digits, then capture that into a group
idx_time_sum = [(idx,*re.search(r"Frame.*?,.*?(\d+(?:\.\d+)?).*?Raw Sum=,,(\d+)", line).group(1,2)) for idx,line in enumerate(lines) if line.startswith("Frame")]
data = np.asarray([list(map(lambda x: list(map(float, x.rstrip().split(","))), lines[i+1:i+1+44])) for i,_,_ in idx_time_sum])

lbs_to_newtons = 4.44822
psi_to_mpa = 0.00689476
scale_factor = 2.99847 #psi/raw
exponent = 1.15447
cell_area = 0.0025 #in^2

# compute things
x = []
y = []
for i in range(data.shape[0]):
    frame = data[i, :, :]
    pressures = scale_factor * (frame**exponent)
    loads = pressures * cell_area
    tot_lbs = np.sum(loads)
    force = tot_lbs*lbs_to_newtons
    x.append(idx_time_sum[i][1]) # time placed at the end of the list
    y.append(force) # force placed at the the end of the list

plt.plot(x, y)
plt.xlabel('Time')
plt.ylabel('Force')
plt.title('Time vs. Force')
interval = 75  # Adjust
plt.xticks(x[::interval], rotation=45)
plt.show()