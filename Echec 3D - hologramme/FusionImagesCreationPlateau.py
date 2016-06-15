##########################
###   Fusion d'images  ###
##########################

#%%____________________________________________________________________________
# Imports
import matplotlib.pyplot as plt   # nécessaire pour le traitement d'images
import numpy as np                # nécessaire pour manipuler des tableaux (array)
import os 



#%%____________________________________________________________________________
# Placement dans le répertoire
#os.chdir("C:\Users\Nicolas\Documents\Ecole\ISEN\NF - informatique\Projet_fin_d'annee\Pyramide hologramme connectee\Echec 3D - hologramme\Captures") # sous windows
os.chdir("C:\\Users\\vvinc_000\\Desktop\\programmation\\Constellation\\Echec 3D - hologramme") # sous windows


#%%____________________________________________________________________________ 
# Fonction de conversion des images en tableau 22lignes
def imageEnTableau( listeImages ):
    """fonction qui lit et convertit des images png sous forme de tableau
            paramètre : 1 liste de string : la liste des noms des 
                        images à enregistrer
            retourne : 1 liste : les images converties sous forme de tableau
    """
    #Begin
    nbImages = len( listeImages )
    imageTableau = []                           # liste des images converties sous forme de tableau
    
    for image in listeImages :
        #Lecture des images et ajout dans la liste  
        imageLue = plt.imread(image)            # lit l'image /!\ uniquement PNG /!\
        #Conversion des images sous forme de tableau  
        imageTab = imageLue[:, :, 0:3]     # syntaxe sous matplotlib pour transformer l'image en tableau de pixels RVB
        #Ajout à la liste finale
        imageTableau += [ imageTab ]
        #Fermeture de l'image
		plt.close(image)

        
    return imageTableau
    #End



#%%____________________________________________________________________________
# Fonctions de traitement sur deux images 25lignes
def superpose2Images(base, img, imgF):
	"""fonction qui crée une image à partir de la superposition de deux images en comparaison à une base
			paramètres : 3 tableaux = la base de comparaison, l'img qui sera superposée à l'imgF
			retourne : 1 tableau = l'imgF modifiée
    """
   
    #Begin
	print("Traitement en cours...")

	#Calcul du nombre de pixels à fusionner
	if ( (len(base[0]), len(base)) == (len(img[0]), len(img)) ) :
		colonnes = len(base[0])
		lignes = len(base)
	else :
		return ("Erreur : les deux images n'ont pas les même dimentions")

	#Calcul de la valeur des pixels (ligne puis colonne)
	for i in range(lignes):
		for j in range(colonnes):
			p1 = base[i][j]
			p2 = img[i][j]
			if ( (p1[0] != p2[0]) and (p1[1] != p2[1]) and (p1[2] != p2[2]) ) : #comparaison des RVB du pixel
				imgF[i][j] = p2

	#End
	return imgF



#%%____________________________________________________________________________
# Fonctions de traitement sur plusieurs images 28lignes
def superposePlusieursImages(listeImg, orientation):
    """fonction qui crée une image à partir de la fusion de plusieurs images et
    l'enregistre
            paramètres : - 1 liste = contenant les images à superposer, mais ne 
                            contenant pas l'image du plateau de jeu
                         - 1 String = le point de vue pour la prise d'image du plateau
            retourne : 1 tableau = l'image finale
    """
    #Begin
    nbImg = len(listeImg)      # nombre d'images dans la liste
    
    #Conversion des images en tableau
    imageTableau = imageEnTableau( listeImg )
    baseTableau = imageEnTableau( [orientation + "Empty.png"] )[0]
    
    #Création d'une copie de la base = future image fusionnée
    
    imgF = baseTableau.copy()           # ne modifie pas la base 
    if (nbImg != 0):                    # verification qu'il y a des images à fusionner
        #Superposition image par image
        for n in range(nbImg):
            img = imageTableau[n]
            imgF = superpose2Images(baseTableau, img, imgF)
        plt.imsave('imageFusionnee.png', imgF)
        return imgF
        
    else :
		#Erreur : pas d'image dans la liste
		return ("Erreur : il faut entrer une liste contenant des images")
    #End
  
