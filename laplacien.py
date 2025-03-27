import numpy as np 
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
import funcFlu

# conditions aux limites du cas 1
cl = np.loadtxt("CL/1-cl.txt", dtype = float)

def solver(dom, num):

    # nbr de noeuds a calculer
    non_zero = np.count_nonzero(dom)

    # taille du systeme etudiee
    rows, cols = dom.shape

    # initialisation des vecteurs a mettre dans la sparse matrix
    dataSparse = []
    rowSparse = []
    colSparse = []
    b = np.zeros((non_zero))

    # itere sur chaque noeud
    for i in range(rows):
        for j in range(cols):

            # donnees du noeud central
            nodeType = dom[i, j]
            nodeNum = num[i, j]

            # si pas dans le domaine, on passe au suivant
            if nodeType == 0:
                continue

            # appel a getCoeff
            numNoeuds, listeCoeff, valB = funcFlu.getCoeff(num[i, j-1], num[i, j+1], num[i+1, j], num[i-1, j], nodeNum, nodeType, cl[i, j]) 

            # getCoeff retourne les valeurs selon 3 cas, l'un des cas est elimine par le if nodeType == 0
            nbrCoeff = len(listeCoeff)

            # Nœud de Dirichlet, cas 1
            if nbrCoeff == 1: 
                dataSparse.append(listeCoeff[0])
                rowSparse.append(nodeNum - 1)
                colSparse.append(numNoeuds[0] - 1)

            # noeud normal, cas 2
            else: 
                for k in range(5):
                    dataSparse.append(listeCoeff[k, 0])
                    rowSparse.append(nodeNum - 1)
                    colSparse.append(numNoeuds[k, 0] - 1)

            # on place la valeur de la condition limite (on doit aller de 0 a nbrNoeuds - 1)
            b[nodeNum - 1] = valB
    
    # on construit la matrice creuse
    A = csc_matrix((dataSparse, (rowSparse, colSparse)), shape=(non_zero, non_zero))

    # on resout le systeme
    psi = spsolve(A, b)

    return psi