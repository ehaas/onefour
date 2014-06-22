import random
from strategy import Strategies
from collections import Counter

class IllegalPlay(Exception):
    pass

def rolldice(count):
    return [random.randint(1, 6) for x in xrange(0, count)]

def validate(roll, play):
    if not play:
        return False

    rollcount = Counter(roll)
    playcount = Counter(play)
    for value, numplayed in playcount.iteritems():
        if rollcount[value] < numplayed:
            return False
    return True

def playgame(strategy, ndice=6):
    history = []
    while ndice > 0:
        roll = rolldice(ndice)
        play = strategy.handle_roll(roll, history)
        if validate(roll, play):
            history.extend(play)
            ndice -= len(play)
        else:
            raise IllegalPlay("Roll: %s; play: %s; history: %s" % (roll, play, strategy))
    if strategy.has_qualified(history):
        return sum(history) - 5
    else:
        return 0

def simulate(Strat, ngames):
    strategy = Strat()
    results = [0]*25
    for i in xrange(0, ngames):
        score = playgame(strategy)
        results[score] += 1
    return results

def printOutcomes(strategy, table):
    print "Using strategy %s" % strategy.__name__

    totalGames = float(sum(table))
    totalQualifications = float(sum(table) - table[0])
    qualified = totalQualifications > 0
    if not qualified:
        totalQualifications = 1
        print "Do you even qualify, bro?"
    expectedScore = 0
    for i, outcome in enumerate(table):
        if i == 0:
            print "DNQ: %05.2f%%" % (100 * outcome / totalGames)
        elif i >= 4:
            expectedScore += i * outcome / totalQualifications
            print "%3s: %05.2f%%" % (i, 100 * outcome / totalGames)
    if qualified:
        print "Expected score, given qualification: %.2f" % expectedScore

if __name__ == "__main__":
    for strategy in Strategies:
        results = simulate(strategy, ngames=10000)
        printOutcomes(strategy, results)
        print '=========================================='
