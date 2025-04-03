import numpy as np

# initialise le tableau des conditions limites en partant du tableau du domaine
def createCl():
    dom = np.loadtxt("CL/2-dom.txt", dtype = int)

    rows, cols = dom.shape

    for i in range(rows):
        for j in range(cols):

            if dom[i, j] == 0:
                continue

            if dom[i, j] == 1:
                dom[i, j] = 0

    np.savetxt("CL/2-cl.txt", dom, fmt='%6.3f')

# change les valeures des conditions limites de dietricht
def changeCl():
    cl = np.loadtxt("CL/2-cl.txt", dtype = float)

    rows, cols = cl.shape

    # valeures limite 
    qIn = 1
    qOut = 0
    clMur = 0.5

    # le debit sortant
    for i in range(2, 21, 1):
        cl[1, i] = qOut

    # le debit entrant
    for i in range(80, 99, 1):
        cl[1, i] = qIn
        cl[99, i] = qIn

    # on cahnge les valeures des murs
    for i in range(rows):
        for j in range(cols):
            if cl[i, j] != qIn and cl[i,j] != qOut:
                cl[i, j] = clMur

    # on sauve le changement
    np.savetxt("CL/2-cl.txt", cl, fmt='%6.3f')

changeCl()