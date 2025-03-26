import numpy as np

# Pas de la discretisation
h = 1

def getCoeff(num_left, num_right, num_down, num_up, num_cent, type_cent, cl_cent):
    
    if type_cent == 0:  # Nœud hors domaine
        j = np.array([]) 
        a = np.array([]) 
        b = 0
    
    elif type_cent == 1:  # Nœud intérieur
        coeff = 1 / (h ** 2)
        j = np.array([num_left, num_right, num_down, num_up, num_cent]).reshape(-1, 1)
        a = np.array([coeff, coeff, coeff, coeff, -4 * coeff]).reshape(-1, 1).astype(int)
        b = 0  # Pas de terme source explicite

    elif type_cent == 2:  # Nœud de Dirichlet
        j = np.array([num_cent])
        a = np.array([1])
        b = cl_cent  # La valeur de la condition de Dirichlet

    return j,a,b

def deriv(f_left, f_c, f_right, type_left, type_c, type_right, h):

    # Si le centre n'est pas dans le domaine, v = 0
    if type_c == 0:
        return 0.0

    # Les deux voisins sont valides
    if type_left in (1, 2) and type_right in (1, 2):
        return (f_right - f_left) / (2 * h)

    # Seulement le point à gauche
    if type_left in (1, 2) and type_right == 0:
        return (f_c - f_left) / h

    # Seulement le point à droite
    if type_right in (1, 2) and type_left == 0:
        return (f_right - f_c) / h

    # Aucun voisin n’est utilisable
    return 0.0

def circu(u, v, x, y):

    # Longuer de la courbe de circulation (nbr noeuds)
    lengthCourbe = len(x) - 1

    # Initialisation des var
    c = 0.0

    # Etant une courbe fermee, le dernier noeud est le 1er (range vas de 0 a lengthCourbe - 1)
    for i in range(lengthCourbe):
        # Calcule la variation d'un noeud a  un noeud
        dx = x[i + 1] - x[i]
        dy = y[i + 1] - y[i]
        
        # Si dx = 0 on est sur une paroi verticale -> formule trapezoidale pour l'integrale
        if dx == 0:
            c = c + (v[i] + v[i+1])*dy/2

        # Si dy = 0 la paroi est horizontale
        if dy == 0:
            c = c + (u[i] + u[i+1])*dx/2

    return c

def force(p,x,y):

    # Longuer de la courbe de circulation (nbr noeuds)
    lengthCourbe = len(x) - 1

    # Initialisation des var
    fx = 0.0
    fy = 0.0

    # Etant une courbe fermee, le dernier noeud est le 1er (range vas de 0 a lengthCourbe - 1)
    for i in range(lengthCourbe):
        # Calcule la variation d'un noeud a  un noeud
        dx = x[i + 1] - x[i]
        dy = y[i + 1] - y[i]
        
        # la paroi est verticale
        if dx == 0:
            # on parcour la coube "aire a droite" donc si on monte la pression pointe vers la droite
            # et si on descends p pointe vers la gauche. La drection est contenu dans le signe de dy
            fx = fx + (p[i] + p[i+1])*dy/2

        # la paroi est horizontale
        if dy == 0:    
            # si on vas vers la droite p pointe vers le bas (-x)
            fy = fy - (p[i] + p[i+1])*dx/2

    return fx, fy