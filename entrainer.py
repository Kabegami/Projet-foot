""" Permet de jouer et d'entrainer une strategie
    * changer les strategies ajoutees
    * utilisation : python entrainer prefix_fichier_exemple
    par defaut ajoute au fichier d'exemples sil existe deja
    (extension : .exp pour le fichier exemple)
"""

from soccersimulator import SoccerMatch, show, SoccerTeam,Player,KeyboardStrategy
from projet import *
import sys

if __name__=="__main__":
    prefix = "train"
    if len(sys.argv)>1:
        prefix = sys.argv[1]
    strat_key = KeyboardStrategy()
    strat_key.add("f",fonceStrat)
    strat_key.add("g",gardien)
    strat_key.add("a",attaque)
    strat_key.add("d",defense)
    team_noob = SoccerTeam("keyb",[Player("KBs", strat_key),Player("goal", gardien)])
    team_bad = SoccerTeam("foncteam",[Player("toto",j_solo),Player("def",defense)])
    match = SoccerMatch(team_noob,team_bad,1000)
    show(match)
    strat_key.write(prefix+".exp",True)
