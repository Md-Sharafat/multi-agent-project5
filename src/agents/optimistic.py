class OptimisticAgent:
    def __init__(self, name):
        self.name = name

    def choose_effort(self, history):
        """Always aims for the highest effort (7), assuming perfect coordination."""
        return 7