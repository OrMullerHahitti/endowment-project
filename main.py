import random
import networkx as nx
import os
import matplotlib.pyplot as plt


def generate_random_preferences(num_agents):
    """
    Generate random preferences for each agent.

    Parameters:
    num_agents (int): Number of agents.

    Returns:
    dict: Random preferences for each agent.
    """
    preferences = {}
    agents = list(range(num_agents))

    for agent in agents:
        preferences[agent] = random.sample(agents, len(agents))

    return preferences


def top_trading_cycle(agents, preferences, save_intermediate=False):
    """
    Implement the Top Trading Cycle algorithm and generate the trading graph.

    Parameters:
    agents (list): List of agents, where each agent is represented by an integer.
    preferences (dict): Dictionary where the key is the agent, and the value is a list of preferences.
    save_intermediate (bool): Whether to save intermediate graphs.

    Returns:
    dict: Final allocation of items to agents.
    GEXF: Graph of the trading process.
    """
    # Initialize allocation to None for all agents
    allocation = {agent: None for agent in agents}
    endowments = {agent: agent for agent in agents}  # Each agent initially owns an item with their own number

    # Create a directed graph
    G = nx.DiGraph()
    iteration = 0

    while None in allocation.values():
        cycle = []
        current_agent = agents[0]
        while current_agent not in cycle:
            cycle.append(current_agent)
            current_agent = preferences[current_agent][0]

        # Add cycle to the graph
        for i in range(len(cycle)):
            G.add_edge(cycle[i], preferences[cycle[i]][0])

        # Save intermediate graph
        if save_intermediate:
            intermediate_file_path = f"top_trading_cycle_iter_{iteration}.gexf"
            nx.write_gexf(G, intermediate_file_path)
            print(f"Intermediate graph saved to '{os.path.abspath(intermediate_file_path)}'")
            iteration += 1

        # Perform the trades
        for agent in cycle:
            allocation[agent] = endowments[preferences[agent][0]]
            next_agent = preferences[agent][0]
            for pref in preferences.values():
                if next_agent in pref:
                    pref.remove(next_agent)
            agents.remove(agent)

    # Save the final graph to a GEXF file
    final_file_path = "top_trading_cycle_final.gexf"
    nx.write_gexf(G, final_file_path)
    pos = nx.spring_layout(G)  # or use any other layout like nx.circular_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=15)
    plt.title(" ")
    plt.show()


    print(f"The final trading graph has been saved to '{os.path.abspath(final_file_path)}'")

    return allocation


# Number of agents
num_agents = 10

# Generate random preferences
preferences = generate_random_preferences(num_agents)
agents = list(range(num_agents))

print("Initial preferences:", preferences)

allocation = top_trading_cycle(agents, preferences, save_intermediate=True)
print("\nFinal allocation:", allocation)



