from abc import ABCMeta, abstractmethod

def get_subclasses(c):
    subclasses = c.__subclasses__()
    for d in list(subclasses):
        subclasses.extend(get_subclasses(d))
    return subclasses

class AbstractStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_roll(self, roll, history):
        pass

    def grab_sixes(self, roll):
        return [die for die in roll if die == 6]

    def grab_qualifiers(self, roll):
        if self.has_1(roll) and self.has_4(roll):
            return [1, 4]
        elif self.has_1(roll):
            return [1]
        elif self.has_4(roll):
            return [4]
        return []

    def has_1(self, dice):
        return 1 in dice

    def has_4(self, dice):
        return 4 in dice

    def has_qualified(self, dice):
        return self.has_1(dice) and self.has_4(dice)

    def grab_max(self, roll):
        maxdie = max(roll)
        if maxdie == 6:
            return self.grab_sixes(roll)
        else:
            return [maxdie]

class QualifyAtAllCosts(AbstractStrategy):
    def handle_roll(self, roll, history):
        if self.has_qualified(history):
            return self.grab_max(roll)
        else:
            qualifiers = self.grab_qualifiers(roll)
            if qualifiers:
                return qualifiers + self.grab_sixes(roll)
            else:
                return self.grab_max(roll)

class MaximizeFirstRound(QualifyAtAllCosts):
    def handle_roll(self, roll, history):
        if not history:
            return self.grab_max(roll)
        return super(MaximizeFirstRound, self).handle_roll(roll, history)

class NoOnesInFirstRound(QualifyAtAllCosts):
    def handle_roll(self, roll, history):
        if not history:
            qualifiers = [q for q in self.grab_qualifiers(roll) if q != 1]
            if qualifiers:
                return qualifiers + self.grab_sixes(roll)
            else:
                return self.grab_max(roll)
        return super(NoOnesInFirstRound, self).handle_roll(roll, history)

Strategies = get_subclasses(AbstractStrategy)
