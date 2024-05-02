# Making a PFR (Plug Flow Reactor) simulation using a discrete method
# Using a known reaction kinetics, residency time, diameter of the reactor, the script calculates the volume of the reactor
#Reaction A + B -> C; A + C -> D and E is inert

import numpy as np
from scipy.integrate import odeint

def reaction_rate(k: float, C = np.array([0]), exp = np.array([0])):
    '''
    Calculates the reaction rate based on the rate constant, concentration of the reactants and the exponents of the reactants
    k: rate constant
    C: Concentration of the reactants
    exp: Exponents of the reactants
    '''
    return k*np.prod(np.power(C, exp))

# System variables
tau = 3 # Residency time in hours
D = 0.5 # Diameter of the reactor in meters
T0 = 300 # Initial temperature in Kelvin
P0 = 1 # Initial pressure in atm
Q0 = 1 # Initial flow rate in m^3/h
C0 = np.array([10, 5, 0, 0, 2]) # Initial concentration of the reactants in mol/m^3
k1 = 0.3 # Rate constant for the first reaction in 1/h
k2 = 0.5 # Rate constant for the second reaction in 1/h

# Defining the differential equations for ODEINT
def dCdt(C, L):
    '''
    Differential equations for the concentration of the reactants
    C: Concentration of the reactants
    t: Time
    '''
    # Unpacking the concentration of the reactants
    CA, CB, CC, CD, CE = C
    
    # Reaction rates
    rxn1 = reaction_rate(k1, [CA, CB], [1, 1])
    rxn2 = reaction_rate(k2, [CA, CC], [1, 1])

    # Differential equations
    dAdL = -rxn1 - rxn2
    dBdL = -rxn1
    dCdL = rxn1 - rxn2
    dDdL = rxn2
    dEdL = 0
    return [dAdL, dBdL, dCdL, dDdL, dEdL]

# Solving the ODEs
L = np.linspace(0, 5, 100) # Length of the reactor
C = odeint(dCdt, C0, L) # Solving the ODEs

# Plotting the concentration profiles
import matplotlib.pyplot as plt

for i in range(5):
    plt.plot(L, C[:, i], label=f'{chr(65+i)}')
plt.xlabel('Length (m)')
plt.ylabel('Concentration (mol/m^3)')
plt.legend()
plt.show()