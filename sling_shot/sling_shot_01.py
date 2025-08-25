"""
Ik snapte nooit hoe een ruimtevaartuig door middel van een 'slingshot'
manoeuvre kon versnellen...

Voordat we dat gaan opzoeken op wikipedia ofzo (chatGPT e.d. doe ik 
niet an...) dacht ik dat we zelf wat sommetjes/simulaties gaan maken....

We hebben een zwaar ding (planeet,m1) wat initieel over de x-as fietst en
een licht ding (ruimtevaartuig) wat over de y-as gaat. Ze zullen bij
de oorsprong ongeveer bijelkaar komen.

We gaan een eenvoudige simulatie maken, plotjes maken en dan wat spelen
met de initiele start waardes...

noot 1) eenheden zijn volledig arbitrair...

noot 2) best run with: ipython --pylab
 
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn


# constanten (dus niet stiekum veranderen...!)
g  = 0.00001
dt = 0.01
m1 = 1000.0
m2 = 1.0

# globals (hoofdletters zijn array's in dit script)
T  = []
P1 = []
P2 = []
V1 = []
V2 = []
F  = []

def append_to_globals(t, p1, p2, v1, v2, f):
    global T, P1, P2, V1, V2
    T.append(t)
    P1.append(p1.copy())
    P2.append(p2.copy())
    V1.append(v1.copy())
    V2.append(v2.copy())
    F.append(f)

# start waardes variabelen
t  = 0.0
p1 = np.array([-10.0,   0.0 ])
p2 = np.array([  0.0, -10.0 ])
v1 = np.array([  1.0,   0.0 ])
v2 = np.array([  0.0,   0.6 ])

# de eenvoudige simulatie...
max_t = 20.0
while t < max_t:
    
    # bereken afstand tussen de twee dingen, de aantrekkings kracht
    # en de richtingen daarvan
    r     = np.linalg.norm(p1-p2)
    f     = ( g * m1 * m1 ) / ( r ** 2 ) 
    vec21 = (p1-p2) / r
    vec12 = - vec21
    
    # versnellingen berekenen
    a1 = vec12 * f / m1
    a2 = vec21 * f / m2
        
    # nieuwe waardes berekenen
    t  += dt
    p1 += dt * v1
    p2 += dt * v2
    v1 += dt * a1
    v2 += dt * a2

    # opslaan
    append_to_globals(t, p1, p2, v1, v2, f)

# data netjes maken    
P1 = np.asarray(P1).T
P2 = np.asarray(P2).T

V1 = np.asarray(V1).T
V2 = np.asarray(V2).T
velocity_1 = np.sqrt( V1[0,:]**2 + V1[1,:]**2 )
velocity_2 = np.sqrt( V2[0,:]**2 + V2[1,:]**2 )

# plaatjes maken
plt.close('all')
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(15,5))

ax1.set_title('trajectories')
ax1.set_box_aspect(1)
ax1.set_aspect('equal')
line2 = ax1.plot(P2[0], P2[1], label='light object')
line1 = ax1.plot(P1[0], P1[1], label='heavy object')
ax1.legend(loc = 'best')
ax1.set_ylim(-10, ax1.get_xlim()[1])
ax1.set_xlabel('x pos')
ax1.set_ylabel('y pos')

ax2.set_title('speeds')
ax2.set_box_aspect(1)
ax2.plot(T, velocity_2, label='light object')
ax2.plot(T, velocity_1, label='heavy object')
ax2.legend(loc = 'best')
ax2.set_xlabel('time')
ax2.set_ylabel('speed')

ax3.set_title('force')
ax3.set_box_aspect(1)
ax3.plot(T,F)
ax3.set_xlabel('time')
ax3.set_ylabel('force')

plt.savefig('sling_shot_01.png')

# nu nog een animatie maken

# inspiratie van https://matplotlib.org/stable/gallery/animation/simple_scatter.html

import matplotlib.animation as animation

fig2, ax4 = plt.subplots(1,1, figsize=(5,5))
ax4.set_xlim(ax1.get_xlim())
ax4.set_ylim(ax1.get_ylim())
ax4.set_box_aspect(1)
ax4.set_aspect('equal')
color2 = line2[0].get_color()
color1 = line1[0].get_color()

plt.show()

# we want a 3 seconds animation...
aninmation_time = 3.0

samples = len(T)

interval = 500
frames = 50

def animate(i):
    n_points_per_frame = len(T) // frames
    start = i * n_points_per_frame
    end = (i + 1) * n_points_per_frame -1
    print(start,end)
    #ax4.plot(P2[0][start:end], P2[1][start:end], c=color2, lw=.5)
    #ax4.plot(P1[0][start:end], P1[1][start:end], c=color1, lw=.5)
    ax4.plot(P2[0][end], P2[1][end], 'o', c=color2, ms=1)
    ax4.plot(P1[0][end], P1[1][end], 'o', c=color1, ms=1)
    pass

ani = animation.FuncAnimation(fig2, 
                              animate, 
                              repeat=False, 
                              frames=frames, 
                              interval=interval)

# To save the animation using Pillow as a gif
writer = animation.PillowWriter(fps=15,
                                metadata=dict(artist='Me'),
                                bitrate=1800)
ani.save('sling_shot_01.gif', writer=writer)

# plt.show()

