#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Main.py
#  
#  Copyright 2016 Sylvain PRYFER <sylvain@sylvain-HP-Spectre-Pro-x360-G1>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
#%%_______________________________________________________________________________________________
import os
import time



#%%_______________________________________________________________________________________________
cheminScriptVideo = "/home/pi/Desktop/scriptsRpi/bash/scriptVideo"
cheminScriptImage = "/home/pi/Desktop/scriptsRpi/bash/scriptImage"
cheminIdImage = "/home/pi/Desktop/scriptsRpi/bash/IdImage"
cheminIdVideo = "/home/pi/Desktop/scriptsRpi/bash/IdVideo"



#%%_______________________________________________________________________________________________

# fonction permettant d'appeller le script linux qui affiche une image, écrit les erreurs dans ./bash/logImage et l'identifiant du processus dans ./bash/IdImage
def showImage(cheminScriptImage):
        """appelle le script linux qui affiche une image, écrit les erreurs dans ./bash/logImage et l'identifiant du processus dans ./bash/IdImage
                paramètre : 1 String = le chemin d'accès au script
                retourne : 1 int = l'id du processus exécuté
        """

        #ouverture du processus
        os.system(cheminScriptImage)

        #récupération de l'ID du precessus pour pouvoir le fermer plus tard
        IdentifiantProcessustxt = open(cheminIdImage)
        IdProcI = IdentifiantProcessustxt.read()
        IdentifiantProcessustxt.close()
        print IdProcI
        #renvoie l'ID du processus
        return IdProcI



# fonction permettant d'appeller le script linux qui lance une vidéo, écrit les erreurs dans ./bash/logVideo et l'identifiant du processus dans ./bash/IdVideo
def showVideo(cheminScriptVideo):
        """appelle le script linux qui lance une vidéo, écrit les erreurs dans ./bash/logVideo et l'identifiant du processus dans ./bash/IdVideo
                paramètre : 1 String = le chemin d'accès au script
                retourne : 1 int = l'id du processus exécuté
        """
        
        #ouverture du processus
        os.system(cheminScriptVideo)

        #récupération de l'ID du precessus pour pouvoir le fermer plus tard
        IdentifiantProcessustxt = open(cheminIdVideo)
        IdProcV = IdentifiantProcessustxt.read()
        IdentifiantProcessustxt.close()
        print IdProcV
        #renvoie l'ID du processus
        return IdProcV



#%%_______________________________________________________________________________________________

# test
def main():

        #Ouverture d'une image
        IdProcI=showImage(cheminScriptImage)
        print("Image ouverte")
        time.sleep(5)
        #Fermeture de l'image
        tuer = "kill " + str(IdProcI)
        os.system(tuer)
        print("Image fermée")

        #Ouverture d'une vidéo
        IdProcV = showVideo(cheminScriptVideo)
        print("Vidéo ouverte")
        time.sleep(5)
        #Fermeture de la vidéo
        tuer = "kill " + str(IdProcV)
        os.system(tuer)
        print("Vidéo fermée")

        return 0



if __name__ == '__main__':
        main()

