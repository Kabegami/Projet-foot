import soccersimulator,soccersimulator.settings
from soccersimulator import AbstractStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings

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
            V = Vector2D(0,settings.GAME_HEIGHT/2.0)
        else:
            V = Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.0)

        if (state.ball.position.distance(state.player_state(teamid,player).position) < settings.PLAYER_RADIUS + settings.BALL_RADIUS):
            return SoccerAction(state.ball.position - state.player_state(teamid,player).position,V)
        else:
            return SoccerAction(state.ball.position - state.player_state(teamid,player).position,Vector2D(0,0))
                

team1 = SoccerTeam("team1",[Player("t1j1",FonceurStrategy())])
team2 = SoccerTeam("team2",[Player("t2j1",FonceurStrategy())])
match = SoccerMatch(team1, team2)
soccersimulator.show(match)
