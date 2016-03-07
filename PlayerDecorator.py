
import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from zone import *
from miroir import *

class PlayerDecorator(object):
    def __init__(self, state, idteam,player):
        self.state = state
        self.key = (idteam,player)
        self.adv_but = Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.0)
        self.my_but = Vector2D(0,settings.GAME_HEIGHT/2.0)
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
    def distance_but_adv(self):
        return self.my_position.distance(self.adv_but)

    @property
    def distance_my_but(self):
        return self.my_position.distance(self.my_but)
    
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
    def distance_adv_ball(self):
        return self.adv_proche.distance(self.ball_position)
    
    @property
    def equ_proche_distance(self):
        distance = 10000
        for i in self.equipe:
            if self.my_position.distance(i.position) < distance:
                distance = self.my_position.distance(i.position)
        return distance
        
    #fonction de deplacement
    def go(self,p):
        return SoccerAction(p - self.my_position, Vector2D(0,0))

    def vise(self, p):
        if (not(self.distance_adv_ball > self.distance_ball + 5) and  not(self.distance_ball > 5) and not(self.ball_position.x < self.my_position.x + 5)):
            V = (self.ball_position - p)*1.05
            return SoccerAction((p + V) - self.my_position, Vector2D(0,0))
        else:
            return SoccerAction(self.ball_position - self.my_position,p - self.my_position)

    @property
    def vise_but(self):
        return self.vise(self.adv_but)

    def drible(self, p):
        if self.can_shoot:
            if (self.adv_proche_distance < 10):
                return SoccerAction(Vector2D(0,0),(p - self.my_position))
            else:
                return SoccerAction(Vector2D(0,0), 0.025 * (p - self.my_position))
        else:
            return SoccerAction(Vector2D(0,0),Vector2D(0,0))

    @property
    def drible_but(self):
        return self.drible(self.adv_but)
    
    @property
    def go_ball(self):
        return self.go(self.ball_position)
                            
    #fonction de shoot
    def shoot(self,p):
        if self.can_shoot:
            return SoccerAction(Vector2D(0,0), p - self.my_position)
        else:
            return SoccerAction(Vector2D(0,0),Vector2D(0,0))

    def evite(self,p):
        if self.can_shoot:
            return SoccerAction(Vector2D(0,0),p - Vector2D(angle=20,norm=1))
        else:
            return SoccerAction(Vector2D(0,0),Vector2D(0,0))
            
        
    @property
    def shoot_but(self):
        return self.shoot(self.adv_but)

    @property
    def trouve_attaquant(self):
        distance = 10000
        for i in self.equipe:
            if (i.position).distance(self.adv_but) < distance:
                distance = (i.position).distance(self.adv_but)
                a = i.position
        return a

    @property
    def passe(self):
        distance = self.my_position.distance(self.trouve_attaquant)
        if distance > 30:
            return SoccerAction(self.ball_position - self.my_position, 0.025 *(self.equ_proche - self.my_position))
        else:
            if (not(self.distance_adv_ball > self.distance_ball + 5) and  not(self.distance_ball > 5) and not(self.ball_position.x < self.my_position.x + 5)):
                V = (self.ball_position - self.equ_proche)*1.05
                return SoccerAction((self.equ_proche + V) - self.my_position, Vector2D(0,0))
            else:
                return SoccerAction(self.ball_position - self.my_position, 0.2 *(self.equ_proche - self.my_position))
        

    def small_shoot(self,p):
        if self.can_shoot:
            return SoccerAction(Vector2D(0,0), 0.10 *(p - self.my_position))
        else:
            return SoccerAction(Vector2D(0,0),Vector2D(0,0))
        
    @property
    def small_shoot_but(self):
        return self.small_shoot(self.adv_but)
            
    
    #trigger

    @property
    def can_shoot(self):
        if (self.distance_ball < settings.PLAYER_RADIUS + settings.BALL_RADIUS):
            return True
        else:
            return False

    def degage(self,zone):
        if not(self.adv_dans_zone(zone.division_horizontale[0])):
            return self.shoot(zone.division_horizontale[0].milieu)
        else:
            if not(self.adv_dans_zone(zone.division_horizontale[1])):
                return self.shoot(zone.division_horizontale[1].milieu)
            else:
                return self.shoot_but

                
    #def degage2(self):
        #z = self.my_zone.division_verticale[1]
        #d = (z.division_horizontale[0]).distance(etat.adv_proche)
        #if z.division_horizontale[1].distance(etat.adv_proche) > d:
            #return self.shoot(z.division_horizontale[1].milieu)
       # return self.shoot(z.division_horizontale[0].milieu)
            
   # @property
    #def degagement(self,zone):
        #return self.tire(self.rechercher_zone_libre(zone).milieu)

    #constantes de zones
    @property
    def my_zone(self):
        return z[0]

    @property
    def my_but_zone(self):
        return self.my_zone.division_verticale[0]

    @property
    def adv_zone(self):
        return z[1]

    @property
    def adv_but_zone(self):
        return self.adv_zone.division_verticale[1]

    #fonction bas niveau
    def dans_zone(self,zone,position):
        return zone.vecteur_dans_zone(position)
        #return zone.est_dans(position)

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

    def balle_dans_zone(self,zone):
        return self.dans_zone(zone,self.ball_position)

    @property
    def ball_in_my_zone(self):
        return self.balle_dans_zone(self.my_zone)

    @property
    def adv_in_my_zone(self):
        return self.adv_dans_zone(self.my_zone)

    @property
    def equ_in_my_zone(self):
        return self.equ_dans_zone(self.my_zone)

#Gestion du terrain
    def zone_libre(self,liste_zone):
        for i in liste_zone:
            if (self.adv_dans_zone(i)):
                return i
        return zone(Vector2D(0,0),Vector2D(0,0))

    def rechercher_zone_libre(self,zone):
        L = []
        new = [zone]
        temp = []
        while self.zone_libre(L).bg == Vector2D(0,0) and elf.zone_libre(L).hd == Vector2D(0,0):
            for i in new:
                temp.append(i.division_horizontale)
                temp.append(j.division_verticale)
                L.append[i]
                new = []
                new = new + temp
                temp = []
        return self.zone_libre(L)
    
    @property
    def zone_joueur(self):
        return zone(self.my_position - Vector2D(10,10),self.my_position + Vector2D(10,10))
