from projet import *
from tools import *
from decisiontree import DTreeStrategy
from soccersimulator import SoccerMatch, show, SoccerTeam,Player,KeyboardStrategy
from decisiontree import gen_features
import cPickle


#### Arbres de decisions

tree = cPickle.load(file("./train.pkl"))
dic = {"goal":gardien,"fonceur":fonceStrat,"defenseur":defense,"attaquant":attaque}
treeStrat = DTreeStrategy(tree,dic,gen_features)
