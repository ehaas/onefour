import random
from strategy import QualifyAtAllCosts


def rolldice(count):
    return [random.randint(1, 6) for x in xrange(0, count)]

def validate(roll, play):
    """
        TODO: make sure this is a valid play given the dice
    """
    return len(play) >= 1

def playgame(strategy, ndice=6):
    history = []
    while ndice > 0:
        roll = rolldice(ndice)
        play = strategy.handle_roll(roll, history)
        if validate(roll, play):
            history.extend(play)
            ndice -= len(play)
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
    totalGames = float(sum(table))
    print "Using strategy %s" % strategy.__name__
    for i, outcome in enumerate(table):
        if i == 0:
            print "DNQ: %05.2f%%" % (100 * outcome / totalGames)
        elif i >= 4:
            print "%3s: %05.2f%%" % (i, 100 * outcome / totalGames)

if __name__ == "__main__":
    results = simulate(QualifyAtAllCosts, ngames=10000)
    printOutcomes(QualifyAtAllCosts, results)
