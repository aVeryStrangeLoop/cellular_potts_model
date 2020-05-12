import numpy as np
import sys
import matplotlib.pyplot as plt

filename = sys.argv[1]

img = np.loadtxt(filename)

plt.imshow(img)
plt.show() 
