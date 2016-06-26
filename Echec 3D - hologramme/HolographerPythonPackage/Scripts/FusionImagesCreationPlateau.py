##########################
###   Fusion d'images  ###
##########################
"""
Script contenant toutes les fonctions nécessaires pour créer et mettre à jour les images du plateau de jeu
Ce script est utilisé dans le package du e-Holographer
"""



#%%____________________________________________________________________________
# Imports
import matplotlib.pyplot as plt     # nécessaire pour le traitement d'images
import matplotlib.image as mpimg    # nécessaire pour le traitement d'images
from numpy import ndarray           # utile pour resize 
import numpy as np
import scipy as sc
from scipy import ndimage           # utile pour rotate
import os 



#%%____________________________________________________________________________
# Placement dans le répertoire
os.chdir("<Chemin_vers_le_bon_repertoire_a_inserer_ici>") # != sous windows et sous linux



#%%____________________________________________________________________________ 
# Fonction de conversion des images en tableau (8lignes)
def imageEnTableau( listeImages ):
    """fonction qui lit et convertit des images png sous forme de tableau
            paramètre : 1 liste de String = la liste des noms des images à enregistrer
            retourne : 1 liste = les images converties sous forme de tableau
    """
    #Begin
    nbImages = len( listeImages )
    imageTableau = []                           # liste des images converties sous forme de tableau
    
    for image in listeImages :
        #Lecture des images et ajout dans la liste  
        imageLue = plt.imread(image)            # lit l'image /!\ uniquement PNG /!\
        #Conversion des images sous forme de tableau  
        imageTab = imageLue[:, :, 0:3]          # syntaxe sous matplotlib pour transformer l'image en tableau de pixels RVB (on enlève le canal alpha)
        #Ajout à la liste finale
        imageTableau += [ imageTab ]
        #Fermeture de l'image
        plt.close(image)

        
    return imageTableau
    #End

    

#%%____________________________________________________________________________
# Fonction qui renvoie les dimensions d'une image (3lignes)
def dimensionImage(image) :
    """Fonction qui renvoie les dimensions d'une image 
        paramètre : 1 np.array (au moins bidimensionnel) = une image
        retourne : 1 2-uple = les dimensions de l'image
    """
    #Begin
    colonnes = len(image[0])
    lignes = len(image)

    return (lignes, colonnes)
    #End

    

#%%____________________________________________________________________________
# Fonctions de traitement sur deux images (13lignes)
def superpose2Images(base, img, imgF):
    """fonction qui crée une image à partir de la superposition de 2 images en comparaison à 1 base (plateau vide)
            paramètres :    - 1 tableau = l'image de la base utilisée pour réaliser la comparaison
                            - 1 tableau = l'image qui sera superposée à l'image que l'on veut modifier
                            - 1 tableau = l'image que l'on veut modifier
            retourne : 1 tableau = l'image modifiée
    """
   
    #Begin
    print("Traitement en cours...")
    
    #Calcul du nombre de pixels à fusionner et vérification que les deux images sont de mêmes dimensions
    if ( (len(base[0]), len(base)) == (len(img[0]), len(img)) ) :
        colonnes = len(base[0])
        lignes = len(base)
    else :
        return ("Erreur : les deux images n'ont pas les même dimensions")
        
    #Calcul de la valeur des pixels (ligne puis colonne)
    for i in range(lignes):
        for j in range(colonnes):
            p1 = base[i][j]
            p2 = img[i][j]
            if ( (p1[0] != p2[0]) and (p1[1] != p2[1]) and (p1[2] != p2[2]) ) : #comparaison des niveaux de couleurs RVB des pixels
                imgF[i][j] = p2
    return imgF
    #End



#%%____________________________________________________________________________
# Fonctions de traitement sur plusieurs images (12lignes)
def superposePlusieursImages(listeImg, orientation):
    """fonction qui crée une image à partir de la fusion de plusieurs images et l'enregistre
            paramètres : - 1 liste = contenant les images à superposer, mais ne 
                            contenant pas l'image du plateau de jeu
                         - 1 String = le point de vue pour la prise d'image du plateau
            retourne : 1 tableau = l'image finale
    """
    #Begin
    nbImg = len(listeImg)        # nombre d'images dans la liste
    
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
        plt.imsave(orientation+'ImageFusionnee.png', imgF)
        return imgF
        
    else :
        #Erreur : pas d'image dans la liste
        return ("Erreur : il faut entrer une liste contenant des images")
    #End

    
    
