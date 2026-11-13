class MinimumEffortGame:
    def __init__(self, group_size):
        """
        Initializes the Minimum-Effort Coordination Game.
        """
        self.group_size = group_size
        self.history = []

    def calculate_payoffs(self, agent_efforts):
        """
        Takes a dictionary of agent efforts, calculates the group minimum, 
        and determines the payoff for each agent.
        
        Payoff function: U_i = 2 * m - e_i
        (where m is the minimum effort, and e_i is the individual effort)
        """
        # Ensure all efforts are within the valid 1-7 scale
        for name, effort in agent_efforts.items():
            if not (1 <= effort <= 7):
                raise ValueError(f"Effort {effort} for agent {name} is out of bounds (must be 1-7).")

        # Find the weakest link (minimum effort in the group)
        min_effort = min(agent_efforts.values())
        
        payoffs = {}
        for agent_name, effort in agent_efforts.items():
            # Apply the payoff function
            payoff = (2 * min_effort) - effort
            payoffs[agent_name] = payoff
            
        # Store the round results in history
        round_result = {
            'agent_efforts': agent_efforts,
            'min_effort': min_effort,
            'payoffs': payoffs
        }
        self.history.append(round_result)
        
        return round_result