from soccersimulator import *
from tools import *
from PlayerDecorator import *
from zone import *
from miroir import *

class PADState(SoccerState):
    """ Etat d'un tour du jeu. Contient la balle (MobileMixin), l'ensemble des configurations des joueurs, le score et
    le numero de l'etat.
    """
    def __init__(self, **kwargs):
        SoccerState.__init__(self,**kwargs)
        self.cur_score = 0

    def apply_actions(self, actions=None):
        sum_of_shoots = Vector2D()
        if actions:
            for k, c in self._configs.items():
                if k in actions:
                    act = actions[k].copy()
                    if k[0] == 1 and self.player_state(k[0],k[1]).vitesse.norm>0.01:
                        act.shoot = Vector2D()
                    sum_of_shoots += c.next(self.ball, act)
        self.ball.next(sum_of_shoots)
        self.step += 1
        dball = [(it,ip) for it,ip in self.players
                 if self.player_state(it,ip).position.distance(self.ball.position)<settings.BALL_RADIUS+settings.PLAYER_RADIUS]
        mines = [(it,ip) for it,ip in dball if it ==1 ]
        others = [(it,ip) for it,ip in dball if it==2 ]
        if len(others)==0 or len(mines)>0 or self.ball.vitesse.norm>1:
            self.cur_score += 1
        else:
            self._score[1]=max(self._score[1],self.cur_score)
            self.cur_score=0
            self._score[2]+=1
            self._winning_team = 2
        if self.ball.position.x < 0:
            self.ball.position.x = -self.ball.position.x
            self.ball.vitesse.x = -self.ball.vitesse.x
        if self.ball.position.y < 0:
            self.ball.position.y = -self.ball.position.y
            self.ball.vitesse.y = -self.ball.vitesse.y
        if self.ball.position.x > settings.GAME_WIDTH:
            self.ball.position.x = 2 * settings.GAME_WIDTH - self.ball.position.x
            self.ball.vitesse.x = -self.ball.vitesse.x
        if self.ball.position.y > settings.GAME_HEIGHT:
            self.ball.position.y = 2 * settings.GAME_HEIGHT - self.ball.position.y
            self.ball.vitesse.y = -self.ball.vitesse.y

    def reset_state(self, nb_players_1=0, nb_players_2=0):
        SoccerState.reset_state(self,nb_players_1,nb_players_2)
        self.ball = Ball.from_position(self.player(1,0).position.x,self.player(1,0).position.y)
        self.cur_score = 0




def immobile(etat):
    return SoccerAction(Vector2D(0,0),Vector2D(0,0))  

def passe(etat):
    if etat.adv_proche_distance < 20:
        return etat.shoot(etat.equ_proche)
    else:
        return immobile(etat)
    
def recepteur(etat):
    if etat.porteur_equipe == etat.key[0]:
        porteur = etat.trouve_porteur
        if (etat.my_position.distance(porteur) > 60):
            adv = etat.adv_proche
            V = (porteur - etat.my_position)
            return etat.go(0.5*V)
        else:
            return immobile(etat)
    else:
        if etat.porteur_equipe == -1:
            if etat.distance_ball < etat.equ_proche.distance(etat.state.ball.position):
                return fonceur(etat)
            else:
                return immobile(etat)
        else:
            return fonceur(etat)

def recepteur2(etat):
    if etat.porteur_equipe == etat.key[0]:
        porteur = etat.trouve_porteur
        if (etat.my_position.distance(porteur) < 60):
            V = (porteur - etat.my_position)
            return etat.go(-3*V)
        else:
            return immobile(etat)
    else:
        if etat.porteur_equipe == -1:
            if etat.distance_ball < etat.equ_proche.distance(etat.state.ball.position):
                return fonceur(etat)
            else:
                return immobile(etat)
        else:
            return fonceur(etat) 

def intercepte(etat):
    Vecteur = etat.trouve_porteur - etat.adv_proche
    return etat.milieu_seg(Vecteur)
    

#Strategies completes
def passeStrat(etat):
    if etat.trouve_porteur == etat.my_position:
        return passe(etat)
    else:
        return recepteur(etat)

class StratStateless(BaseStrategy):
    def __init__(self,decideur):
        BaseStrategy.__init__(self,decideur.__name__)
        self.decideur = decideur
        self.log = []
    def compute_strategy(self,state,idt,idp):
        if(idt != 1):
            miroir = MiroirState(state)
            #return self.decideur(PlayerDecorator(miroir,idt,idp))
            return MiroirSoccerAction(self.decideur(PlayerDecorator(miroir,idt,idp)))
        else:
            return self.decideur(PlayerDecorator(state,idt,idp))


#team evite
passeur = StratStateless(passeStrat)
fonce = StratStateless(fonceur)

j1 = Player("Passeur",passeur)
j2 = Player("Fonceur",fonce)


team2 = SoccerTeam("team 1",[j1,j1])
team1 = SoccerTeam("team 2",[j1])
team3 = SoccerTeam("team 3",[j1,j1,j1])
team4 = SoccerTeam("team 4",[j1,j1,j1,j1])

#match = SoccerMatch(team4,team3,init_state=PADState.create_initial_state(4,3))
#show(match)


