from environment import MinimumEffortGame
from agents.optimistic import OptimisticAgent
from agents.cautious import CautiousAgent
from agents.adaptive import AdaptiveAgent

def run_simulation(config_name, agents, num_rounds=50):
    print(f"\n{'='*60}")
    print(f"--- Running {config_name} ({num_rounds} Rounds) ---")
    print(f"{'='*60}")
    
    game = MinimumEffortGame(group_size=len(agents))
    
    for round_num in range(1, num_rounds + 1):
        # Collect efforts from all agents
        current_efforts = {agent.name: agent.choose_effort(game.history) for agent in agents}
        
        # Calculate results
        round_result = game.calculate_payoffs(current_efforts)
        
        # Print the first 5 and last 5 rounds to keep the console clean
        if round_num <= 5 or round_num > num_rounds - 5:
            print(f"Round {round_num:02d}: Min Effort = {round_result['min_effort']} | Efforts: {current_efforts}")
        elif round_num == 6:
            print("... [Rounds 6 to 45 hidden for brevity] ...")

    print(f"\nFinal Round Payoffs: {game.history[-1]['payoffs']}")

if __name__ == "__main__":
    # Config 1: All Optimistic (Baseline Perfect Coordination)
    run_simulation("Config 1: 5 Optimistic Agents", [OptimisticAgent(f"Opti_{i}") for i in range(1, 6)])
    
    # Config 2: All Cautious (Fear of Loss Collapse)
    run_simulation("Config 2: 5 Cautious Agents", [CautiousAgent(f"Caut_{i}") for i in range(1, 6)])
    
    # Config 3: All Adaptive (Organic Learning)
    run_simulation("Config 3: 5 Adaptive Agents", [AdaptiveAgent(f"Adap_{i}") for i in range(1, 6)])
    
    # Config 4: Mixed Group (2 Opti, 2 Cautious, 1 Adap)
    mixed_agents = [
        OptimisticAgent("Opti_1"),
        OptimisticAgent("Opti_2"),
        CautiousAgent("Caut_1"),
        CautiousAgent("Caut_2"),
        AdaptiveAgent("Adap_1")
    ]
    run_simulation("Config 4: The Mixed Group", mixed_agents)