import pickle
from bot import Bot
from bot import hiddennodes, onodes
import math
import sys
import random
import os

# this constant determines how likely it is that a mutation will occur
MUTATION_RANGE = 0.22

# INPUT: Int, Int, Int, [Int]
# OUTPUT: NULL
# Requires that ./bots/ has the bots labelled "P1BOTX.bot" or "P2BOTX.bot" and the ./botsNext is empty
# At the end, ./bots/ has the new bots and ./botsNext will be empty again
# This can only be called from the main folder, not the AI folder
def evolve(topx, totalBots, playerSide, results):
    
    # We index the results of the AIs so that when we sort by wins we can retain the
    # AI number that got those results
    indexedResults = []
    for index in range(len(results)):
        indexedResults.append([index, results[index]])

    # Sort the results by number of wins that each bot got
    resultsSorted = sorted(indexedResults, key=getWins, reverse=True)
    
    # Get an array of the topx bots to produce new bots
    goodBots = []
    for i in range(topx):
        with open ("./AI/bots/P" + str(playerSide) + "BOT" + str(resultsSorted[i][0]) + ".bot", 'rb') as fp:
            wih1 = pickle.load(fp)
            who1 = pickle.load(fp)
            goodBots.append(Bot(wih1, who1))

    # Now we generate new descendants, start by grabbing 2 of the good bots at random
    botsToGenerate = totalBots - topx
    for _ in range(botsToGenerate):
        candidates = range(0, topx)
        randomIndex = random.sample(candidates, 2)
        org1 = goodBots[randomIndex[0]]
        org2 = goodBots[randomIndex[1]]

        # Crossover
        crossoverWeight = random.uniform(0,1)
        wihNew = (crossoverWeight * org1.wih) + ((1 - crossoverWeight) * org2.wih)
        whoNew = (crossoverWeight * org1.who) + ((1 - crossoverWeight) * org2.who)

        # Mutation
        mutate = random.uniform(0,1)
        if mutate <= MUTATION_RANGE:
            # PICK WHICH WEIGHT MATRIX TO MUTATE
            mutPick = random.randint(0,1)     

            # MUTATE: WIH WEIGHTS
            if mutPick == 0:
                indexRow = random.randint(0,hiddennodes-1)
                indexCol = random.randint(0,36)
                wihNew[indexRow][indexCol] = wihNew[indexRow][indexCol] * random.uniform(-1.25, 1.25)
                if wihNew[indexRow][indexCol] >  1: wihNew[indexRow][indexCol] = 1
                if wihNew[indexRow][indexCol] < -1: wihNew[indexRow][indexCol] = -1
                
            # MUTATE: WHO WEIGHTS
            if mutPick == 1:
                indexRow = random.randint(0,onodes-1)
                indexCol = random.randint(0,hiddennodes-1)
                whoNew[indexRow][indexCol] = whoNew[indexRow][indexCol] * random.uniform(-1.25, 1.25)
                if whoNew[indexRow][indexCol] >  1: whoNew[indexRow][indexCol] = 1
                if whoNew[indexRow][indexCol] < -1: whoNew[indexRow][indexCol] = -1
    
        # Add to list of new generation
        goodBots.append(Bot(wihNew, whoNew))

    # put all new generation into "./botsNext/"
    # right now, it just replaces the file
    for num in range(totalBots):
        os.remove("./AI/bots/P" + str(playerSide) + "BOT" + str(num) + ".bot")
        with open("./AI/bots/P" + str(playerSide) + "BOT" + str(num) + ".bot", 'wb') as fp:
            pickle.dump(goodBots[num].wih, fp)
            pickle.dump(goodBots[num].who, fp)

# This is just a helper function to use as a sorting key with evolve
def getWins(item):
    return item[1]

