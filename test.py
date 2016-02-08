import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from projet import *
from PlayerDecorator import *

joueur1 = Player("Joueur1",FonceurStrategy())
joueur2 = Player("Joueur2",GardienStrategy())
joueur3 = Player("Joueur3",DefenseurStrategy())
joueur4 = Player("Joueur4",PasseurStrategy())

team1 = SoccerTeam("team1",[joueur1])
team2 = SoccerTeam("team2",[joueur1,joueur2])
team4 = SoccerTeam("team4",[joueur1,joueur1,joueur2,joueur2])

match = SoccerMatch(team2, team2)
soccersimulator.show(match)