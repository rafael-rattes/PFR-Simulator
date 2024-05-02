# Making a PFR (Plug Flow Reactor) simulation using a discrete method
# Using a known reaction kinetics, residency time, diameter of the reactor, the script calculates the volume of the reactor
#Reaction A + B -> C; A + C -> D and E is inert

import numpy as np

tau = 0.5 # Residency time in hours
D = 0.5 # Diameter of the reactor in meters
T0 = 300 # Initial temperature in Kelvin
P0 = 1 # Initial pressure in atm
F0 = np.array([10, 10, 0, 0, 2]) # Initial molar flow in mol/h for (A, B, C, D, E)

rxn_r = {'zero':      lambda var: var[0][0], #var = [[k]] one dimensional
         'elementar': lambda var: var[0][0]*np.prod(var[1][:]), #var = [[k], [C_i1, C_i2...]] two dimensional
         'custom':    lambda var: var[0][0]*np.prod(np.power(var[1], var[2]))} #var = [[k], [C_i1, C_i2...], [exp_i1, exp_i2...]] three dimensional

rxn_r = rxn_r['custom']( [[0.1], [1, 3], [2, 2]] ) # Reaction kinetics constant in mol/(L.h)

print(rxn_r)