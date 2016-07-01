#################################################
### Package Holographer pour le e-Holographer ###
#################################################

import Constellation
#import ScriptRpi
#import FusionImagesCreationPlateau



#%%______________________________________________________________________________
#===== Message Callbacks =====

#Connexion démarrée
@Constellation.MessageCallback()
def InfosConnection():
	"Bouton qui écrit 'connecté' dans la console log"

	Constellation.WriteInfo("Holographer connecté à Constellation")



##Début du jeu
#@Constellation.MessageCallback()
#def PlateauDeDepart():
#	"Bouton qui génère le plateau de départ après la 1ere connexion"

#	Constellation.WriteInfo( "Initialisation du plateau" )
#	#PlateauDeDepart()
#	Constellation.WriteInfo("Génération du plateau terminée")



#En cours de jeu
@Constellation.MessageCallback()
def MAJPlateau(caseDeDepart, caseDarrivee):
	"Bouton qui génère le plateau suivant à partir de 2 integer"

	Constellation.WriteInfo( "MAJ du plateau lancee | [case de depart = " + str(caseDeDepart) + " | case d'arrivee = " + str(caseDarrivee) + "]" )

	deplacement = [caseDeDepart, caseDarrivee]

	if (deplacement == [0, 0]):
		#Creation du plateau de départ quand on est en cours de jeu
		Constellation.WriteInfo( "Initialisation du plateau" )
		#PlateauDeDepart()
		
		##Fermeture d'une eventuelle image
		#os.system( "kill " + str(IdProcI) )

		##Affichage de l'image
		#IdProcI = showImage(cheminScriptImage)

		Constellation.WriteInfo("Génération du plateau terminée")

	else:
		##Mise A Jour (MAJ) de la position des pieces sur le plateau
		#MAJPlateau(caseDeDepart, caseDarrivee)

		##Fermeture d'une eventuelle image
		#os.system( "kill " + str(IdProcI) )

		##Affichage de l'image
		#IdProcI = showImage(cheminScriptImage)
		
		Constellation.WriteInfo("Maj plateau terminée")



#A utiliser quand on aura cree des animations pour les combats entre les différentes pièces
@Constellation.MessageCallback()
def AnimationCombat():
	"Bouton qui lance une animation de combat"

	Constellation.WriteInfo("Animation de combat lancée")



#Fin du jeu
@Constellation.MessageCallback()
def FinDuJeu():
	"Bouton qui signale la fin du jeu"

	Constellation.WriteWarn("Game Over")



#===== State Object =====

#Lancé au démarrage du package
def OnStart():
	Constellation.PushStateObject("Holographer", { "Sender": "Holographer" }, "Info", { "Device_Id": "RPi", "Etat du package":"lancé" })



#%%____________________________________________________________________________________
#Démarrage du package

Constellation.Start(OnStart);



#%%____________________________________________________________________________________
