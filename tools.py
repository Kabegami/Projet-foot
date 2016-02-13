import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from zone import *
from PlayerDecorator import *

def fonceur(etat):
    return etat.shoot_but + etat.go_ball

def goal(etat):
    if (etat.distance_ball) < 20:
        return etat.go_ball + etat.degage
    else:
        return etat.go(etat.my_but) + etat.shoot_but


        
