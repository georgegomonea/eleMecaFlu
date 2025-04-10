import funcFlu
import laplacien
import condLimite
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# changer le 1 a 2 pour les differentes situations
dom = np.loadtxt("CL/2-dom.txt", dtype = int)
num = np.loadtxt("CL/2-num.txt", dtype = int)

# donnees
# rapport entre Vin1 et Vout
raportV = 0.5
pasDiscret = 0.01 # m
rows, cols = dom.shape

# creation des conditions limite
vOut = condLimite.createCl(raportV, pasDiscret)
cl = np.loadtxt("CL/2-cl.txt", dtype = float)

# resolution du laplacien
psi = laplacien.solver(dom, num, cl)

# calcul des vitesses
v = funcFlu.velocity(psi, dom, pasDiscret)

# calcul des pressions
p0 = 100
const = p0 / (1000 * 9.81) + np.square(vOut) / (2 * 9.81)
p = funcFlu.pressure(v, dom, const)

# on passe en vision cartesienne
psi_cartesien = psi.T
vX = v[:,:,0].T
vY = v[:,:,1].T
p_cartesien = p.T
dom_cartesien = dom.T

# utile pour la verification
np.savetxt("vx.txt", v[:,:,0], fmt='%6.3f')
np.savetxt("vy.txt", v[:,:,1], fmt='%6.3f')
np.savetxt("psi.txt", psi, fmt='%6.3f')
np.savetxt("p.txt", p, fmt='%6.3f')

# Graphiques
X, Y = np.meshgrid(np.arange(cols) * pasDiscret, np.arange(rows) * pasDiscret)

def plotChampVitesse():
    plt.figure(figsize=(10, 10))

    # Define mask
    mask = dom_cartesien == 0 

    # Mask the velocity field (components)
    vX_masked = np.ma.masked_where(mask, vX)
    vY_masked = np.ma.masked_where(mask, vY)

    # Define background color for the domain
    masked_dom = np.ma.masked_where(dom_cartesien != 0, dom_cartesien)
    cmap = ListedColormap(['#8C92AC'])

    # Plot vector field only where allowed
    step = 2
    plt.quiver(X[::step, ::step], Y[::step, ::step], vX_masked[::step, ::step], vY_masked[::step, ::step], color='blue')

    # Plot domain overlay
    plt.imshow(masked_dom, cmap=cmap, origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()])

    plt.title("Champ des Vitesses")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis('equal')
    plt.grid(False)
    plt.show()

def plotPression():
    plt.figure(figsize=(10, 8))
    
    # mask
    masked_dom = np.ma.masked_where(dom_cartesien != 0, dom_cartesien)
    cmap = ListedColormap(['#8C92AC'])

    plt.imshow(p_cartesien, cmap='viridis', origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()]) 
    plt.colorbar(label='Pression (Pa)')

    plt.imshow(masked_dom, cmap=cmap, origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()])

    plt.title("Champ de Pression Relative")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis('equal')
    plt.grid(False)
    plt.show()

def plotPression2():
    plt.figure(figsize=(10, 8))

    # mask the solid region (dom == 0) as background
    masked_dom = np.ma.masked_where(dom_cartesien != 0, dom_cartesien)
    masked_dom2 = np.ma.masked_where(dom_cartesien == 0, dom_cartesien)
    cmap_dom = ListedColormap(['#8C92AC'])

    # mask pressure values outside the fluid domain
    masked_p = np.ma.masked_where(dom_cartesien == 0, p_cartesien)

    # contourf with color levels for pressure field
    contour = plt.contourf(X, Y, masked_p, levels=100, cmap='coolwarm', extent=[X.min(), X.max(), Y.min(), Y.max()])

    plt.colorbar(contour, label='Pression (Pa)')

    # add domain background
    plt.imshow(masked_dom, cmap=cmap_dom, origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()])
    plt.imshow(masked_dom2, cmap=cmap_dom, origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()])

    # cosmetic stuff
    plt.title("Champ de Pression Relative")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis('equal')
    plt.grid(False)
    plt.show()

plotChampVitesse()
plotPression()
plotPression2()