#%%____________________________________________________________________________
# Fonctions de trie de la liste d'images a fusionner (plus facile à lire) 48lignes
def trieListeImageAFusionnerSelonOrientation(listeImageAFusionner, orientation):
	""" fonction qui trie les images pour qu'elles soient dans le bon ordre : la pièce de devant 'ecrase' celle de derrière mais pas l'inverse pour respecter la perspective
			paramètres : - 1 liste = contenant les images à superposer, mais ne 
                            contenant pas l'image du plateau de jeu
                         - 1 string = le point de vue pour la prise d'image du plateau
			retourne : 1 liste = contenant les images à superposer, mais ne 
                            contenant pas l'image du plateau de jeu
	"""
	#Begin
	#Cree une liste contenant les lettres A B C... H dans l'ordre
	listeColonnes = []
	for i in range(ord('A'),ord('H')+1):
		listeColonnes += [chr(i)]			
	
	#On commence le trie	
	listeTriee = []
	if ((orientation == "front") or (orientation == "left")):
		i = 8
		while (i > 0):
			k = 0
			while (k < len(listeImageAFusionner)):
				nomImage = listeImageAFusionner[k]
				if (orientation == "front"):
					if ((orientation in nomImage) and (str(i) in nomImage)):
						listeTriee += [nomImage]
				else :
					if ((orientation in nomImage) and (listeColonnes[i-1] in nomImage)):
						listeTriee += [nomImage]
				k += 1
			i -= 1
	elif ((orientation == "back") or (orientation == "right")) :
		i = 1
		while (i < 9):
			k = 0
			while (k < len(listeImageAFusionner)):
				nomImage = listeImageAFusionner[k]
				if (orientation == "back"):
					if ((orientation in nomImage) and (str(i) in nomImage)):
						listeTriee += [nomImage]
				else :
					if ((orientation in nomImage) and (listeColonnes[i] in nomImage)):
						listeTriee += [nomImage]
				k += 1
			i += 1
	return listeTriee

	
	
#%%____________________________________________________________________________
# Fonctions de trie de la liste d'images a fusionner (plus optimisee) 37lignes	
def trieListeImageAFusionnerSelonOrientation2(listeImageAFusionner, orientation):
	""" fonction qui trie les images pour qu'elles soient dans le bon ordre : la pièce de devant 'ecrase' celle de derrière mais pas l'inverse pour respecter la perspective
			paramètres : - 1 liste = contenant les images à superposer, mais ne 
                            contenant pas l'image du plateau de jeu
                         - 1 string = le point de vue pour la prise d'image du plateau
			sorties : 1 liste = contenant les images à superposer, mais ne 
                            contenant pas l'image du plateau de jeu
	"""
	#Begin
	#On associe un indice à l'orientation pour permettre par la suite un traitement unique pour tous les cas
	listeOrientations = ["back", "front", "right", "left"]
	indiceOrientation = listeOrientations.index(orientation) 	#Trouve l'indice de orientation dans la liste
	
	#Cree une liste contenant les lettres A B C... H dans l'ordre
	listeColonnes = []
	for i in range(ord('A'),ord('H')+1):
		listeColonnes += [chr(i)]			
	
	#On commence le trie	
	print("on tourne pour ", orientation)
	listeTriee = []
	i = 1 + (7 * (indiceOrientation % 2)) #8 quand indice est impaire et 1 sinon
	print("soit un départ pour i = ", i)
	compteur = 1
	while (compteur < 9):
		
		k = 0
		while (k < len(listeImageAFusionner)):
			nomImage = listeImageAFusionner[k]
			if (indiceOrientation < 2):
				if ((orientation in nomImage) and (str(i) in nomImage)):
					listeTriee += [nomImage]
					print("on modifie bien i et on rentre même dans le if indiceorientation qui va bien", i)
			else :
				if ((orientation in nomImage) and (listeColonnes[i] in nomImage)):
					listeTriee += [nomImage]
					print("on modifie bien i et on rentre même dans le if indiceorientation qui va bien", listeColonnes[i])
			k += 1
		i += (-1)**indiceOrientation  #-1 quand indice est impaire et +1 sinon
		compteur += 1
		print("compteur", compteur -1, "et i = ", i)
	return listeTriee


	
#%%____________________________________________________________________________
# Fonction qui produit les images initiales du plateau // non finie	
# def imagesPlateauInitial():
	# """
	# """
	# #Préparatifs
	# listeOrientations = ["front", "right", "left", "back"]
	# listeColonnes = []
	# for i in range(ord('A'),ord('H')+1):
		# listeColonnes += [chr(i)]
	# listeImagesAFusionner = []
	
		
#%%____________________________________________________________________________
# Tests des fonctions


#%%
listeImagesAFusionner = ["frontWhitePawnD2.png", "backWhitePawnE2.png", "frontWhitePawnC3.png", "frontWhitePawnE2.png", "frontWhiteQueenD1.png"]
orientation = "front"
#plt.imshow(superposePlusieursImages(listeImagesAFusionner, orientation))


"""
#%%____________________________________________________________________________
# Trucs à faire

- close image // fait

- Dans superposePlusieursImages remplacer le paramètre <nom_de_limage_de_base> par un String correspondant au nom du point de vue : "front", "back", "left", "right"

- trier images pour qu'elles soit dans le bon ordre : la pièce de devant ecrase celle de derrière mais pas l'inverse


# A faire quand on aura les images

- creer une fonction qui 
	* prend en entree une liste de tuples de la forme (couleur_piece, type_de_piece, position_sur_le_plateau)
	* sort la liste des images a fusionner triee
	/!\	fin
	
- créer une fonction qui fait une image fusionnée pour les 4 points de vues : front, back, left et right
	elle crée donc 4 images

- créer une fonction qui crée le plateau dans l'état de départ et
	enregistre l'image fusionnee
	retourne la liste des images à fusionner (triee)

- créer une fonction qui repart de la dernière position (celle de départ au début/par défaut) et met à jour la 	position des pièces (une vient d'être déplacée)


# On appelera les fonctions dans le jeu js aux moments où on en aura besoin

"""