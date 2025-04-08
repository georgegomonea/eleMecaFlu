import numpy as np
   
def findNextNode(i0, j0, oldi, oldj, cl):
    rows, cols = cl.shape

    # droite
    if j0 + 1 < cols and (i0, j0 + 1) != (oldi, oldj) and cl[i0, j0 + 1] == 2:
        return i0, j0 + 1

    # gauche
    if j0 - 1 >= 0 and (i0, j0 - 1) != (oldi, oldj) and cl[i0, j0 - 1] == 2:
        return i0, j0 - 1

    # bas
    if i0 + 1 < rows and (i0 + 1, j0) != (oldi, oldj) and cl[i0 + 1, j0] == 2:
        return i0 + 1, j0

    # haut
    if i0 - 1 >= 0 and (i0 - 1, j0) != (oldi, oldj) and cl[i0 - 1, j0] == 2:
        return i0 - 1, j0

    return None

# change les valeures des conditions limites de dietricht
def createCl():

    # je charge les donnees existantes
    cl = np.loadtxt("CL/2-dom.txt", dtype = float)
    contourObj = np.loadtxt("CL/2-contourObj.txt", dtype = int)

    # initialisation du tableau de cl, pour tout les noeuds de type 1, on n'as pas de cl
    cl[cl == 1] = 0

    # valeures du numero de groupe
    X = 7
    Y = 0

    # formule issue de l'enonce
    debitTotal = (10*X + 5*Y)*0.001

    # 21 noeuds pour le gros et 7 pour le cordon vertical et 8 pour le cordon horizontal
    # l'epaisseur est unitaire donc A = 20*pasDiscret qui est de 1cm
    # la sortie et l'entree ont une largeur de 21 points de discretisation
    pasDiscret = 0.01
    aireTotale = (21 - 1) * pasDiscret
    aireObstVerti = (7 - 1) * pasDiscret
    aireObstHori = (8 - 1) * pasDiscret

    # rapport entre Vin1 et Vout (0.5 pour le cas 1 et 0.7 pour le cas 2)
    rap = 0.5

    Vout = debitTotal / aireTotale
    Vin1 = rap * Vout
    Vin2 = (1 - rap) * Vout
    
    # debit est reparti uniformement de cote et d'autre de l'obstacle vertical
    # Vverti est la vitesse moyenne sur le cote vertical de l'obstacle 
    # Vhoribas est la vitesse dans la branche horizontale base de l'obstacle en T
    Vverti = (aireTotale * Vout) / (2 * aireObstVerti)
    Vhoribas = (Vverti * aireObstVerti) / aireObstHori

    # si les debits d'entree sont differents, une partie sera envoie de l'atre cote pour que le debit vertical soit le meme
    # vitesse sur la branche superieure du T
    Vhorihaut = (aireTotale * Vin1) / aireObstHori - Vhoribas

    # le contour, c'est tout les autres point qui sont egaux a deux, on va commencer en 1 1
    row, col = 1, 1

    # valIni est la valeure arbitraire de depart pour les conditions limites
    valIni = 0.5
    valCl = valIni

    # valeures limites des murs
    clGauche, clHaut, clDroite = 0, 0, valIni

    while(True):
        # on sauvgarde le dernier point visite
        oldrow, oldcol = row, col

        # iteration de voisin en voisin
        next_pos = findNextNode(row, col, oldrow, oldcol, cl)

        # gardiens de boucle
        if next_pos is None:
            print("erreur dans le contour")
            break

        # on sauvgarde le dernier point visite
        row, col = next_pos

        # autre gardien de boucle
        if next_pos == (1, 1):
            print("Fin du contour")
            cl[row, col] = valCl
            break

        # sortie
        if row == 1 and col in range(1, 22):
            valCl = valCl - Vout * pasDiscret

            clGauche = valCl

        # entree 1
        if row == 1 and col in range(79, 100):
            valCl = valCl + Vin1 * pasDiscret

            clHaut = valCl

        # entree 2
        if row == 99 and col in range(79, 100):
            valCl = valCl + Vin2 * pasDiscret
        
        if row == 99 and col == 79:
            valCl = valIni

        cl[row, col] = valCl

    # nbr de noeuds qui englobent l'obstacle
    rowObj, _ = contourObj.shape

    # valeures des cl sur l'obstacle
    clVertGauche = (Vverti * aireObstVerti) + clGauche
    clVertDroite = clDroite - (Vverti * aireObstVerti)

    clHoriGauche = clGauche + (Vhoribas * aireObstHori)
    clHoriDroite = clDroite - (Vhoribas * aireObstHori)

    clHoriHaut = clHaut - (Vhorihaut * aireObstHori)

    # on va de noeud en noeud jusqu'a n-2 car on calcule la derivee, donc on utilise i et i+1, et le dernier noeud et aussi le premier
    for i in range(rowObj - 1):

        row = contourObj[i, 0]
        col = contourObj[i, 1]

        if col == 92:
            cl[row, col] = clHoriHaut
            continue

        cl[row, col] = clVertGauche



        
   


    # on sauve le changement
    np.savetxt("CL/2-cl.txt", cl, fmt='%6.3f')

createCl()