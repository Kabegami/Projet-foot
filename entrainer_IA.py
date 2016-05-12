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

IA = Monte_Carlo_Strat()

joueurIA = Player("JoueurIA",IA)
#-----------------------------------------------
joueur1 = Player("Joueur 1", fonceStrat)
joueur2 = Player("Joueur 2", gardien)
joueur3 = Player("Joueur 3", MilieuStrategy())
joueur4 = Player("Joueur 4", attaque)
joueur5 = Player("Joueur 5", defense)
joueur6 = Player("Joueur 6", j_solo)
joueur8 = Player("doge",doge)

teamIA = SoccerTeam("teamIA",[joueurIA])
team1 = SoccerTeam("soloT",[joueur6])
team2 = SoccerTeam("goalT",[joueur2])
team3 = SoccerTeam("attaqueT",[joueur4])
team4 = SoccerTeam("dogeT",[joueur8])
team5 = SoccerTeam("fonceT",[joueur1])

#Joueur pour les exemples
#--------------------------------------------------

p1 = ExempleStrat(fonce_Strat)
p2 = ExempleStrat(goal)
p3 = ExempleStrat(attaquant)
p4 = ExempleStrat(evite)
p5 = ExempleStrat(intercepte)

j1 = Player("FonceJ",p1)
j2 = Player("GoalJ",p2)
j3 = Player("AttaqueJ",p3)
j4 = Player("EviteJ",p4)
j5 = Player("IntercepeteJ",p5)

t1 = SoccerTeam("FonceT",[j1])
t2 = SoccerTeam("GoalT",[j2])
t3 = SoccerTeam("AttaqueT",[j3])
t4 = SoccerTeam("EviteT",[j4])
t5 = SoccerTeam("EviteT",[j5])

L1 = [t1,t2,t3,t4]
L2 = [t4,t3,t2,t1]

Liste = []
Liste.append(team1)
Liste.append(team2)
Liste.append(team3)
Liste.append(team4)
Liste.append(team5)

if __name__ == "__main__":
    init_fichier(team1,team2)
    #exemple_tournoi(IA,L1,Liste,1,0,10)
    tournoi_IA(IA,teamIA,Liste,1,0,10,False)
    #affiche_joue_IA(IA,teamIA,team5,1,0)
    M = SoccerMatch(teamIA, team1)
    M.play()
    soccersimulator.show(M)
    enregistre_dico(IA.dico)
