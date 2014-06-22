from abc import ABCMeta, abstractmethod

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

class QualifyAtAllCosts(AbstractStrategy):
    def handle_roll(self, roll, history):
        if self.has_qualified(history):
            maxdie = max(roll)
            if maxdie == 6:
                return self.grab_sixes(roll)
            else:
                return [maxdie]
        else:
            return self.grab_qualifiers(roll) + self.grab_sixes(roll)
