*******************************************************************
** Instructions pour l'utilisation des fichiers d'initialisation **
*******************************************************************


Conseils pour importer les fichiers dans Python:
------------------------------------------------

Utiliser la commande numpy.loadtxt en pr�cisant le type de donn�es et l'adresse du dossier (path)
ex: my_array = numpy.loadtxt(path + '\\1-num.txt', dtype = int)

La pas de discr�tisation est pr�cis� ci-dessous.


Conventions:
------------

Pour chacune des configurations propos�es, 2 ou 3 matrices sont fournies:
	1) Dans tous les cas: une matrice repr�sentant le domaine g�om�trique (appel�e dom)
	Elle permet d'identifier
		1) les noeuds qui ne doivent pas �tre calcul�s (valeur = 0). Une frange de 0 est plac�e
		autour de chaque domaine.
		2) les noeuds internes qui prennent une valeur = 1.
		3) les noeuds condition limite de Dirichlet qui sont rep�r�s par une valeur = 2.
		
     2) Dans tous les cas: une matrice (appel�e num) qui donne un num�ro de noeud pour chaque noeud de calcul. Cette num�rotation permet d'ordonner le syst�me � r�soudre et commence par 1. Pour plus d'infos, voir la s�ance introductive ou avec les �tudiants-moniteurs.

	3) Pour le canal rectiligne (cas test) : une matrice reprenant les valeurs des conditions de Dirichlet (appel�e cl)

	4) Pour le canal plus complexe avec obstacle : une matrice contenant l'indice des noeuds d�finissant le contour de l'obstacle (2-contourObj.txt).
	
Informations compl�mentaires:
-----------------------------

1) Canal rectiligne - pas spatial = 0,5 m

2) Canal avec obstacle - pas spatial = 1 cm
