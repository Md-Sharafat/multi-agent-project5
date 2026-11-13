import random

class AdaptiveAgent:
    def __init__(self, name):
        self.name = name
        self.current_effort = random.randint(1, 7)

    def choose_effort(self, history):
        """Reduces effort if payoff was lost. Increases cautiously if coordination succeeded."""
        if not history:
            return self.current_effort
        
        last_round = history[-1]
        last_min = last_round['min_effort']
        my_last_effort = last_round['agent_efforts'][self.name]

        if my_last_effort > last_min:
            self.current_effort = last_min
        elif my_last_effort == last_min and last_min < 7:
            self.current_effort = min(7, self.current_effort + 1)
        
        return self.current_effort