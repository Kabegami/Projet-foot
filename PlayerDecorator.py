import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from tools import *

class PlayerDecorator(object):
    def __init__(self, state, idteam,player):
        self.state = state
        self.key = (idteam,player)
        self.but1 = Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.0)
        self.but2 = Vector2D(0,settings.GAME_HEIGHT/2.0)
        self.adv = []
        self.equipe = []
        #Crer une liste contenant ses adversaire et une autre pour sont equipe
        for (it, ip) in state.players:
            if (it != self.key[0]):
               (self.adv).append(state.player_state(it,ip))
            else:
                (self.equipe).append(state.player_state(it,ip))

    #gestion de l'espace
    def my_position(self):
        return self.state.player_state(self.key[0], self.key[1]).position

    def ball_position(self):
        return self.state.ball.position

    def distance_ball(self):
        return (self.my_position().distance(self.ball_position()))

    def adv_proche_distance(self):
        distance = 10000
        for i in self.adv:
            if self.my_position().distance(i.position) < distance:
                distance = self.my_position().distance(i.position)

    #fonction de deplacement
    def go(self,p):
        return SoccerAction(p - self.my_position(), Vector2D(0,0))

    def go_ball(self):
        return self.go(self.ball_position())
                            
    #fonction de shoot
    def shoot(self,p):
        if self.can_shoot():
            return SoccerAction(Vector2D(0,0), p - self.my_position())
        else:
            return SoccerAction(Vector2D(0,0),Vector2D(0,0))

    def shoot_but(self):
        if(self.key[0] == 1):
            return self.shoot(self.but1)
        else:
            return self.shoot(self.but2)

    #trigger

    def can_shoot(self):
        if (self.distance_ball() < settings.PLAYER_RADIUS + settings.BALL_RADIUS):
            return True
        else:
            return False
    
    