#%%____________________________________________________________________________
# Fonctions de trie de la liste d'images a fusionner (27lignes) 
def trieListeImageAFusionnerSelonOrientation(listeImageAFusionner, orientation):
    """ fonction qui trie les images pour qu'elles soient dans le bon ordre : 
    la pièce de devant 'ecrase' celle de derrière mais pas l'inverse 
    pour respecter la perspective
            paramètres : - 1 liste = contenant les images à superposer, 
                                    mais ne contenant pas l'image du plateau de jeu
                         - 1 String = le point de vue pour la prise d'image du plateau
        retourne : 1 liste = contenant les images à superposer, 
                            mais ne contenant pas l'image du plateau de jeu
    """
    #Begin

    #On associe un indice à l'orientation pour permettre par la suite un traitement unique pour tous les cas
    listeOrientations = ["back", "front", "right", "left"]
    indiceOrientation = listeOrientations.index(orientation)    #Trouve l'indice d'une orientation donnee dans la liste
    
    #Cree une liste contenant les lettres A B C... H dans l'ordre
    listeColonnes = []
    for i in range(ord('A'),ord('H')+1):
        listeColonnes += [chr(i)]           

    #On commence le trie    
    print("on tourne pour ", orientation)
    listeTriee = []
    i = 1 + (7 * (indiceOrientation % 2)) # 8 quand indice est impaire {front et left} et 1 sinon {back et right}
    print("soit un départ pour i = ", i)
    compteur = 1
    while (compteur < 9):
        k = 0
        while (k < len(listeImageAFusionner)):
            nomImage = listeImageAFusionner[k]
            #On traite ensemble les cas {front et back}
            if (indiceOrientation < 2):
                if ((orientation in nomImage) and (str(i) in nomImage)):
                    listeTriee += [nomImage]
                    print("on modifie bien i et on rentre même dans le if indiceorientation qui va bien", i)
            #On traite ensemble les cas {left et right}
            else :
                if ((orientation in nomImage) and (listeColonnes[i - 1] in nomImage)):
                    listeTriee += [nomImage]
                    print("on modifie bien i et on rentre même dans le if indiceorientation qui va bien", listeColonnes[i - 1])
            k += 1
        i += (-1)**indiceOrientation  # -1 quand indice est impaire {front et left} et +1 sinon {back et right}
        compteur += 1
        print("compteur", compteur -1, "et i = ", i)

    return listeTriee
    #End

    
    
#%%____________________________________________________________________________
# Fonctions qui associe le numéro de case à ses coordonnées (7lignes)  
def associeNumCaseACoordonnees(numeroCase):
    """Fonction qui associe le numéro de case à ses coordonnées
            paramètre : 1 int = numero de la case
            retourne : 1 str = les coordonnees de la case
    """
    #Cree une liste contenant les lettres A B C... H dans l'ordre
    listeColonnes = []
    for i in range(ord('A'),ord('H')+1):
        listeColonnes += [chr(i)]
    
    #Force numeroCase en entier
    numeroCase = int(numeroCase)
    
    #Associe à l'unité la lettre qui correspond
    lettre = listeColonnes[numeroCase%10 - 1]
    
    #Associe à la dizaine le chiffre qui correspond
    chiffre = str(numeroCase - numeroCase%10 - 1)

    return(lettre+chiffre)

    
    
