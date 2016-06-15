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
os.chdir("<chemin_vers_le_repertoire_de_travail>") # différent sous windows ou linux



#%%____________________________________________________________________________ 
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
        
    return imageTableau
    #End



#%%____________________________________________________________________________
# Fonctions de traitement sur deux images
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
# Fonctions de traitement sur plusieurs images
def superposePlusieursImages(listeImg, base):
    """fonction qui crée une image à partir de la fusion de plusieurs images et
    l'enregistre
            paramètres : - 1 liste = contenant les images à superposer, mais ne 
                            contenant pas l'image du plateau de jeu
                         - 1 String = l'image du plateau de jeu
            retourne : 1 tableau = l'image finale
    """
    #Begin
    nbImg = len(listeImg)      # nombre d'images dans la liste
    
    #Conversion des images en tableau
    imageTableau = imageEnTableau( listeImg )
    baseTableau = imageEnTableau( [base] )[0]
    
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
# Tests des fonctions

listeImagesAFusionner = ["frontWhitePawnD2.png", "frontWhitePawnE2.png", "frontWhiteQueenD1.png"]
base = "frontEmpty.png"
superposePlusieursImages(listeImagesAFusionner, base)

