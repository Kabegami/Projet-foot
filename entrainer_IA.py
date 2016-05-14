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

IA = Monte_Carlo_Strat("dico_apprentissage")
IAD = Monte_Carlo_Strat("dico_apprentissage_duo")

joueurIA = Player("JoueurIA",IA)
joueurIAD = Player("JoueurIA",IAD)
#-----------------------------------------------
inter = StratStateless(intercepte)
passe = StratStateless(passeStrat)

joueur1 = Player("Joueur 1", fonceStrat)
joueur2 = Player("Joueur 2", gardien)
joueur4 = Player("Joueur 4", attaque)
joueur5 = Player("Joueur 5", defense)
joueur6 = Player("Joueur 6", j_solo)
joueur8 = Player("doge",doge)
joueur7 = Player("Joueur 7", inter)
joueur9 = Player("Joueur 9",passe)

teamIA = SoccerTeam("teamIA",[joueurIA])
teamIAD = SoccerTeam("teamIAD",[joueurIA,joueur2])
team1 = SoccerTeam("soloT",[joueur6])
team2 = SoccerTeam("goalT",[joueur2])
team3 = SoccerTeam("attaqueT",[joueur4])
team4 = SoccerTeam("dogeT",[joueur8])
team5 = SoccerTeam("fonceT",[joueur1])
team6 = SoccerTeam("intercepteT",[joueur7])

#Joueur pour les exemples
#--------------------------------------------------

p1 = ExempleStrat(fonce_Strat)
p2 = ExempleStrat(goal)
p3 = ExempleStrat(attaquant)
p4 = ExempleStrat(evite)
p5 = ExempleStrat(intercepte)
p6 = ExempleStrat(passeStrat)

j1 = Player("FonceJ",p1)
j2 = Player("GoalJ",p2)
j3 = Player("AttaqueJ",p3)
j4 = Player("EviteJ",p4)
j5 = Player("IntercepeteJ",p5)
j6 = Player("PasseStrat",p6)

t1 = SoccerTeam("FonceT",[j1])
t2 = SoccerTeam("GoalT",[j2])
t3 = SoccerTeam("AttaqueT",[j3])
t4 = SoccerTeam("EviteT",[j4])
t5 = SoccerTeam("IntercepteT",[j5])

#team equipe duo pour l'IA
d1 = SoccerTeam("D1",[j1,joueur2])
d2 = SoccerTeam("D2",[j4,joueur2])
d3 = SoccerTeam("D3",[j3,joueur2])
d4 = SoccerTeam("D4",[j2,joueur4])
d5 = SoccerTeam("D5",[j5,joueur4])
d6 = SoccerTeam("D6",[j6,joueur2])

#team duo normal

duo1 = SoccerTeam("Duo1",[joueur1,joueur2])
duo2 = SoccerTeam("Duo2",[joueur8,joueur2])
duo3 = SoccerTeam("Duo3",[joueur4,joueur2])
duo4 = SoccerTeam("Duo4",[joueur7,joueur4])
duo5 = SoccerTeam("Duo5",[joueur7,joueur2])
duo6 = SoccerTeam("Duo6",[joueur9,joueur4])


L1 = [t1,t2,t3,t4]
L2 = [t4,t3,t2,t1]


D1= [d1,d2,d3,d4,d5]
D2= [d5,d4,d3,d2,d1]

Liste = []
Liste.append(team1)
Liste.append(team2)
Liste.append(team3)
Liste.append(team4)
Liste.append(team5)
Liste.append(team6)

ListeT = []
ListeT.append(duo1)
ListeT.append(duo2)
ListeT.append(duo3)
ListeT.append(duo4)
ListeT.append(duo5)
ListeT.append(duo6)

if __name__ == "__main__":
    init_fichier(team1,team2)
    #exemple_tournoi(IA,L1,Liste,1,0,10)
    tournoi_IA(IA,teamIAD,ListeT,1,0,20,False)
    #affiche_joue_IA(IA,teamIA,team5,1,0)
    M = SoccerMatch(teamIAD, duo1)
    M.play()
    soccersimulator.show(M)
    enregistre_dico(IA.dico,"dico_apprentissage")