#%%____________________________________________________________________________
# Fonction qui produit les images initiales du plateau (16lignes)
def imagesPlateauInitial(nomImage):
    """Fonction qui crée le plateau dans l'état de départ et
         enregistre les 4 images suivant les 4 points de vue
                paramètre : 1 String = le nom de l'image a enregistrer (sans l'orientation devant)
                retourne : 1 liste = liste des images à fusionner (triee)
    """
    #Begin
    
    #On associe un indice à l'orientation pour permettre par la suite un traitement unique pour tous les cas
    listeOrientations = ["back", "front", "right", "left"]
    
    #Cree une liste contenant les lettres A B C... H dans l'ordre
    listeColonnes = []
    for i in range(ord('A'),ord('H')+1):
        listeColonnes += [chr(i)]   
    
    #On commence a creer les images du plateau initial 
    listeImages = ["WhiteRookA1.png", "WhiteKnightB1.png", "WhiteBishopC1.png", "WhiteQueenD1.png", "WhiteKingE1.png", "WhiteBishopF1.png", "WhiteKnightG1.png", "WhiteRookH1.png", "WhitePawnA2.png", "WhitePawnB2.png", "WhitePawnC2.png", "WhitePawnD2.png", "WhitePawnE2.png", "WhitePawnF2.png", "WhitePawnG2.png", "WhitePawnH2.png", "BlackRookA8.png", "BlackKnightB8.png", "BlackBishopC8.png", "BlackQueenD8.png", "BlackKingE8.png", "BlackBishopF8.png", "BlackKnightG8.png", "BlackRookH8.png", "BlackPawnA7.png", "BlackPawnB7.png", "BlackPawnC7.png", "BlackPawnD7.png", "BlackPawnE7.png", "BlackPawnF7.png", "BlackPawnG7.png", "BlackPawnH7.png"]
    
    #On renomme toutes les images avec l'orientation en debut
    listeImagesAFusionner = []
    listeImagesAFusionnerTriee = []
    nombreImages = len(listeImages)
    for i in range(4):
        orientation = listeOrientations[i]
        for j in range(nombreImages):
            listeImagesAFusionner += [orientation + listeImages[j]] #produit le nom del'image sous la forme "frontWhiteRookA1" et l'insere dans la liste
        listeImagesAFusionnerTriee += trieListeImageAFusionnerSelonOrientation(listeImagesAFusionner[nombreImages*i : (nombreImages*(i+1))], orientation)
        imageFusionnee = superposePlusieursImages(listeImagesAFusionnerTriee[nombreImages*i : (nombreImages*(i+1))], orientation)
        plt.imsave(orientation+nomImage+".png",imageFusionnee)
    #return (listeImagesAFusionnerTriee)

    return (listeImages)
    #End

    
    
#%%____________________________________________________________________________
# Fonction qui met à jour la liste des images à fusionner (20lignes)
def MAJListImage(listeImagesOld, caseDepart, caseArrivee):
    """Fonction qui met à jour la liste des images à fusionner
            paramètre : 1 liste = ancienne liste des pieces du plateau avec leur position
                        2 int = numeros des cases modifiees
            retourne : 1 liste = nouvelle liste des pieces du plateau avec leur position
    """
    #Associe les coordonnees au numero de la case
    coordonneesCaseDepart = associeNumCaseACoordonnees(caseDepart)
    coordonneesCaseArrivee = associeNumCaseACoordonnees(caseArrivee)
    
    #Recuperation du nom de la piece dans la liste ainsi que sa position dans celle-ci et de même pour l'éventuelle piece prise lors du mouvement
    nombrePieces = len(listeImagesOld)
    
    #On initialise à vide la piece bougee et prise pour reconnaitre pouvoir retourner une erreur si aucune pice n'est bougee
    pieceBougee, indicePieceBougee = "",0
    piecePrise, indicePiecePrise = "",0
    
    for i in range(nombrePieces) :
        if (coordonneesCaseDepart in listeImagesOld[i]):
            pieceBougee, indicePieceBougee = listeImagesOld[i], i
            
        elif (coordonneesCaseArrivee in listeImagesOld[i]):
            piecePrise, indicePiecePrise = listeImagesOld[i], i
    
    #On verifie qu'une piece est bien bougee
    if (pieceBougee, indicePieceBougee == "",0):
        return ("erreur : aucune piece sur la case selectionnee")
    
    #On modifie maintenant les coordonnees de la piece bougee 
    longueurNomPiece = len(pieceBougee)
    pieceBougee = pieceBougee[:longueurNomPiece- 2] + coordonneesCaseArrivee
    listeImagesOld[indicePieceBougee] = pieceBougee
    
    #On verifie si une piece est prise et on la supprime si oui
    if (piecePrise, indicePiecePrise == "",0) :
        listeImagesNew = listeImagesOld[: indicePiecePrise]+listeImagesOld[indicePiecePrise + 1 :]
    else :
        listeImagesNew = listeImagesOld
    
    return (listeImagesNew)
    #End
    
    

