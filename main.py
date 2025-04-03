import funcFlu
import laplacien
import numpy as np
import matplotlib.pyplot as plt

# changer le 1 a 2 pour les differentes situations
dom = np.loadtxt("CL/2-dom.txt", dtype = int)
num = np.loadtxt("CL/2-num.txt", dtype = int)
cl = np.loadtxt("CL/2-cl.txt", dtype = float)

# donnees
pasDiscret = 0.5
rows, cols = dom.shape

# resolution du laplacien
psi = laplacien.solver(dom, num, cl)

# calcul des vitesses
v = funcFlu.velocity(psi, dom, pasDiscret)

# calcul des pressions
p = funcFlu.pressure(v, dom, 0)

print(psi)
print(v[:,:,0])
print(v[:,:,1])
print(p)

np.savetxt("psi.txt", psi, fmt='%6.3f')

# Create meshgrid for coordinates (assuming spacing h = 1 for simplicity)
X, Y = np.meshgrid(np.arange(cols), np.arange(rows))

# Plot
plt.figure(figsize=(8, 6))
plt.quiver(X, Y, v[:, :, 0], v[:, :, 1], color='blue')
plt.title("Velocity Field (Stream Function Gradient)")
plt.xlabel("x")
plt.ylabel("y")
plt.axis('equal')
plt.grid(True)
plt.show()