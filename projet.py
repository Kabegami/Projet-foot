import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from tools import *

class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")
    def compute_strategy(self, state, teamid, player):
        return SoccerAction(Vector2D.create_random(low=-1.,high=1.), Vector2D.create_random(low=-1.,high=1.))

class FonceurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Fonceur2")
    def compute_strategy(self,state,teamid,player):
        pos = state.player_state(teamid,player).position
        if (peut_shoot(player,teamid,state)):
            return SoccerAction(deplace_point(pos,state.ball.position),shoot_but(player,teamid,state))
        else:
            return SoccerAction(deplace_point(pos,state.ball.position),Vector2D(0,0))

class DefenseurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Defenseur")
    def compute_setrategy(self,state,teamid,player):
        pos = state.player_state(teamid,player).position
        if(trouver_adv_distance(player,teamid,state) < 50):
            if (peut_shoot(player,teamid,state)):
                return SoccerAction(deplace_point(pos,state.ball.position),shoot_but(player,teamid,state))
            else:
                return SoccerAction(deplace_point(pos,state.ball.position),Vector2D(0,0))
        else:
            return SoccerAction(deplace_point(pos,mes_but(player,teamid,state)),Vector2D(0,0))

            

joueur1 = Player("Joueur 1", FonceurStrategy())
joueur2 = Player("Joueur 2", DefenseurStrategy())
team1 = SoccerTeam("team1",[joueur1,joueur2])
team2 = SoccerTeam("team2",[joueur1,joueur2])
match = SoccerMatch(team1, team2)
soccersimulator.show(match)
