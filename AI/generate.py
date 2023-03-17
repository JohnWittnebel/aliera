# This is to generate the initial bots for our EA algorithm
import numpy as np
import pickle

BOTS_TO_GEN = 50
NUM_HIDDEN = 10
NUM_OUTPUT = 6
NUM_INPUT = 37

for num in range(BOTS_TO_GEN):
    with open("bots/P1BOT" + str(num) + ".bot", 'wb') as fp:
        pickle.dump(np.random.uniform(-1,1,(NUM_HIDDEN,NUM_INPUT)), fp)
        pickle.dump(np.random.uniform(-1,1,(NUM_OUTPUT,NUM_HIDDEN)), fp)
    with open("bots/P2BOT" + str(num) + ".bot", 'wb') as fp:
        pickle.dump(np.random.uniform(-1,1,(NUM_HIDDEN,NUM_INPUT)), fp)
        pickle.dump(np.random.uniform(-1,1,(NUM_OUTPUT,NUM_HIDDEN)), fp)

#z = Bot(test1, test2)
#test3 = np.random.uniform(-1,1,(10,37))
#test4 = np.random.uniform(-1,1,(6,10))
#z2 = Bot(test1, test2)
