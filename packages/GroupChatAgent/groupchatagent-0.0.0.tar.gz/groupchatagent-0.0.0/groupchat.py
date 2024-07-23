from src.package_DEIDARA285231.agent import Agent
from scheduling import random_choice, round_robin, weighted_selection, priority_selection

class Groupchat:
    def __init__(self, agents: list[Agent], task: str, next_agent_selection: str):
        self.agents = agents
        self.task = task
        self.next_agent_selection = next_agent_selection
        
        print(f"Initializing GroupChat(agents={self.agents}, task={self.task}, next_agent_selection={self.next_agent_selection}")
    
    def ask_groupchat(self, user_id: str, agent_id: str, session_id: str, weights):
        
        output_list = []
        match self.next_agent_selection:
            case "random_choice":
                output_list = random_choice(self.agents, user_id, agent_id, session_id, self.task)
            case "round_robin":
                output_list = round_robin(self.agents, 1, user_id, agent_id, session_id, self.task)
            case "weighted_selection":
                # Define how weights are taken
                output_list = weighted_selection(self.agents, weights, user_id, agent_id, session_id, self.task)
            case "priority_selection":
                output_list = priority_selection(self.agents, weights, user_id, agent_id, session_id, self.task)
            case _ :
                #print(self.agents[0])
                agent_reply = self.agents[0].ask_agent(user_id, agent_id, self.task)
                output_list.append(agent_reply)
                # Cycle every agent and ask for its view on the task.
                for agent in self.agents[1:]: 
                    # Take the replies of each individual agent and pass it to the others
                    agent_reply = agent.ask_agent(user_id, agent_id, agent_reply + self.task)
                    output_list.append(agent_reply)
            
        # Once the last agent defines its answer we can declase the task as finished
        return output_list