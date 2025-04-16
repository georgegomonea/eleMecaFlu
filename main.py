import funcFlu
import laplacien
import condLimite
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# changer le 1 a 2 pour les differentes situations
dom = np.loadtxt("CL/2-dom.txt", dtype = int)
num = np.loadtxt("CL/2-num.txt", dtype = int)
contourObj = np.loadtxt("CL/2-contourObj.txt", dtype = int)

# donnees
# rapport entre Vin1 et Vout
raportV = 0.7
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

# calcul de la circulation
# on doit d'abbord creer les vecteurs u et v, dans l'ordre de parcours des noeuds
rowObj, _ = contourObj.shape

uCircu = np.zeros(rowObj)
vCircu = np.zeros(rowObj)

for i in range(rowObj):
    # indices du contour de l'obj
    x = contourObj[i, 0]
    y = contourObj[i, 1]

    # u est la vitesse horizontale
    uCircu[i] = v[x, y, 0]

    # v est la vitesse verticale
    vCircu[i] = v[x, y, 1]

# appel a la fonction de la circulation
circu = funcFlu.circu(uCircu, vCircu, contourObj[:, 0], contourObj[:, 1])

print(circu)

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
    cmap = ListedColormap(['#eeeeee'])

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
    cmap_dom = ListedColormap(['#eeeeee'])

    # mask pressure values outside the fluid domain
    masked_p = np.ma.masked_where(dom_cartesien == 0, p_cartesien)

    # contourf with color levels for pressure field
    contour = plt.contourf(X, Y, masked_p, levels=200, cmap='coolwarm', extent=[X.min(), X.max(), Y.min(), Y.max()])

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

def plotVelocityColor():
    step = 4
    speed = np.sqrt(vX**2 + vY**2)
    
    plt.figure(figsize=(10, 8))

    # Mask vectors in solid region
    mask = dom_cartesien == 0
    vX_masked = np.ma.masked_where(mask, vX)
    vY_masked = np.ma.masked_where(mask, vY)
    speed_masked = np.ma.masked_where(mask, speed)

    # Background for structure (like before)
    masked_dom = np.ma.masked_where(dom_cartesien != 0, dom_cartesien)
    cmap_dom = ListedColormap(['#eeeeee'])

    # Plot velocity field with color magnitude
    q = plt.quiver(X[::step, ::step], Y[::step, ::step],
                   vX_masked[::step, ::step], vY_masked[::step, ::step],
                   speed_masked[::step, ::step],
                   cmap='viridis', scale=25, width=0.002)

    # Background shape
    plt.imshow(masked_dom, cmap=cmap_dom, origin='lower',
               extent=[X.min(), X.max(), Y.min(), Y.max()])

    plt.colorbar(q, label='Vitesse (m/s)')
    plt.title("Champ de Vitesse")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis('equal')
    plt.grid(False)
    plt.show()

def plotVelocityStream():
    plt.figure(figsize=(10, 8))
    
    # === Compute speed for coloring ===
    speed = np.sqrt(vX**2 + vY**2)

    # === Mask velocity and speed outside fluid domain ===
    mask = dom_cartesien == 0
    vX_masked = np.ma.masked_where(mask, vX)
    vY_masked = np.ma.masked_where(mask, vY)
    speed_masked = np.ma.masked_where(mask, speed)

    # === Background (solid region as light gray) ===
    masked_dom = np.ma.masked_where(dom_cartesien != 0, dom_cartesien)
    cmap_dom = ListedColormap(['#eeeeee'])

    plt.imshow(masked_dom, cmap=cmap_dom, origin='lower',
               extent=[X.min(), X.max(), Y.min(), Y.max()])

    # === Streamplot ===
    stream = plt.streamplot(
        X, Y,
        vX_masked, vY_masked,
        color=speed_masked,
        cmap='viridis',
        linewidth=1,
        density=1.6,  # increase for more lines
        arrowstyle='->'
    )

    # === Colorbar for speed ===
    plt.colorbar(stream.lines, label='Vitesse (m/s)')

    # === Labels and formatting ===
    plt.title("Lignes de courant")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis('equal')
    plt.grid(False)
    plt.show()

def plotVlinesPress():
    plt.figure(figsize=(10, 6.5))
    
    # === Compute speed for coloring ===
    speed = np.sqrt(vX**2 + vY**2)

    # === Mask velocity and speed outside fluid domain ===
    mask = dom_cartesien == 0
    vX_masked = np.ma.masked_where(mask, vX)
    vY_masked = np.ma.masked_where(mask, vY)
    speed_masked = np.ma.masked_where(mask, speed)

    # === Background (solid region as light gray) ===
    masked_dom = np.ma.masked_where(dom_cartesien != 0, dom_cartesien)
    masked_dom2 = np.ma.masked_where(dom_cartesien == 0, dom_cartesien)
    cmap_dom = ListedColormap(['#eeeeee'])

    plt.imshow(masked_dom, cmap=cmap_dom, origin='lower',
               extent=[X.min(), X.max(), Y.min(), Y.max()])

    # === Streamplot ===
    stream = plt.streamplot(
        X, Y,
        vX_masked, vY_masked,
        color=speed_masked,
        cmap='viridis',
        linewidth=1,
        density=1.6,  # increase for more lines
        arrowstyle='->'
    )

    # === Colorbar for speed ===
    plt.colorbar(stream.lines, label='Vitesse (m/s)')

     # mask pressure values outside the fluid domain
    masked_p = np.ma.masked_where(dom_cartesien == 0, p_cartesien)

    # contourf with color levels for pressure field
    contour = plt.contourf(X, Y, masked_p, levels=200, cmap='coolwarm', extent=[X.min(), X.max(), Y.min(), Y.max()])

    plt.colorbar(contour, label='Pression (Pa)')

    # add domain background
    plt.imshow(masked_dom, cmap=cmap_dom, origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()])
    plt.imshow(masked_dom2, cmap=cmap_dom, origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()])

    # === Labels and formatting ===
    plt.title("Lignes de courant superposées au champ de pression")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis('equal')
    plt.grid(False)
    plt.show()


plotVlinesPress()