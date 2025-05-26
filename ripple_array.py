"""
dus....
"""

import numpy as np
import matplotlib.pyplot as plt

# remove 'old' matplotlib figures
plt.close('all')

# some globals and some utility functions using those
alpha        = 2 * np.pi
beta         = 0.05
c            = 2.0         # not lightspeed, but some 'speed'
dt           = 10.0        # delay time, to have the max of the pulse at dt
N            = 501
size         = 20.0
first_source = np.array([ 1.0 ,1.0])
last_source  = np.array([ 1.0 ,5.0]) 
N_sources    = 5
xs, ys       = np.meshgrid(np.linspace(0.0, size, N), 
                           np.linspace(0.0, size, N) )

def wave(t):
    return np.cos(alpha * (t-dt)) * np.exp( -beta * ((t-dt)**2)) 

def create_distances_field(x,y):
    return np.sqrt( (xs-x)**2 + (ys-y)**2 )


def estimate_some_params():
    """
    test function to tune the globals alpha, beta and dt to create
    a 'nice' wave function; a cosine @1Hz modulated with a maximum
    at 10 seconds and alomost nill at 0 and 20 seconds. 
    
    """
    t = np.linspace(0.0, 20.0, 1000)
    a = wave(t)
    plt.figure()
    plt.plot(t,a)
    plt.show()

# estimate_some_params()


def create_wave_field(dist_mat, t, delay):
    time_mat = t - dist_mat / c - delay
    return wave(time_mat)

def clip_field(field_mat):
    max_value = np.abs(np.max(field_mat))
    if max_value > 1.001:
        return field_mat / max_value
    else:
        return field_mat


d_1 = create_distances_field(2,1)
d_2 = create_distances_field(2,2)
d_3 = create_distances_field(2,3)
d_4 = create_distances_field(2,4)
d_5 = create_distances_field(2,5)

w_1 = create_wave_field(d_1, 10.0, 0.0)
w_2 = create_wave_field(d_2, 10.0, 0.0)
w_3 = create_wave_field(d_3, 10.0, 0.0)
w_4 = create_wave_field(d_4, 10.0, 0.0)
w_5 = create_wave_field(d_5, 10.0, 0.0)

wave_field = w_1 + w_2 + w_3 + w_4 + w_5
wave_field = clip_field(wave_field)

plt.figure(figsize=(6,6))
plt.gca().axis('equal')
plt.imshow(wave_field, origin='lower')
plt.axis('off')
plt.tight_layout()
plt.savefig('ripple_array_sample_1.png')
plt.show()

w_1 = create_wave_field(d_1, 10.0, 0.0)
w_2 = create_wave_field(d_2, 10.0, 0.2)
w_3 = create_wave_field(d_3, 10.0, 0.4)
w_4 = create_wave_field(d_4, 10.0, 0.6)
w_5 = create_wave_field(d_5, 10.0, 0.8)

wave_field = w_1 + w_2 + w_3 + w_4 + w_5
wave_field = clip_field(wave_field)

plt.figure(figsize=(6,6))
plt.gca().axis('equal')
plt.imshow(wave_field, origin='lower')
plt.axis('off')
plt.tight_layout()
plt.savefig('ripple_array_sample_2.png')
plt.show()






