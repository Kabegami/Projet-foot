import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction, KeyboardStrategy
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from projet import *
from PlayerDecorator import *
from tools import *
from zone import *
from ia import *
import pickle

IA = Monte_Carlo_Strat()
joueurIA = Player("JoueurIA",IA)
joueur6 = Player("Joueur 6", j_solo)

teamIA = SoccerTeam("teamIA",[joueurIA])
teamAdv = SoccerTeam("teamAdv",[joueur6])
teamAdv2 = SoccerTeam("teamAdv",[joueur2])


init_fichier(teamAdv,teamAdv2)
if os.path.getsize("action") != 0:
    a = open("action","a")
    for i in range(0,10):
        a.write("\n goal")
    a.close()
    f = open('dico_apprentissage','r')
    dicoIA = pickle.load(f)
    f.close()
    dicoIA = dict()
    Monte_Carlo("fichier","action",dicoIA,1,0)
    print("enregistre le dico")
    enregistre_dico(dicoIA)

#on supprime le fichier action apres l'apprentissage
a = open("action","w")
a.close()

if __name__ == "__main__":
    match = SoccerMatch(teamIA, teamAdv2)
    #on efface l'ancien match
    a = open("fichier","w")
    a.close()
    
    
    #Si on veut enregister le dictionnaire
    temp = sys.stdout
    sys.stdout = open("dico_apprentissage","w")
    print(IA.dico)
    sys.stdout.close()
    sys.stdout = temp
    
    soccersimulator.show(match)
    match.save("fichier")

#pb : Comment notre joueur perd contre l'attaquant et a match nulle contre le defenseur donc il ne change pas asser, il faut donc que je lui donnes des examples avec la KeyBoard Strat
# et on observe que l'exploration est tres longue
