import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings

class zone(object):
    def __init__(self,bg,hd):
        self.bg = bg
        self.hd = hd

def est_dans(self,pos):
    if (pos.x < self.bg.x or pos.x > self.hd.x):
        return False
    if (pos.y < self.bg.y or pos.y > self.hd.y):
        return False
    return True

def milieu(self):
    return Vector2D(self.bg.x + self.hd.x / 2, self.bg.y + self.hd.y / 2)

