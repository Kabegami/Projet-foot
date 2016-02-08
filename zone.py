import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings

class zone(object):
    def __init__(self,bg,hd):
        self.bg = bg
        self.hd = hd
        self.n_bg = Vector2D(-1,-1)
        self.n_hd = Vector2D(1,1)

    def normalisation(self,Vecteur):
        Vecteur.x = (Vecteur.x * 2 / self.hd.x - self.bg.x) - 1
        Vecteur.y = (Vecteur.y * 2 / self.hd.y - self.bg.y) - 1
        return Vecteur
    
    def denormalisation(self, Vecteur):
        Vecteur.x = (Vecteur.x + 1)* (self.hd.x - self.bg.x) / 2
        Vecteur.y = (Vecteur.y + 1)* (self.hd.y - self.bg.y) / 2
        return Vecteur
    
    def est_dans(self,pos):
        if (pos.x < self.bg.x or pos.x > self.hd.x):
            return False
        if (pos.y < self.bg.y or pos.y > self.hd.y):
            return False
        return True

    def mirroir(self,Vecteur):
        V = self.normalisation(Vecteur)
        V.x = -(V.x)
        V = self.denormalisation(Vecteur)
        return V

    

terrain = zone(Vector2D(0,0),Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT))
