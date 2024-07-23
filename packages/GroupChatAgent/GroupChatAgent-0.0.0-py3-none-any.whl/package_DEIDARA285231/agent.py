import os
import sys
import requests
import importlib
from datetime import timedelta
from firebase_admin import storage
from langchain_openai import ChatOpenAI
from langchain.llms import OpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import VertexAI
from langchain.agents import AgentType, initialize_agent
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class Agent:
    def __init__(self, role: str, goal: str, backstory: str, llm: dict, allow_delegation:bool):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = llm
        self.allow_delegation = allow_delegation
        
        print(f"Initializing Agent(role={self.role}, goal={self.goal}, backstory={self.backstory}, "
                f"LLM={self.llm}, allow_delegation={self.allow_delegation})")
        
    def ask_agent(self, user_id: str, agent_id: str, task: str):
        
        # Obtain tools reference
        spec = self.retrieve_tools(user_id, agent_id)
        custom_tools = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(custom_tools)
        tools = custom_tools.get_tools()
        
        # Define the LLM that needs to be initialized
        match self.llm.get("model"):
            case "GPT_4": 
                llm = ChatOpenAI(
                    model_name="gpt-4-1106-preview", openai_api_key="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"
                )
            case "GPT_3_5": 
                llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo-16k", openai_api_key="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"
                )
            case "PALM_2": 
                llm = VertexAI(max_output_tokens=1000)
            case "Anthropic":
                llm = ChatAnthropic(
                    temperature=self.llm.get("temperature"),
                    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
                    model_name="claude-3-opus-20240229",
                )
            case _:
                raise ValueError(f"Unsupported engine: { self.llm.get('model') }")

        # Initialize the agent with the LLM and set of tools before asking the question
        
        # agent = initialize_agent(
        #         tools,
        #         llm,
        #         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        #         verbose=True,
        #         handle_parsing_errors="Check you output and make sure it conforms!"
        #         "Do not output an action and a final answer at the same time.",
        #     )
        
        # prompt = hub.pull("hwchase17/openai-functions-agent")
        # agent = create_tool_calling_agent(llm, tools, prompt)
        # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        prompt_ai = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template("You are a " + self.role + ". Your goal is to: " + self.goal + ". This is your backstory: " + self.backstory),
                HumanMessagePromptTemplate.from_template(
                    "{task}"
                ),
            ]
        )
        
        conversation = LLMChain(llm=llm, prompt=prompt_ai, verbose=True)
        output_model = conversation.predict(
            task=task,
        )
    
        
        # Invoke the agent to obtain an answer
        #output = agent_executor.invoke({"input":text})
        #output = agent.invoke(text)
        
        return output_model
    
    def retrieve_tools(self, user_id, agent_id):
        """
        This function retrieves tools from firebase, for a specific user and agent.
        """
        # Look for the tools in the fire storage
        bucket = storage.bucket()
        blob = bucket.blob("users/" + user_id + "/" + agent_id + "/tools.py")
        url = blob.generate_signed_url(timedelta(seconds=300), method="GET")

        # Download the requested file and save it locally
        response = requests.get(url, timeout=None)

        local_path = "./static/ToolsAgent/" + user_id + "/" + agent_id

        if not os.path.exists(local_path):
            # If the directory does not exist, it creates it
            print("Does not exist")
            os.makedirs(local_path)

        with open(local_path + "/tools.py", "wb") as f:
            f.write(response.content)

        # Add the path to sys.path to allow imports
        sys.path.append(local_path)

        # Import dynamically the module
        spec = importlib.util.spec_from_file_location("tools", local_path + "/tools.py")

        return spec