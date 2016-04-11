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
    maxi = -10000
    best_act = act[0]
    for action in act:
        #print("action :",action)
        if action.name not in dico[state]:
            dico[state][action.name] = random()*9 + 1
        if dico[state][action.name] > maxi:
            maxi = dico[state][action.name]
            best_act = action
    return best_act

#Pour la strategie de l ia, on prend le chemin avec la meilleur esperance d action


def apprend_Monte_Carlo(dico, scenario, it, ip):
    gamma=1
    R=0
    alpha=0.2
    #on parcours les etat en partant par les etats finaux
    for (etat,action,state) in scenario[::-1]:
        R=gamma*R + recompense(state,it,ip)
        #si on n a pas encore croise cette situation, on initialise Q
        if etat not in dico:
            dico[etat] = defaultdict(float)
        #on actualise la recompense
        dico[etat][action]=dico[etat][action] + alpha*(R-dico[etat][action])


def Monte_Carlo(fEtat,fAction,it,ip,dico):
    #print("dico avant monte Carlo",dico)
    scenario = creation_scenario(fEtat,fAction,it,ip)
    apprend_Monte_Carlo(dico,scenario,it, ip)
    #print(dico)

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
        if (i < len(liste)):
            tuple = (transformation_etat(etat_j,it,ip), liste[i],etat_j)
            scenario.append(tuple)
            i = i + 1
    #print("scenario : \n",scenario)
    return scenario

#---------------------------------------------------------------
#Fonctions relatives a l'utilisation de notre IA
#---------------------------------------------------------------

def enregistre_dico(dico):
    f = open('dico_apprentissage_exemple','w')
    pickle.dump(dico,f)
    f.close()

#fonction qui prend un dictionnaire stoquer dans un fichier et l'affecte a une variable
#pb pour ouvre_dico car on ferme la fonction avant le retour
def ouvre_dico():
    #si le fichier est vide on renvoi un dico vide
    if os.path.getsize("dico_apprentissage_exemple") == 0:
        dico = dict()
    else:
        f = open('dico_apprentissage_exemple','r')
        dico = pickle.load(f)
        f.close()
    return dico

def init_IA(IA):
    try:
        IA
    except NameError:
        IA = Monte_Carlo_Strat()    
    
def joue_IA(IA,teamIA, teamAdv,it, ip,):
    #si le fichier d'action n'est pas vide on apprend
    if os.path.getsize("action") != 0:
        Monte_Carlo("Match","action",it,ip,IA.dico)
        #on supprime les anciennes actions
        a = open("action","w")
        a.close()
    match = SoccerMatch(teamIA, teamAdv)
    #on reinitisalise fichier
    a = open("Match","w")
    a.close()
    match.play()
    match.save("Match")
    #A la fin on enregistre le dico optenu

def affiche_joue_IA(IA,teamIA, teamAdv,it, ip):
    #si le fichier d'action n'est pas vide on apprend
    if os.path.getsize("action") != 0:
        Monte_Carlo("Match","action",it,ip,IA.dico)
        #on supprime les anciennes actions
        a = open("action","w")
        a.close()
    match = SoccerMatch(teamIA, teamAdv)
    a = open("Match","w")
    a.close()
    match.play()
    soccersimulator.show(match)
    match.save("Match")
    #A la fin on enregistre le dico optenu

#lance n fois un tournoi avec la liste des joueurs
def tournoi_IA(IA,TeamIA, Liste,it,ip,n,affiche):
    for j in range(0,n+1):
        for i in Liste:
            if not(affiche):
                joue_IA(IA,TeamIA,i,it,ip)
            else:
                affiche_joue_IA(IA,TeamIA,i,it,ip)
    

def init_fichier(team1 ,team2):
    if os.path.getsize("Match") == 0:
        match = SoccerMatch(team1,team2)
        match.save("Match")

#Fonction pour enseigner a l'IA avec des exemples
#--------------------------------------------------
        
def exempleIA(IA,team1, team2, it, ip):
    match = SoccerMatch(team1,team2)
    #on reinitisalise fichier
    a = open("Match","w")
    a.close()
    match.play()
    match.save("Match")
    Monte_Carlo("Match","action",it,ip,IA.dico)
    a = open("action","w")
    a.close()

#Fait jouer tous les jouerus de la liste1 contre les joueurs de la liste2
def exemple_tournoi(IA,L1,L2,it,ip,n):
    for i in range(0,n+1):
        for j in L1:
            for k in L2:
                exempleIA(IA,j,k,it,ip)

    
