
import Constellation
import os 
""""import matplotlib.pyplot as plt     # nécessaire pour le traitement d'images
import matplotlib.image as mpimg    # nécessaire pour le traitement d'images
from numpy import ndarray           # utile pour resize 
import numpy as np
import scipy as sc
from scipy import ndimage # utile pour rotate


def regroupe4ImagesEn1(Alias, chemin):
    Fonction qui regroupe les 4 images correspondant aux 4 orientations en une seule image a projeter sur la pyramide
            parametre : 1 String  = le nom de l'image a fusionner (sans l'orientation devant)
            retourne : 1 String = le chemin de l'image fusionnee
    
    #Begin

    #importation des images
    front = mpimg.imread(chemin)
    print("Images importees")

    #rotation des images
    rotateRight = ndimage.rotate(front, 270)
    rotateBack = ndimage.rotate(front, 180)
    rotateLeft = ndimage.rotate(front, 90)
    print("Images retournees")

    #creation de la "base" ou "coller" les quatre images ci-dessus
    lignes, colonnes = dimensionImage(front) 
    print("les dimensions sont : lignes  = ",lignes," colonnes = ", colonnes)
    
    dimension = lignes*2 + colonnes
    base = np.zeros((dimension,dimension,3), dtype='f')
    print("base crÃ©Ã©e : dimension = ", dimension," et ", dimensionImage(left) )

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
                nouveauChemin = os.chdir(os.path.expanduser('~')+'\\Desktop\\EHolographerW')+'\\'+Alias

                plt.imsave(nouveauChemin,base)
    return(nouveauChemin)         
"""
#%%______________________________________________________________________________
# Procedure permettant d'afficher une image ou une video sous windows
def callWMplayer(chemin):
    """ procedure qui lance Windows Media Player en plein ecran
        parametre chemin vers l'image ou la video
    """

    """  'CALL' est une instruction windows qui lanc    e un programme
         le premier chemin est celui vers windows media player
         le second est le chemin variable vers le fichier a ouvrir    
    """
    os.system('CALL "C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe" /fullscreen '+chemin)
 

# Message Callback creant un fichier d'index sur le bureau
@Constellation.MessageCallback()
def InitialisationIndex():
    
    #change le chemin actuel pour aller sur le bureau
    os.chdir(os.path.expanduser('~')+'\\Desktop')
    #cree un dossier eholographer sur le bureau
    if not(os.path.exists(os.path.expanduser('~')+'\\Desktop\\EHolographerW')):
        os.mkdir(os.path.expanduser('~')+'\\Desktop\\EHolographerW')

    
    #change pour se mettre dans le dossier eholographer
    os.chdir(os.path.expanduser('~')+'\\Desktop\\EHolographerW')
    #creer le fichier d'index
    fichier = open('Index.txt','w')
    #ecrit les consignes dans le fichier
    fichier.write('Veuillez ecrire les ligne de la forme "Alias" "Chemin" ')
    fichier.close()

#Meassage Callback qui ajoute un element a l'index
@Constellation.MessageCallback()
def AjoutElementIndex(Alias, Path, type):
    """Procedure ajoutant un element a l'index
        Parametre : 1 string = le nom avec lequel on veut appeler l'element
                    1 string = le chemin vers l'element
    """
    Constellation.WriteInfo("on est la ")

    if str(type) in {'I','i','P','p','Image','image','picture','Picture'}:
        
        Constellation.WriteInfo("on est la ")
        #nouveauChemin = regroupe4ImagesEn1(Alias, Path)
        Path = nouveauChemin

    #change le repertoire de travail pour le bureau
    os.chdir(os.path.expanduser('~')+'\\Desktop\\EHolographerW')
    #ouvre le fichier d'index en mode ajouter du texte
    fichier = open('Index.txt','a')
    # écrit un retour a la ligne puis les caracteristique de l'element
    fichier.write("\n" + Alias + " " + Path)
    fichier.close()


#Message Callback affichant 
@Constellation.MessageCallback()
def showVideo(Alias):
    """ procedure pour lancer une video
        parametre : 1 string = le nom que l'on a definis pour l'element
    """
    
    #change le repertoire de travail pour le Bureau
    os.chdir(os.path.expanduser('~')+'\\Desktop\\EHolographerW')
    #ouvre le fichier d'index en mode lecture
    fichier = open('Index.txt','r')

    #recherche de l'alias dans le fichier
    contenu = fichier.readlines()
    nombreLigne = len(contenu)
    i = 0
    while (i < (nombreLigne - 1)):
        i = i + 1
        Ligne = contenu[i]
        Separe = Ligne.split()
        if Alias == Separe[0]:
            #lance la video par windows media player
            callWMplayer(Separe[1])
            break

    fichier.close()
   


def OnExit():
    pass

def OnStart():
    # Register callback on package shutdown
    Constellation.OnExitCallback = OnExit   
   
    # Last StateObjects of the previous instance
    if Constellation.LastStateObjects:
        for so in Constellation.LastStateObjects:
            Constellation.WriteInfo(" + %s @ %s" % (so.Name, so.LastUpdate))

Constellation.Start(OnStart);