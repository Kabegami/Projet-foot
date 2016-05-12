import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from PlayerDecorator import *
from zone import *
from tools import *
from ia import *

class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")
    def compute_strategy(self, state, teamid, player):
        return SoccerAction(Vector2D.create_random(low=-1.,high=1.), Vector2D.create_random(low=-1.,high=1.))

class FonceurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"FonceurStrategy")
    def compute_strategy(self, state, teamid,player):
        etat = PlayerDecorator(state, teamid, player)
        return fonceur(etat)
        
class MilieuStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"MilieuStrategy")
    def compute_strategy(self, state, teamid,player):
        etat = PlayerDecorator(state, teamid, player)
        return milieu(etat)
        
    
class StratStateless(BaseStrategy):
    def __init__(self,decideur):
        BaseStrategy.__init__(self,decideur.__name__)
        self.decideur = decideur
        self.log = []
    def compute_strategy(self,state,idt,idp):
        if(idt != 1):
            miroir = MiroirState(state)
            return MiroirSoccerAction(self.decideur(PlayerDecorator(miroir,idt,idp)))
        else:
            return self.decideur(PlayerDecorator(state,idt,idp))

class ExempleStrat(BaseStrategy):
    def __init__(self,decideur):
        BaseStrategy.__init__(self,decideur.__name__)
        self.decideur = decideur
    def compute_strategy(self,state,idt,idp):
        if(idt != 1):
            miroir = MiroirState(state)
            res =  MiroirSoccerAction(self.decideur(PlayerDecorator(miroir,idt,idp)))
            f = open("action","a")
            f.write(res.name)
            f.write("\n")
            f.close()
            return res
        else:
            res =  self.decideur(PlayerDecorator(state,idt,idp))
            f = open("action","a")
            f.write(res.name)
            f.write("\n")
            f.close()
            return res            

class GoalStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"GoalStrategy")
    def compute_strategy(self, state, teamid,player):
        etat = PlayerDecorator(state,teamid,player)
        return goal(etat)

class Monte_Carlo_Strat(BaseStrategy):
    def __init__(self):
       BaseStrategy.__init__(self,"Monte_Carlo")
       #on initialise L'IA avec le dictionnaire stoquer dans dico_apprentissage
       self.dico = ouvre_dico()
    def compute_strategy(self,state,teamid,player):
        if (teamid != 1):
            miroir = MiroirState(state)
            etat_discret = transformation_etat(miroir,teamid,player)
            etat = PlayerDecorator(miroir,teamid,player)
            #action = [fonce_Strat(etat), tire_hautStrat(etat), tire_basStrat(etat),viseStrat(etat),attend(etat),dribleStrat(etat), intercepteStrat(etat)]
            action = [fonce_Strat(etat),goal(etat),attaquant(etat),evite(etat)]
            
            #gestion de l'enregistrement des actions dans le fichier action
            if etat_discret not in self.dico:
                self.dico[etat_discret] = defaultdict(float)
            res =  best_act(self.dico,etat_discret,action)
            f = open("action","a")
            f.write(res.name)
            f.write("\n")
            f.close()
            return MiroirSoccerAction(res)
        else:
            etat_discret = transformation_etat(state,teamid,player)
            etat = PlayerDecorator(state,teamid,player)
            #action = [fonce_Strat(etat), tire_hautStrat(etat), tire_basStrat(etat),viseStrat(etat),dribleStrat(etat),goal(etat)]
            action = [fonce_Strat(etat),goal(etat),attaquant(etat),evite(etat)]
            #gestion de l'enregistrement des actions dans le fichier action
            if etat_discret not in self.dico:
                self.dico[etat_discret] = defaultdict(float)
            res =  best_act(self.dico,etat_discret,action)
            f = open("action","a")
            f.write(res.name)
            f.write("\n")
            f.close()
            return res
                

gardien = StratStateless(goal)
fonceStrat= StratStateless(fonceur)
attaque = StratStateless(attaquant)
defense = StratStateless(defenseur)
j_solo = StratStateless(solo)
toto = StratStateless(test)
dio = StratStateless(campe)
doge = StratStateless(evite)
test = StratStateless(attaquant2)
test2 = StratStateless(dribleStrat)
inter = StratStateless(intercepte)

joueur1 = Player("Joueur 1", fonceStrat)
joueur2 = Player("Joueur 2", gardien)
joueur4 = Player("Joueur 4", attaque)
joueur5 = Player("Joueur 5", defense)

#team1 = SoccerTeam("team1",[joueur1])
#team2 = SoccerTeam("team2",[joueur3])
#team1 = SoccerTeam("team1",[joueur1,joueur2,joueur3,joueur3])
#team2 = SoccerTeam("team2",[joueur1,joueur2,joueur3,joueur3])
#match = SoccerMatch(team1, team2)

#soccersimulator.show(match)

