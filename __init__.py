from projet import *

joueur1 = Player("Joueur 1", fonceStrat)
joueur2 = Player("Joueur 2", gardien)
joueur3 = Player("Joueur 3", MilieuStrategy())
joueur4 = Player("Joueur 4", attaque)
joueur5 = Player("Joueur 5", defense)
joueur6 = Player("Joueur 6", j_solo)
joueur7 = Player("passeur",toto)
joueur8 = Player("doge",doge)

team1 = SoccerTeam("team2",[joueur6])
team2 = SoccerTeam("team1",[joueur8,joueur2])
team4 = SoccerTeam("team4",[joueur2,joueur8,joueur5,joueur8])
teamIA = SoccerTeam("teamIA",[Player("IA",treeStrat),joueur2]
