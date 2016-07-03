###################     
### Holographer ###
###################

import Constellation
import os



#%%______________________________________________________________________________
# Fonction permettant d'afficher une vidéo sous windows
def callVideoWindows(instruction,  logiciel, chemin):
    """
    
    """
    os.system('CALL '+logiciel+' '+chemin)
 


@Constellation.MessageCallback()
def CallVideo(data):
    if int(data) == 1:
        callVideo('CALL', '"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc"', '"D:\\Autre\\Demo.mp4"')

        Constellation.WriteInfo(data)
    if int(data) == 2 : 
        callVideo('CALL', '"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc"', '"D:\\Autre\\Chess.mp4"')

        Constellation.WriteInfo(data)
        


#%%____________________________________________________________________________________

Constellation.Start()
