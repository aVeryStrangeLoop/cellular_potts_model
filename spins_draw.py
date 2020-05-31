# Draws the spins and types in a single graph
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections as mc

foldername = sys.argv[1]
mcs = int(sys.argv[2])

spins = np.loadtxt(foldername+"/mcs_"+str(mcs)+"_spins.csv")
types = np.loadtxt(foldername+"/mcs_"+str(mcs)+"_types.csv")

lines = []
X = spins.shape[0]
Y = spins.shape[1]

for i in range(spins.shape[0]):
    for j in range(spins.shape[1]):
        my_spin = spins[i,j]
        # Check left spin
        left_spin = (spins[i-1,j] if i>0 else spins[X-1,j])
        if left_spin!=my_spin:
            lines.append([(j-0.5,i-0.5),(j+0.5,i-0.5)])
        # Check right spin
        right_spin = (spins[i+1,j] if i<X-1 else spins[0,j])
        if right_spin!=my_spin:
            lines.append([(j-0.5,i+0.5),(j+0.5,i+0.5)])    
        # Check bottom spin
        bot_spin = (spins[i,j-1] if j>0 else spins[i,Y-1])
        if bot_spin!=my_spin:
            lines.append([(j-0.5,i-0.5),(j-0.5,i+0.5)])
        # Check top spin
        top_spin = (spins[i,j+1] if j<Y-1 else spins[i,0])
        if top_spin!=my_spin:
            lines.append([(j+0.5,i-0.5),(j+0.5,i+0.5)])

lc = mc.LineCollection(lines,color="red",linewidths=2)            
fig, ax = plt.subplots()
ax.add_collection(lc)
ax.imshow(types)
plt.savefig('spins_out.png')
