import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import sys

#*XDATCAR.xlsx file as input to the script
input_file = sys.argv[1]
dataset = pd.read_excel(input_file)
dataset = dataset.fillna(0)

#lattice Parameters in Angstrom
a = (dataset.iloc[[0], :]).values.tolist()[0][0]
b = (dataset.iloc[[1], :]).values.tolist()[0][1]
c = (dataset.iloc[[2], :]).values.tolist()[0][2]

#atoms and number of atoms
atom = (dataset.iloc[[3], :]).values.tolist()[0]

number_of_atom = (dataset.iloc[[4], :]).values.tolist()[0]

#coordinates

X = (dataset.iloc[5:,[0]]).values.tolist()
Y = (dataset.iloc[5:,[1]]).values.tolist()
Z = (dataset.iloc[5:,[2]]).values.tolist()

if (len(X) != len(Y)):
    print("Check Input File. Coordinates missing/extra!")


if (len(X) != len(Z)):
    print("Check Input File. Coordinates missing/extra!")

#frames in dynamic simualtion
number_of_frames = math.floor(len(X)/sum(number_of_atom))

#atom numbers as input to the script for tracking the bond angle
atom_number_one = int(sys.argv[2])
atom_number_two = int(sys.argv[3])

periodic_distance = [[[0 for k in range(3)] for j in range(3)] for i in range(3)]
distance = []
avg_distance = []

for frames in range(number_of_frames):
    x_atom1, y_atom1, z_atom1 = X[frames*sum(number_of_atom) + atom_number_one][0], Y[frames*sum(number_of_atom) + atom_number_one][0], Z[frames*sum(number_of_atom) + atom_number_one][0]
    x_atom2, y_atom2, z_atom2 = X[frames*sum(number_of_atom) + atom_number_two][0], Y[frames*sum(number_of_atom) + atom_number_two][0], Z[frames*sum(number_of_atom) + atom_number_two][0]
    for m in range(-1, 2):
        for n in range(-1, 2):
            for o in range(-1, 2):
                periodic_distance[m+1][n+1][o+1] = math.dist((x_atom1*a, y_atom1*b, z_atom1*c), ((x_atom2 + m)*a, (y_atom2 + n)*b, (z_atom2 + o)*c))
    distance += [min(min(min(periodic_distance)))]
    avg_distance += [sum(distance)/len(distance)]

fig = plt.figure(figsize=(10, 4))
plt.plot(distance, color = "darkgrey")
plt.plot(avg_distance, "lightcoral", label = "Average", linewidth = 3)
plt.xlabel('Number of Frames')
plt.xlim([0, number_of_frames])
plt.ylabel('C-C Distance for Oxalate Radical Anion in $\mathrm{\AA}$ ')
plt.legend(loc="upper right")
output_file = sys.argv[4]
plt.savefig(output_file)