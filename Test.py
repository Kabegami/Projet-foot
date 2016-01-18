import soccersimulator,soccersimulator.settings
from soccersimulator import AbstractStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament

class RandomStrategy(AbstractStrategy):
    def __init__(self):
        AbstractStrategy.__init__(self, "Random")
    def compute_strategy(self, state, teamid, player):
        return SoccerAction(Vector2D.create_random(low=-1.,high=1.), Vector2D.create_random(low=-1.,high=1.))

class FonceurStrategy(AbstractStrategy):
    def __init__(self):
        AbstractStrategy.__init__(self,"Fonceur")
    def compute_strategy(self,state,teamid,player):
        if(teamid == 1):
            V = Vector2D(0,45)
        else:
            V = Vector2D(150,45)
        return SoccerAction(state.ball.position - state.player_state(teamid,player).position,V)

team1 = SoccerTeam("team1",[Player("t1j1",FonceurStrategy())])
team2 = SoccerTeam("team2",[Player("t2j1",FonceurStrategy())])
match = SoccerMatch(team1, team2)
soccersimulator.show(match)
