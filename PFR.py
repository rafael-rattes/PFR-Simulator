# Making a PFR (Plug Flow Reactor) simulation using a discrete method
# Using a known reaction kinetics, residency time, diameter of the reactor, the script calculates the volume of the reactor
#Reaction A + B -> C; A + C -> D and E is inert

import numpy as np

def reaction_rate(k: float, C = np.array([0]), exp= np.array([0])):
    '''
    Calculates the reaction rate based on the rate constant, concentration of the reactants and the exponents of the reactants
    k: rate constant
    C: Concentration of the reactants
    exp: Exponents of the reactants
    '''
    return k*np.prod(np.power(C, exp))

tau = 0.5 # Residency time in hours
D = 0.5 # Diameter of the reactor in meters
T0 = 300 # Initial temperature in Kelvin
P0 = 1 # Initial pressure in atm
Q0 = 1 # Initial flow rate in m^3/h

# Reaction values
C0 = np.array([10, 10, 0, 0, 2]) # Initial concentration of the reactants in mol/m^3
k1 = 0.3 # Rate constant for the first reaction in 1/h
k2 = 0.1 # Rate constant for the second reaction in 1/h
# Defining the differential equations for ODEINT
def dCdt(C, t):
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
    dAdt = -rxn1 - rxn2
    dBdt = -rxn1
    dCdt = rxn1 - rxn2
    dDdt = rxn2
    dEdt = 0
    return [dAdt, dBdt, dCdt, dDdt, dEdt]

from scipy.integrate import odeint

# Time points
t = np.linspace(0, tau, 100)

# Solving the ODEs
C = odeint(dCdt, C0, t)

# Plotting the concentration profiles
import matplotlib.pyplot as plt

plt.plot(t, C[:, 0], label='A')
plt.plot(t, C[:, 1], label='B')
plt.plot(t, C[:, 2], label='C')
plt.plot(t, C[:, 3], label='D')
plt.plot(t, C[:, 4], label='E')
plt.xlabel('Time (h)')
plt.ylabel('Concentration (mol/m^3)')
plt.legend()
plt.show()