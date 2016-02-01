import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from zone import *

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
                if(ip != self.key[1]):
                   (self.equipe).append(state.player_state(it,ip))

    #gestion de l'espace
    @property
    def my_position(self):
        return self.state.player_state(self.key[0], self.key[1]).position
    
    @property
    def ball_position(self):
        return self.state.ball.position
    
    @property
    def distance_ball(self):
        return (self.my_position.distance(self.ball_position))
    
    @property
    def adv_proche(self):
        distance = 10000
        for i in self.adv:
            if self.my_position.distance(i.position) < distance:
                distance = self.my_position.distance(i.position)
                a = i.position
        return a

    @property
    def equ_proche(self):
        distance = 10000
        for i in self.equipe:
            if self.my_position.distance(i.position) < distance:
                distance = self.my_position.distance(i.position)
                a = i.position
        return a
                   
    #gestion des distances
    @property
    def adv_proche_distance(self):
        distance = 10000
        for i in self.adv:
            if self.my_position.distance(i.position) < distance:
                distance = self.my_position.distance(i.position)
        return distance

    @property
    def equ_proche_distance(self):
        distance = 10000
        for i in self.equipe:
            if self.my_position.distance(i.position) < distance:
                distance = self.my_position.distance(i.position)
        return distance

    @property
    def my_but(self):
        if(self.key[0] == 1):
            return(self.but2)
        else:
            return(self.but1)

    @property
    def adv_but(self):
        if(self.key[0] == 1):
            return(self.but1)
        else:
            return(self.but2)
        
    #fonction de deplacement
    def go(self,p):
        return SoccerAction(p - self.my_position, Vector2D(0,0))
    
    @property
    def go_ball(self):
        return self.go(self.ball_position)
                            
    #fonction de shoot
    def shoot(self,p):
        if self.can_shoot:
            return SoccerAction(Vector2D(0,0), p - self.my_position)
        else:
            return SoccerAction(Vector2D(0,0),Vector2D(0,0))

    @property
    def shoot_but(self):
        return SoccerAction(Vector2D(0,0),self.adv_but - self.my_position)

    #trigger

    @property
    def can_shoot(self):
        if (self.distance_ball < settings.PLAYER_RADIUS + settings.BALL_RADIUS):
            return True
        else:
            return False

    #constantes de zones
    @property
    def my_zone(self):
        if (self.key[0] == 1):
            return zone(Vector2D(0,0),Vector2D(settings.GAME_WIDTH/2,settings.GAME_HEIGHT))
        else:
            return zone(Vector2D(settings.GAME_WIDTH/2,0),Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT))

    @property
    def adv_zone(self):
        if (self.key[0] != 1):
            return zone(Vector2D(0,0),Vector2D(settings.GAME_WIDTH/2,settings.GAME_HEIGHT))
        else:
            return zone(Vector2D(settings.GAME_WIDTH/2,0),Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT))

    
    #fonction bas niveau
    def dans_zone(self,zone,position):
        return est_dans(zone,position)

    #fonction moyen_niveau

    def j_dans_zone(self,zone):
        return self.dans_zone(zone,self.my_position)

    def adv_dans_zone(self,zone):
        for i in self.adv:
            if self.dans_zone(zone,i.position):
                return True
            return False
            
    def equ_dans_zone(self,zone):
        for i in self.equipe:
            if self.dans_zone(zone,i.position):
                return True
            return False

    @property
    def adv_in_my_zone(self):
        return self.adv_dans_zone(self.my_zone)

    @property
    def equ_in_my_zone(self):
        return self.equ_dans_zone(self.my_zone)
    

    