#%%____________________________________________________________________________
# Fonction qui produit les images initiales du plateau (19lignes)
def initialisationOuMAJImagesPlateau(nomImage, listeImagesOld, caseDepart, caseArrivee):
    """Fonction qui crée le plateau en cours de partie et
         enregistre les 4 images suivant les 4 points de vue
                paramètre : 1 String = le nom de l'image a enregistrer (sans l'orientation devant)
                            1 liste = ancienne liste des pieces du plateau avec leur position 
                                        (mettre une liste vide pour initialiser le plateau)
                            2 int = numeros des cases modifiees 
                                        (mettre à 0 s'il n'y a pas de modification du plateau)
                                Pour le plateau de depart : initialisationOuMAJImagesPlateau(nomImage, [], 0, 0)
                retourne : 1 liste = nouvelle liste des pieces du plateau avec leur position
    """
    #Begin
    
    #On associe un indice à l'orientation pour permettre par la suite un traitement unique pour tous les cas
    listeOrientations = ["back", "front", "right", "left"]
    
    #Cree une liste contenant les lettres A B C... H dans l'ordre
    listeColonnes = []
    for i in range(ord('A'),ord('H')+1):
        listeColonnes += [chr(i)]   
    
    #On commence par creer les images du plateau initial si il n'y a pas encore eu de liste d'images
    if (listeImagesOld == []) :
        listeImagesNew = ["WhiteRookA1", "WhiteKnightB1", "WhiteBishopC1", "WhiteQueenD1", "WhiteKingE1", "WhiteBishopF1", "WhiteKnightG1", "WhiteRookH1", "WhitePawnA2", "WhitePawnB2", "WhitePawnC2", "WhitePawnD2", "WhitePawnE2", "WhitePawnF2", "WhitePawnG2", "WhitePawnH2", "BlackRookA8", "BlackKnightB8", "BlackBishopC8", "BlackQueenD8", "BlackKingE8", "BlackBishopF8", "BlackKnightG8", "BlackRookH8", "BlackPawnA7", "BlackPawnB7", "BlackPawnC7", "BlackPawnD7", "BlackPawnE7", "BlackPawnF7", "BlackPawnG7", "BlackPawnH7"]
    
    #Sinon s'il il n'y a pas de modification on retourne simplement la liste des images pour eviter de perdre du temps à recalculer le plateau  
    elif (caseDepart == 0 or caseArrivee == 0) : 
        return(listeImagesOld)
        
    #Sinon on cree la nouvelle liste d'image en fonction de l'ancienne et de la piece deplacee
    else :
        listeImagesNew = MAJListImage(listeImagesOld, caseDepart, caseArrivee)
    
    #On renomme toutes les images avec l'orientation en debut
    listeImagesAFusionner = []
    listeImagesAFusionnerTriee = []
    nombreImages = len(listeImages)
    for i in range(4):
        orientation = listeOrientations[i]
        for j in range(nombreImages):
            listeImagesAFusionner += [orientation + listeImages[j] + ".png"] #produit le nom del'image sous la forme "frontWhiteRookA1.png" et l'insere dans la liste
        listeImagesAFusionnerTriee += trieListeImageAFusionnerSelonOrientation(listeImagesAFusionner[nombreImages*i : (nombreImages*(i+1))], orientation)
        imageFusionnee = superposePlusieursImages(listeImagesAFusionnerTriee[nombreImages*i : (nombreImages*(i+1))], orientation)
        plt.imsave(orientation+nomImage+".png",imageFusionnee)
    return (listeImagesNew)
    #End


    
#%%____________________________________________________________________________
# Fonction qui cree l'image à projeter  (30lignes)
def regroupe4ImagesEn1(nomImage):
    """Fonction qui regroupe les 4 images correspondant aux 4 orientations en une seule image a projeter sur la pyramide
            paramètre : 1 String  = le nom de l'image a fusionner (sans l'orientation devant)
            retourne : 1 np.array = l'image fusionnee
    """
    #Begin

    #importation des images
    front = mpimg.imread("front"+nomImage+".png")
    right = mpimg.imread("right"+nomImage+".png")
    back = mpimg.imread("back"+nomImage+".png") 
    left = mpimg.imread("left"+nomImage+".png")
    print("Images importées")

    #rotation des images
    rotateRight = ndimage.rotate(right, 270)
    rotateBack = ndimage.rotate(back, 180)
    rotateLeft = ndimage.rotate(left, 90)
    print("Images retournées")

    #creation de la "base" ou "coller" les quatre images ci-dessus
    lignes, colonnes = dimensionImage(front) 
    print("les dimensions sont : lignes  = ",lignes," colonnes = ", colonnes)
    print("on entre dans le if ? : ", ((lignes, colonnes) == dimensionImage(back))," and ",( (colonnes, lignes) == dimensionImage(rotateRight) == dimensionImage(rotateLeft)) )
    
    if ( ((lignes, colonnes) == dimensionImage(back)) and ( (colonnes, lignes) == dimensionImage(rotateRight) == dimensionImage(rotateLeft)) ) :
        print("les dimensions sont bonnes")
        dimension = lignes*2 + colonnes
        base = np.zeros((dimension,dimension,3), dtype='f')
        print("base créée : dimension = ", dimension," et ", dimensionImage(left) )

        #insertion des images dans la base
        for i in range(dimension):
            for j in range(dimension):          
                #insertion de back
                if ( (i < lignes) and (lignes <= j < lignes + colonnes) ):
                    base[i][j] = rotateBack[i][j - lignes][0:3]
                    #print("pixel position : i = ",i," et j = ",j)
                #insertion de right 
                elif ( (lignes <= i < lignes + colonnes) and (j < lignes) ):
                    base[i][j] = rotateRight[i - lignes][j][0:3]
                    #print("pixel position : i = ",i," et j = ",j)
                #insertion de left
                elif ( (lignes <= i < lignes + colonnes) and (lignes + colonnes <= j < dimension ) ) :
                    base[i][j] = rotateLeft[i - lignes][j - lignes - colonnes][0:3]
                    #print("pixel position : i = ",i," et j = ",j)
                #insertion de front
                elif ( (lignes + colonnes <= i < dimension) and (lignes <= j < lignes + colonnes) ) :
                    base[i][j] = front[i - lignes - colonnes][j - lignes][0:3]
                    #print("pixel position : i = ",i," et j = ",j)
        plt.imsave('imageAProjeter.png',base)
        return(base)        
    #si les dimensions ne sont pas bonnes
    return("erreur : les images doivent avoir les memes dimentions")    
    #End    

    
    
