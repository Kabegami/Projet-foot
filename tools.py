import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from zone import *
from PlayerDecorator import *
import sys

def fonceur(etat):
    return etat.shoot_but + etat.go_ball

def goal(etat):
    if (etat.distance_ball) < 20:
        res =  etat.go_ball + etat.degage(etat.my_zone)
        res.name = "goal"
        return res
    else:
        res =  etat.go(etat.my_but) + SoccerAction(Vector2D(5,0),Vector2D(0,0)) + etat.shoot_but
        res.name = "goal"
        return res

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
        res = etat.vise_but
        res.name = "attaquant"
        return res
    else:
        res =  etat.go_ball + etat.drible_but
        res.name = "attaquant"
        return res

def campe(etat):
    if etat.distance_ball < 20:
        if etat.my_position.distance(etat.adv_but) > 30:
            return etat.drible_but + etat.go_ball
        else:
            return etat.vise_but
    else:
        return etat.go(t_droite.division_horizontale[1].milieu)

def test(etat):
    if etat.equ_proche_distance > 5:
        return etat.drible(etat.equ_proche) + etat.go_ball
    else:
        return etat.passe2

def evite(etat):
    if etat.adv_proche_distance < 10:
        res = etat.evite(etat.adv_but) + etat.go_ball
        res.name = "evite"
        return res
    else:
        if (etat.distance_but_adv < 30):
            res = etat.vise(etat.adv_but)
            res.name = "evite"
            return res
        else:
            res =  etat.drible_but + etat.go_ball
            res.name = "evite"
            return res

def attaquant2(etat):
    a = sys.stdout
    sys.stdout=open('action','a')
    if etat.dans_zone(etat.adv_but_zone,etat.my_position):
        res = etat.vise_but
        res.name = "visebut"
        print("attaquant")
        sys.stdout.close()
        sys.stdout=a
        return res
    else:
        res =  etat.go_ball + etat.drible_but
        res.name = "driblebut"
        print("attaquant")
        sys.stdout.close()
        sys.stdout=a
        return res

def intercepte(etat):
    if not(etat.distance_ball  < etat.distance_ball_adv):
        return etat.intercepte_adv_proche
    else:
        return fonceur(etat)

#-------------------------------------------------------
#Strat IA
#-------------------------------------------------------

def fonce_Strat(etat):
    res = etat.shoot_but + etat.go_ball
    res.name = "fonce_Strat"
    return res
    
def tire_hautStrat(etat):
    V = Vector2D(angle = 45, norm = 2)
    if not((etat.ball_position - etat.my_position).angle > 42 and (etat.ball_position - etat.my_position).angle < 48):
        res =  etat.go(etat.ball_position - 0.1 *V)
    else:
        res =  SoccerAction(etat.ball_position - etat.my_position,Vector2D(angle=45, norm=2))
    res.name = "tire_hautStrat"
    return res

def tire_basStrat(etat):
    V = Vector2D(angle = -45, norm = 2)
    if not((etat.ball_position - etat.my_position).angle < -42 and (etat.ball_position - etat.my_position).angle > -48):
        res =  etat.go(etat.ball_position - 0.1 *V)
    else:
        res =  SoccerAction(etat.ball_position - etat.my_position,Vector2D(angle=-45, norm=2))
    res.name = "tire_basStrat"
    return res

def viseStrat(etat):
    res =  etat.vise_but
    res.name = "viseStrat"
    return res

def passeStrat(etat):
    res =  etat.vise(etat.equ_proche)
    res.name = "passeStrat"
    return res

def attend(etat):
    res = SoccerAction(Vector2D(0,0),Vector2D(0,0))
    res.name = "attend"
    return res

def dribleStrat(etat):
    V = (etat.ball_position - etat.adv_but)*1.05
    if not(etat.dans_zone(zone(etat.adv_but + V - Vector2D(5,5), etat.adv_but + V + Vector2D(5,5)),etat.my_position)):
        res =  SoccerAction((etat.adv_but + V) - etat.my_position, Vector2D(0,0))
    else:
        res = SoccerAction(etat.ball_position - etat.my_position,0.030*(etat.adv_but - etat.my_position))
    res.name = "dribleStrat"
    return res

def intercepteStrat(etat):
    V = etat.adv_proche - etat.my_but
    res = etat.go(etat.adv_proche + 0.5*V)
    res.name = "intercepteStrat"
    return res
