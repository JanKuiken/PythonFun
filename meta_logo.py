"""
Ik zag op het journaal een bewegend meta logo (van facebook en zo)

even namaken met MatPlotlib....

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


fig = plt.figure()
ax = plt.axes(projection='3d')

p = np.linspace(0, 2 * np.pi, 1000)

x = np.sin(p)
y = np.cos(p)
z = np.sin(2*p)

ax.plot3D(x,y,z,'b-', lw=8)
plt.axis('off')
plt.tight_layout()
plt.show()

