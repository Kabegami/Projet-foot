import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction, KeyboardStrategy
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from projet import *
from PlayerDecorator import *
from zone import *
from ia import *

joueurIA = Player("JoueurIA",Monte_Carlo_Strat())
joueur6 = Player("Joueur 6", j_solo)

teamIA = SoccerTeam("teamIA",[joueurIA])
teamAdv = SoccerTeam("teamAdv",[joueur6])
teamAdv2 = SoccerTeam("teamAdv2",[joueur6])

Monte_Carlo("fichier")
match = SoccerMatch(teamIA, teamAdv)
soccersimulator.show(match)
match.save("fichier")

