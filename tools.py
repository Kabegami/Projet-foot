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

def attaquant(etat):
    if etat.j_dans_zone(etat.adv_but_zone):
        return fonceur(etat)
    else:
        if etat.j_dans_zone(etat.adv_zone):
            if etat.j_dans_zone(etat.adv_zone.division_horizontale[0]):
                return etat.go_ball + etat.small_shoot(etat.adv_zone.division_horizontale[0].milieu)
            else:
                return etat.go_ball + etat.small_shoot(etat.adv_zone.division_horizontale[1].milieu)
        else:
            return fonceur(etat)

def defenseur(etat):
    if etat.distance_ball < etat.adv_proche_distance or not(etat.balle_dans_zone(etat.my_but_zone)):
        return fonceur(etat)
    if etat.balle_dans_zone(etat.my_zone.division_horizontale[0]):
        return etat.go(etat.my_zone.division_horizontale[1].division_verticale[1].milieu) + etat.shoot_but
    if etat.balle_dans_zone(etat.my_zone.division_horizontale[1]):
        return etat.go(etat.my_zone.division_horizontale[0].division_verticale[0].milieu) + etat.shoot_but
    else:
        return fonceur(etat)

def solo(etat):
    if etat.balle_dans_zone(etat.my_but_zone):
        return goal(etat)
    else:
        return fonceur(etat)

def test(etat):
    return etat.go_ball + etat.passe
