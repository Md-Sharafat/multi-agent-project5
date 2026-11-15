import os
import matplotlib.pyplot as plt
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
        current_efforts = {agent.name: agent.choose_effort(game.history) for agent in agents}
        round_result = game.calculate_payoffs(current_efforts)
        
        if round_num <= 5 or round_num > num_rounds - 5:
            print(f"Round {round_num:02d}: Min Effort = {round_result['min_effort']} | Efforts: {current_efforts}")
        elif round_num == 6:
            print("... [Rounds 6 to 45 hidden for brevity] ...")

    # Calculate 50-round summary metrics for comparison
    avg_min_effort = sum(r['min_effort'] for r in game.history) / num_rounds
    all_payoffs = [p for r in game.history for p in r['payoffs'].values()]
    avg_payoff = sum(all_payoffs) / len(all_payoffs)

    print(f"\nFinal Round Payoffs: {game.history[-1]['payoffs']}")
    print(f"50-Round Avg Min Effort: {avg_min_effort:.2f} | Avg Agent Payoff: {avg_payoff:.2f}")

    return {
        'config': config_name,
        'avg_min_effort': avg_min_effort,
        'avg_payoff': avg_payoff
    }

def generate_comparison_chart(results):
    labels = ["5 Optimistic", "5 Cautious", "5 Adaptive", "Mixed Group"]
    min_efforts = [r['avg_min_effort'] for r in results]
    payoffs = [r['avg_payoff'] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12']

    # Bar Chart 1: Average Group Minimum Effort (Coordination Level)
    bars1 = ax1.bar(labels, min_efforts, color=colors, width=0.55)
    ax1.set_title("Avg Group Minimum Effort (50 Rounds)", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Effort Level (1 - 7)")
    ax1.set_ylim(0, 8)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.15, f"{yval:.2f}", ha='center', fontweight='bold')

    # Bar Chart 2: Average Payoff per Agent
    bars2 = ax2.bar(labels, payoffs, color=colors, width=0.55)
    ax2.set_title("Avg Payoff per Agent (50 Rounds)", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Payoff Score")
    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.set_ylim(min(min(payoffs) - 1, -1), 8)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    for bar in bars2:
        yval = bar.get_height()
        offset = 0.15 if yval >= 0 else -0.45
        ax2.text(bar.get_x() + bar.get_width()/2, yval + offset, f"{yval:.2f}", ha='center', fontweight='bold')

    plt.suptitle("Phase 2 Baseline: Rule-Based Strategy Comparison (N=5)", fontsize=14, fontweight='bold')
    plt.tight_layout()

    os.makedirs("data", exist_ok=True)
    output_path = "data/phase2_comparison.png"
    plt.savefig(output_path, dpi=300)
    print(f"\n[SUCCESS] Comparison chart saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    results = []
    
    # Config 1: All Optimistic
    results.append(run_simulation("Config 1: 5 Optimistic", [OptimisticAgent(f"Opti_{i}") for i in range(1, 6)]))
    
    # Config 2: All Cautious
    results.append(run_simulation("Config 2: 5 Cautious", [CautiousAgent(f"Caut_{i}") for i in range(1, 6)]))
    
    # Config 3: All Adaptive
    results.append(run_simulation("Config 3: 5 Adaptive", [AdaptiveAgent(f"Adap_{i}") for i in range(1, 6)]))
    
    # Config 4: Mixed Group (2 Opti, 2 Cautious, 1 Adap)
    mixed_agents = [
        OptimisticAgent("Opti_1"),
        OptimisticAgent("Opti_2"),
        CautiousAgent("Caut_1"),
        CautiousAgent("Caut_2"),
        AdaptiveAgent("Adap_1")
    ]
    results.append(run_simulation("Config 4: Mixed Group", mixed_agents))

    # Print final summary table & generate chart
    print(f"\n{'='*60}")
    print("PHASE 2 SUMMARY COMPARISON")
    print(f"{'='*60}")
    print(f"{'Configuration':<25} | {'Avg Min Effort':<15} | {'Avg Payoff':<12}")
    print("-" * 60)
    for r in results:
        print(f"{r['config']:<25} | {r['avg_min_effort']:<15.2f} | {r['avg_payoff']:<12.2f}")

    generate_comparison_chart(results)