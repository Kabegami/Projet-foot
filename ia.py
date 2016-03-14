import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from projet import *
from PlayerDecorator import *

def distance(distance):
    # tres proche
    if (distance < 10):
        return 0
    if (distance < 30):
        return 1
    if (distance < 50):
        return 2
    return 3

def angle(angle):
    angle = angle % 360
    angle = int(angle/45.)
    #devant
    if (angle < 1 or angle > 5):
        return 0
    #derriere
    else:
        return 1

def recompense(etat):
    #marque un but
    if (etat.state.winning_team == etat.id_team):
        return 100
    if (etat.state.winning_team != 0):
        return -100
    #possede la balle
    if (etat.ball_position.distance(etat.my_position) < 10):
        return 1
    return -1

etat = PlayerDecorator(state,idteam,player)

Liste = [distance(etat.distance_ball),distance(etat.distance_but_adv),distance(etat.distance_my_but),distance(etat.adv_proche_distance),angle(etat.angle_adv_proche)]

action = [gardien,doge,fonceur]

from collections import defaultdict

#retourne la meilleurs action locale
def best_act(dico,state):
    max = -101
    for action in dico[state]:
        if dico[state][action] > max:
            max = dico[state][action]
            best_act = action 
    return best_act

#Pour la strategie de l ia, on prend le chemin avec la meilleur esperance d action

def apprend_Monte_Carlo(dico):
    gamma = 0.10
    r_suivant = 0
    max = -101
    #on parcours tous les etats afin d avoir la recompense totale
    for etat in (dico,-1):
        r = gamma*dico[etat][best_act(dico,etat)] + r_suivant
        r_suivant = r


def Q(state,action,R):
    #pour Q il faut faire un calcule lineaire demander au prof
    Q = -R

if s not in dic :
    dic[s] = defaultdict(float)
dic[s][a] = 2.3
