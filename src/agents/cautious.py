import random

class CautiousAgent:
    def __init__(self, name):
        self.name = name
        self.first_round = True

    def choose_effort(self, history):
        """Starts randomly. Matches the previous group's minimum effort thereafter."""
        if self.first_round or not history:
            self.first_round = False
            return random.randint(1, 7)
        
        return history[-1]['min_effort']