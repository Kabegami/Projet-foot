import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction, KeyboardStrategy
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from projet import *
from PlayerDecorator import *
from zone import *
from exemples import *


joueur1 = Player("Joueur 1", fonceStrat)
joueur2 = Player("Joueur 2", gardien)
joueur3 = Player("Joueur 3", MilieuStrategy())
joueur4 = Player("Joueur 4", attaque)
joueur5 = Player("Joueur 5", defense)
joueur6 = Player("Joueur 6", j_solo)
j7 = Player("passeur",toto)
dio = Player("Dio",dio)
j8 = Player("doge",doge)

team1 = SoccerTeam("team1",[joueur6])
toto_team = SoccerTeam("toto_team",[j7,joueur2])
test = SoccerTeam("test",[j7,joueur2,dio])
test2 = SoccerTeam("test2",[joueur1,joueur2])
test3 = SoccerTeam("test2",[joueur2])
test4 = SoccerTeam("test4",[joueur6])
team2 = SoccerTeam("team2",[joueur2,j8])
team4 = SoccerTeam("team4",[joueur2,j8,joueur5,j8])

#apprentissage superviseshell
strat = KeyboardStrategy()
strat.add("f",fonceStrat)
strat.add("g",gardien)
strat.add("a",attaque)
strat.add("d",defense)

eleve = Player("eleve",strat)
team_spe = SoccerTeam("team_eleve",[eleve])
team_arbre = SoccerTeam("IA",[Player("IA",treeStrat)])

#match = SoccerMatch(team_arbre, team_arbre)
#match = SoccerMatch(test3,toto_team)
#match = SoccerMatch(team4, test2)
#soccersimulator.show(match)
strat.write("mon_fichier.exp")
