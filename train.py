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
test= StratStateless(attaquant2)

joueurIA = Player("JoueurIA",IA)
joueur6 = Player("Joueur 6", j_solo)
jtest = Player("jTest",test)

teamIA = SoccerTeam("teamIA",[joueurIA])
teamAdv = SoccerTeam("teamAdv",[joueur6])
teamAdv2 = SoccerTeam("teamAdv2",[jtest])

Monte_Carlo("fichier","action",IA,1,0)
match = SoccerMatch(teamIA, teamAdv2)
soccersimulator.show(match)
match.save("fichier")

