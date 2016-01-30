import projet.py
import tools.py
from projet import *
from tools import *

joueur1 = Player("Joueur1",FoncteurStrategy())
joueur2 = Player("Joueur2",FoncteurStrategy())
joueur3 = Player("Joueur3",FoncteurStrategy())
joueur4 = Player("Joueur4",FoncteurStrategy())

team1 = SoccerTeam("team1",[joueur1])
team1 = SoccerTeam("team1",[joueur1,joueur2])
team1 = SoccerTeam("team1",[joueur1,joueur2,joueur3,joueur4])
