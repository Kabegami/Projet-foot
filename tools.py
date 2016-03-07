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
        return etat.go_ball + etat.degage(etat.my_zone)
    else:
        return etat.go(etat.my_but) + SoccerAction(Vector2D(5,0),Vector2D(0,0)) + etat.shoot_but

def defenseur(etat):
    if etat.distance_ball < etat.adv_proche_distance or not(etat.balle_dans_zone(etat.my_but_zone)):
        return attaquant(etat)
    if etat.balle_dans_zone(etat.my_zone.division_horizontale[0]):
        return etat.go(etat.my_zone.division_horizontale[1].division_verticale[1].milieu) + etat.shoot_but
    if etat.balle_dans_zone(etat.my_zone.division_horizontale[1]):
        return etat.go(etat.my_zone.division_horizontale[0].division_verticale[0].milieu) + etat.shoot_but
    else:
        return attaquant(etat)

def solo(etat):
    if etat.balle_dans_zone(etat.my_zone):
        return goal(etat)
    else:
        return attaquant(etat)

def attaquant(etat):
    if etat.dans_zone(etat.adv_but_zone,etat.my_position):
        return etat.vise_but
    else:
        return etat.go_ball + etat.drible_but

def campe(etat):
    if etat.distance_ball < 20:
        if etat.my_position.distance(etat.adv_but) > 30:
            return etat.drible_but + etat.go_ball
        else:
            return etat.vise_but
    else:
        return etat.go(t_droite.division_horizontale[1].milieu)

def test(etat):
    return etat.passe

def evite(etat):
    if etat.adv_proche_distance < 10:
        return etat.evite(etat.adv_but) + etat.go_ball
    else:
        return drible_but + etat.go_ball

