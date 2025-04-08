import funcFlu
import laplacien
import numpy as np
import matplotlib.pyplot as plt

# changer le 1 a 2 pour les differentes situations
dom = np.loadtxt("CL/2-dom.txt", dtype = int)
num = np.loadtxt("CL/2-num.txt", dtype = int)
cl = np.loadtxt("CL/2-cl.txt", dtype = float)

# donnees
pasDiscret = 0.01
rows, cols = dom.shape

# resolution du laplacien
psi = laplacien.solver(dom, num, cl)

# calcul des vitesses
v = funcFlu.velocity(psi, dom, pasDiscret)

# calcul des pressions
p = funcFlu.pressure(v, dom, 0)

np.savetxt("vx.txt", v[:,:,0], fmt='%6.3f')
np.savetxt("vy.txt", v[:,:,1], fmt='%6.3f')
np.savetxt("psi.txt", psi, fmt='%6.3f')

# Create meshgrid for coordinates (assuming spacing h = 1 for simplicity)
X, Y = np.meshgrid(np.arange(cols), np.arange(rows))

# Plot
def plot1():
    plt.figure(figsize=(8, 6))
    plt.quiver(X, Y, v[:, :, 1], v[:, :, 0], color='blue')
    plt.title("Velocity Field (Stream Function Gradient)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis('equal')
    plt.grid(True)
    plt.show()

def plot2():

    plt.imshow(p, cmap='viridis', origin='lower')  # 'lower' = y vers le haut
    plt.colorbar(label='Pa')
    plt.title("Visualisation des pressions")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis('equal')
    plt.grid(True)
    plt.show()

def plot3():
    plt.contourf(X, Y, psi, levels=20, cmap='coolwarm')
    plt.colorbar(label='ψ')
    plt.title("Lignes de niveau de ψ (contourf)")
    plt.axis('equal')
    plt.grid(True)
    plt.show()

def plot4():
    plt.contourf(X, Y, p, levels=20, cmap='coolwarm')
    plt.colorbar(label='ψ')
    plt.title("Lignes de niveau de ψ (contourf)")
    plt.axis('equal')
    plt.grid(True)
    plt.show()

plot1()
plot3()