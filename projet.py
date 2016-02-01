import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from PlayerDecorator import *
from zone import *

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
        return etat.go_ball + etat.shoot_but
        
class GardienStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"GardienStrategy")
    def compute_strategy(self, state, teamid,player):
        etat = PlayerDecorator(state,teamid,player)
        if ((etat.my_position).distance(etat.my_but) > 50):
            return etat.go(etat.my_but)
        else:
            if (etat.my_position.distance(etat.ball_position) < 30):
                return etat.go_ball + etat.shoot_but
            else:
                return etat.go(etat.my_but)

class PasseurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"PasseurStrategy")
    def compute_strategy(self, state, teamid,player):
        etat = PlayerDecorator(state,teamid,player)
        if (etat.adv_proche_distance < 30):
            return etat.go_ball + etat.shoot(etat.equ_proche)
        else:
            return etat.go_ball + etat.shoot_but

class StratStateless(BaseStrategy):
    def __init__(self,decideur):
        BaseStrategy.__init__(self,decideur.__name__)
        self.decideur = decideur
    def compute_strategy(self,state,idt,idp):
        return  self.decideur(PlayerDecorator(state,idt,idp)) 


class DefenseurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"DefenseurStrategy")
    def compute_strategy(self, state, teamid,player):
         etat = PlayerDecorator(state,teamid,player)
         return defenseur(etat)
         
def defenseur(etat):
    if etat.adv_in_my_zone:
        if (etat.adv_proche_distance < 30):
            return etat.go_ball + etat.shoot(etat.equ_proche)
        else:
            return etat.go(etat.my_but)
    if etat.can_shoot:
        return etat.go_ball + etat.shoot_but
    return etat.go(milieu(etat.my_zone))

Defens = StratStateless(defenseur)

joueur1 = Player("Joueur 1", FonceurStrategy())
joueur2 = Player("Joueur 2", GardienStrategy())
joueur3 = Player("Joueur 3", PasseurStrategy())
joueur4 = Player("Joueur 4", DefenseurStrategy())

#team1 = SoccerTeam("team1",[joueur3,joueur2])
#team2 = SoccerTeam("team2",[joueur4,joueur2])
team1 = SoccerTeam("team1",[joueur1,joueur2,joueur3,joueur3])
team2 = SoccerTeam("team2",[joueur1,joueur2,joueur3,joueur3])
match = SoccerMatch(team1, team2)
#soccersimulator.show(match)
