import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from projet import *
from PlayerDecorator import *
from decisiontree import *
import os
import pickle
from random import *

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
    etat_discret = (distance(etat.distance_ball),distance(etat.distance_but_adv),distance(etat.distance_my_but),distance(etat.adv_proche_distance),angle(etat.angle_adv_proche))
    #print("type etat discret",type(etat_discret))
    return etat_discret


def recompense(state,it,ip):
    #marque un but
    if (state.winning_team == it):
        return 100
    #si aucun but n'a ete marque
    if (state.winning_team == 0):
        return 0
    if(state.winning_team != it):
        return -100
    #possede la balle
    if (state.ball.position.distance(state.player_state(it,ip).position) < 10):
        return 1
    return -1

from collections import defaultdict

#retourne la meilleurs action locale
def best_act(dico,state,act):
    #Attention un dictionnaire NE PEUT PAS CONTENIR DES LISTE donc pb pour action essayer avec des tuples
    maxi = 0
    for action in act:
        if action not in dico[state]:
            dico[state][action] = random()*9 + 1
        if dico[state][action] > maxi:
            maxi = dico[state][action]
            best_act = action 
    return best_act

#Pour la strategie de l ia, on prend le chemin avec la meilleur esperance d action


def apprend_Monte_Carlo(dico, scenario, it, ip):
    gamma=1
    R=0
    alpha=0.5
    #print("apprend Monte Carlo",type(dico))
    #on parcours les etat en partant par les etats finales
    for (etat,action,state) in scenario[::-1]:
        R=gamma*R + recompense(state,it,ip)
        #si on n a pas encore croise cette situation, on initialise Q
        if etat not in dico:
            dico[etat] = defaultdict(float)
        #on actualise la recompense
        dico[etat][action]=dico[etat][action] + alpha*(R-dico[etat][action])


def Monte_Carlo(fEtat,fAction,it,ip):
    scenario = creation_scenario(fEtat,fAction,it,ip)
    dico = ouvre_dico()
    apprend_Monte_Carlo(dico,scenario,it, ip)
    enregistre_dico(dico)
    

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

#fonction qui prend un soccerMatch d'etat et un fichier action et les convertis en un scenario pour le Monte-Carlo
def creation_scenario(etats, action, it, ip):
    #un scenario est un tuple (etat_discret, action, SoccerState
    m = SoccerMatch.load(etats)
    f = open(action,"r")
    a = f.read()
    liste = a.split()
    f.close()
    i = 0
    scenario = []
    for etat_j in m.states:
        #pb nombre d'etat variable celon les match
        tuple = (transformation_etat(etat_j,it,ip), liste[i],etat_j)
        scenario.append(tuple)
        #print("i : ",i)
        i = i + 1
    return scenario

#---------------------------------------------------------------
#Fonctions relatives a l'utilisation de notre IA
#---------------------------------------------------------------

def enregistre_dico(dico):
    f = open('dico_apprentissage','w')
    pickle.dump(dico,f)
    f.close()

#fonction qui prend un dictionnaire stoquer dans un fichier et l'affecte a une variable
#pb pour ouvre_dico car on ferme la fonction avant le retour
def ouvre_dico():
    #si le fichier est vide on renvoi un dico vide
    if os.path.getsize("dico_apprentissage") == 0:
        dico = dict()
    else:
        f = open('dico_apprentissage','r')
        dico = pickle.load(f)
        f.close()
    return dico

def init_IA(IA):
    try:
        IA
    except NameError:
        IA = Monte_Carlo_Strat()
    
def joue_IA(teamIA, teamAdv,it, ip,):
    #si le fichier d'action n'est pas vide on apprend
    if os.path.getsize("action") != 0:
        a = open("action","a")
        for i in range(0,10):
            a.write("\n goal")
        a.close()
        Monte_Carlo("fichier","action",it,ip)
        #on supprime les anciennes actions
        a = open("action","w")
        a.close()
    match = SoccerMatch(teamIA, teamAdv)
    #on reinitisalise fichier
    a = open("fichier","w")
    a.close()
    match.play()
    match.save("fichier")
    #A la fin on enregistre le dico optenu

def affiche_joue_IA(teamIA, teamAdv,it, ip):
    #si le fichier d'action n'est pas vide on apprend
    if os.path.getsize("action") != 0:
        a = open("action","a")
        for i in range(0,10):
            a.write("\n goal")
        a.close()
        Monte_Carlo("fichier","action",it,ip)
        #on supprime les anciennes actions
        a = open("action","w")
        a.close()
    match = SoccerMatch(teamIA, teamAdv)
    a = open("fichier","w")
    a.close()
    match.play()
    soccersimulator.show(match)
    match.save("fichier")
    #A la fin on enregistre le dico optenu

#lance n fois un tournoi avec la liste des joueurs
def tournoi_IA(TeamIA, Liste,it,ip,n):
    for j in range(0,n+1):
        for i in Liste:
            joue_IA(TeamIA,i,it,ip)
    

def init_fichier(team1 ,team2):
    if os.path.getsize("fichier") == 0:
        match = SoccerMatch(team1,team2)
        match.save("fichier")



    
