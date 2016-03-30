import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from projet import *
from PlayerDecorator import *
from decisiontree import *

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

def transformation_etat(state, idteam,player):
    etat = PlayerDecorator(state,idteam,player)
    etat_discret = [distance(etat.distance_ball),distance(etat.distance_but_adv),distance(etat.distance_my_but),distance(etat.adv_proche_distance),angle(etat.angle_adv_proche)]
    return etat_discret


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

from collections import defaultdict

#retourne la meilleurs action locale
def best_act(dico,state,act):
    maxi = 0
    for action in act:
        if dico[state][action] > maxi:
            maxi = dico[state][action]
            best_act = action 
    return best_act

#Pour la strategie de l ia, on prend le chemin avec la meilleur esperance d action


def apprend_Monte_Carlo(dico, scenario):
    gamma=1
    R=0
    alpha=0.1
    #on parcours les etat en partant par les etats finales
    for (etat,action) in scenario[::-1]:
        R=gamma*R + recompense(etat)
        #si on n a pas encore croise cette situation, on initialise Q
        if etat not in dico:
            dico[etat] = defaultdict(float)
        #on actualise la recompense
        dico[etat][action]=dico[etat][action] + alpha*(R-dico[etat][action])


def Monte_Carlo(fichier):
    m = SoccerMatch.load(fichier)
    # Liste d etat du match
    L_etat = m.states
    apprend_Monte_Carlo(joueurIA.dico,L_etat)
    

class LogStrategy(KeyboardStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,name)
        self.dic_keys=dict()
        self.cur = None
        self.states=[]

    def compute_strategy(self,state,id_team,id_player):
        self.states.append((state,(teamid,player,self.name)))
        return self.dic_keys[self.cur].compute_strategy(state,id_team,id_player)
    def listen(self,key,teamid,player):
        if key in self.dic_keys.key():
            self.cur=key
            self.name = self.dic_keys[self.cur].name
    
        
