# Here I will implement different scheduling algorithms
# All these functions are still missing the part in which
# I call ask_agent()

import random
from collections import deque

def random_choice(agents_list, user_id, agent_id, session_id, task):
    output_list = []
    output = ""
    for i in range(len(agents_list)):
        random_agent = random.choice(agents_list)
        # Obtain the index of the random agent
        id = agents_list.index(random_agent)
        # Ask the question to the agent
        output = random_agent.ask_agent(user_id, agent_id, output + task)
        output_list.append(output)
        agents_list.pop(id)
        
    return output_list
    
def round_robin(agents_list, num_cycles, user_id, agent_id, session_id, task):
    if not isinstance(agents_list, deque):
        agents_list = deque(agents_list)
    
    output_list = []
    output = ""
    for _ in range(len(agents_list)):
        agent = agents_list.popleft()
        output = agent.ask_agent(user_id, agent_id, output + task)
        output_list.append(output)
        agents_list.append(agent)
        
    return output_list
        
def weighted_selection(agents_list, weights, user_id, agent_id, session_id, task):
    
    output_list = []
    output = ""
    for i in range(len(agents_list)):
        weighted_agent = random.choices(agents_list, weights=weights, k=1)[0]
        id = agents_list.index(weighted_agent)
        
        output = weighted_agent.ask_agent(user_id, agent_id, output + task)
        output_list.append(output)
        agents_list.pop(id)
        weights.pop(id)

    return output_list

def priority_selection(agents_list, priority, user_id, agent_id, session_id, task):
    output_list = []
    output = ""
    
    agents = list(zip(agents_list, priority))
    agents_sorted = sorted(agents, key=lambda x: x[1], reverse=True)

    for agent in agents_sorted:
        output = agent[0].ask_agent(user_id, agent_id, task)
        output_list.append(output)
        
    return output_list