#%%____________________________________________________________________________
# Fonction qui cree l'image à projeter (4lignes)
def creePlateauHolographique(nomImage, listeImagesOld, caseDepart, caseArrivee):
    """Fonction qui regroupe les 4 images correspondant aux 4 orientations en une seule image a projeter sur la pyramide
        paramètre : 1 String = le nom de l'image a enregistrer puis fusionner(sans l'orientation devant)
                    1 liste = ancienne liste des pieces du plateau avec leur position 
                                (mettre une liste vide pour initialiser le plateau)
                    2 entiers = numero de la cases modifiees 
                                (mettre à 0 s'il n'y a pas de modification du plateau)
        retourne :  1 liste = liste des images à fusionner (triee)
                    1 np.array = l'image fusionnee
    """
    #Begin
    listeImagesNew = initialisationOuMAJImagesPlateau(nomImage, listeImagesOld, caseDepart, caseArrivee)    #cree les quatres images du plateau initial et la nomme : orientation+nomImage+.png
    
    #Si il y a du changement on recree imageHolographique
    if (listeImagesNew!=listeImagesOld) :
        imageHolographique = regroupe4ImagesEn1(nomImage)       #regroupe les quatres images du nom "orientation+nomImage+.png" en une seule à projeter
    
    return (listeImagesNew)
    #End


    
#%%____________________________________________________________________________
# Tests des fonctions

# listeImagesAFusionnerTest0 = ["frontWhitePawnD2.png", "frontWhitePawnD2.png", "frontWhitePawnD2.png", "frontWhitePawnD2.png", "frontWhitePawnD2.png", "frontWhitePawnD2.png", "frontWhitePawnD2.png",  "backWhitePawnE2.png", "frontWhitePawnE2.png", "frontWhiteQueenD1.png"]
# orientation = "front"
#plt.imshow(superposePlusieursImages(listeImagesAFusionner, orientation))
# listeImagesAFusionnerTest1 = imagesPlateauInitial()
# imageHolo = creeImageHolographique('WhiteQueenD1')
# plt.imshow(imageHolo)
#listeImagesAFusionner, imageHolographique = creePlateauHolographique('_2_Test')


"""
#%%=============================================================================
# Trucs à faire

- close image // fait

- Dans superposePlusieursImages remplacer le paramètre <nom_de_limage_de_base> par un String correspondant au nom du point de vue : "front", "back", "left", "right"

- trier images pour qu'elles soit dans le bon ordre : la pièce de devant ecrase celle de derrière mais pas l'inverse


# A faire quand on aura les images

- creer une fonction qui 
    * prend en entree une liste de tuples de la forme (couleur_piece, type_de_piece, position_sur_le_plateau)
    * sort la liste des images a fusionner triee
    /!\ fin
    
- créer une fonction qui fait une image fusionnée pour les 4 points de vues : front, back, left et right
    elle crée donc 4 images

- créer une fonction qui crée le plateau dans l'état de départ et
    enregistre l'image fusionnee
    retourne la liste des images à fusionner (triee)

- créer une fonction qui repart de la dernière position (celle de départ au début/par défaut) et met à jour la  position des pièces (une vient d'être déplacée)


# On appelera les fonctions dans le jeu js aux moments où on en aura besoin

#%%=============================================================================
"""
  
 