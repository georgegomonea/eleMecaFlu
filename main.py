import funcFlu
import laplacien
import numpy as np

# changer le 1 a 2 pour les differentes situations
dom = np.loadtxt("CL/1-dom.txt", dtype = int)
num = np.loadtxt("CL/1-num.txt", dtype = int)

# resolution du laplacien
psi = laplacien.solver(dom, num)

# illustration des resultats
print(psi)
