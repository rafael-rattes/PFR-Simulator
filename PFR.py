import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.widgets import Slider
from matplotlib.text import Text

def reaction_rate(k: float, C = np.array([0]), exp = np.array([0])):
    '''
    Calculates the reaction rate based on the rate constant, concentration of the reactants and the exponents of the reactants
    k: rate constant
    C: Concentration of the reactants
    exp: Exponents of the reactants
    '''
    return k * np.prod(np.power(C, exp))

# System variables
C0 = np.array([10, 5, 0, 0, 2])  # Initial concentration of the reactants in mol/m^3
k1 = 0.3  # Rate constant for the first reaction in 1/h
k2 = 0.5  # Rate constant for the second reaction in 1/h

# Initial reaction rates
rxn1 = reaction_rate(k1, [C0[0], C0[1]], [1, 1]) # Reaction rate for the first reaction in mol/m^3/h
rxn2 = reaction_rate(k2, [C0[0], C0[2]], [1, 1]) # Reaction rate for the second reaction in mol/m^3/h

# Defining the differential equations for ODEINT
def dCdL(C, L, k1, k2):
    '''
    Differential equations for the concentration of the reactants
    C: Concentration of the reactants
    L: Length
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
L = np.linspace(0, 5, 100)  # Length of the reactor

# Function to update plot based on sliders
def update(val):
    ax.clear()
    k1 = s_k1.val
    k2 = s_k2.val
    C0_new = np.array([s_A.val, s_B.val, s_C.val, s_D.val, s_E.val])
    C = odeint(dCdL, C0_new, L, args=(k1, k2))
    ax.plot(L, C[:, 0], label='A')
    ax.plot(L, C[:, 1], label='B')
    ax.plot(L, C[:, 2], label='C')
    ax.plot(L, C[:, 3], label='D')
    ax.plot(L, C[:, 4], label='E')
    ax.legend()
    
    # Calculate conversion and yield
    X = (C0_new[0] - C[-1, 0]) / C0_new[0]
    Y = C[-1, 3] / C0_new[0]
    
    # Update the text display
    text_display.set_text(f'Conversion $(X_A)$: {X:.2f}\nYield $(Y_D)$: {Y:.2f}')
    
    plt.draw()

# Create plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35, right=0.7)

# Plot initial concentrations
C = odeint(dCdL, C0, L, args=(k1, k2))
ax.plot(L, C[:, 0], label='A')
ax.plot(L, C[:, 1], label='B')
ax.plot(L, C[:, 2], label='C')
ax.plot(L, C[:, 3], label='D')
ax.plot(L, C[:, 4], label='E')
ax.legend()

y_pos = np.linspace(0.05, 0.25, 7)

# Slider for k2
ax_k2 = plt.axes([0.25, y_pos[0], 0.4, 0.03])
s_k2 = Slider(ax_k2, 'k2', 0.1, 1.0, valinit=k2)

# Slider for k1
ax_k1 = plt.axes([0.25, y_pos[1], 0.4, 0.03])
s_k1 = Slider(ax_k1, 'k1', 0.1, 1.0, valinit=k1)

# Slider for initial concentration of A
ax_A = plt.axes([0.25, y_pos[6], 0.4, 0.03])
s_A = Slider(ax_A, 'C0_A', 0, 20, valinit=C0[0])

# Slider for initial concentration of B
ax_B = plt.axes([0.25, y_pos[5], 0.4, 0.03])
s_B = Slider(ax_B, 'C0_B', 0, 20, valinit=C0[1])

# Slider for initial concentration of C
ax_C = plt.axes([0.25, y_pos[4], 0.4, 0.03])
s_C = Slider(ax_C, 'C0_C', 0, 20, valinit=C0[2])

# Slider for initial concentration of D
ax_D = plt.axes([0.25, y_pos[3], 0.4, 0.03])
s_D = Slider(ax_D, 'C0_D', 0, 20, valinit=C0[3])

# Slider for initial concentration of E
ax_E = plt.axes([0.25, y_pos[2], 0.4, 0.03])
s_E = Slider(ax_E, 'C0_E', 0, 20, valinit=C0[4])

# Text box for displaying conversion and yield
ax_text = plt.axes([0.45, y_pos[3], 0.4, 0.1])
ax_text.axis('off')
text_display = plt.text(x=0.75, y=0.15, s=f'Conversion $(X_A)$: {(C0[0] - C[-1, 0]) / C0[0]:.2f}\nYield $(Y_D)$: {C[-1, 3] / C0[0]:.2f}')

# Update plot when sliders change
s_k1.on_changed(update)
s_k2.on_changed(update)
s_A.on_changed(update)
s_B.on_changed(update)
s_C.on_changed(update)
s_D.on_changed(update)
s_E.on_changed(update)

plt.show()