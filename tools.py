import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
import math

def deplace_point(p1,p2):
    #prend 2 joueurs et retourne un Vector2D
    return  Vector2D(p2.x - p1.x, p2.y - p1.y)


def shoot_but(player,teamid,state):
    #Retourne un Vector2D correspondant au vecteur poitant sur les but
    if(teamid == 1):
        V = deplace_point(state.player_state(teamid,player).position,Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.0))
    else:
        V = deplace_point(state.player_state(teamid,player).position,Vector2D(0,settings.GAME_HEIGHT/2.0))
    return V


def trouver_adv(player,teamid,state):
    min = 10000
    pos = state.player_state(teamid,player).position
    for (it,ip) in state.players:
        if (it != teamid):
            if (pos.distance(state.player_state(it,ip)) < min):
                min = pos.distance(state.player_state(it,ip))
                p = state.player_state(it,ip)
    return p


def trouver_adv_distance(player,teamid,state):
    min = 10000
    pos = state.player_state(teamid,player).position
    for (it,ip) in state.players:
        if (it != teamid):
            if (pos.distance(state.player_state(it,ip)) < min):
                min = pos.distance(state.player_state(it,ip))
    return min


def peut_shoot(player,teamid,state):
    pos = state.player_state(teamid,player).position
    if (pos.distance(state.ball.position) < settings.PLAYER_RADIUS + settings.BALL_RADIUS):
        return True
    else:
        return False

    
def mes_but(player,teamid,state):
    if(teamid == 1):
        return Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.0)
    else:
       return Vector2D(0,settings.GAME_HEIGHT/2.0)
