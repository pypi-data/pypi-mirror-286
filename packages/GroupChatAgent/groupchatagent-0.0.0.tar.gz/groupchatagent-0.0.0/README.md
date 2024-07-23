# GroupChatAgent Library

## Overview

GroupChatAgent is a Python library designed to facilitate the creation of group chats among multiple agents. These agents can communicate with each other, share information, and collaboratively reach a refined answer to a given problem. This library is ideal for applications requiring consensus building, brainstorming, and collaborative problem-solving among automated agents.

## Features

- **Create Group Chats**: Easily create group chats with multiple agents.
- **Agent Communication**: Enable agents to communicate and share information in real-time.
- **Collaborative Problem-Solving**: Agents work together to refine answers and reach a consensus.
- **Customizable Agents**: Define and customize the behavior and characteristics of each agent.
- **Flexible Integration**: Integrate with other systems and libraries to extend functionality.

## Installation

To install GroupChatAgent, simply use pip:

```bash
pip install groupchatagent
```

## Usage

Here's a basic example of how to use the GroupChatAgent library:

```bash
from groupchatagent import GroupChat, Agent

# Define custom agent behavior
class CustomAgent(Agent):
    def process_message(self, message):
        # Custom logic for processing messages
        return f"Processed: {message}"

# Create agents
agent1 = CustomAgent(name="Agent1")
agent2 = CustomAgent(name="Agent2")
agent3 = CustomAgent(name="Agent3")

# Create a group chat with the agents
group_chat = GroupChat(agents=[agent1, agent2, agent3])

# Send a message to the group chat
response = group_chat.send_message("Initial problem to solve")

# Print the refined answer
print(response)
```

## Documentation

For detailed documentation, including advanced usage and API reference, please visit the [official documentation.](pidetto.com)

## Contributing

We welcome contributions to the GroupChatAgent library. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Implement your changes and add tests.
4. Submit a pull request with a detailed description of your changes.
For more information, please see our contributing guidelines.

## License
GroupChatAgent is licensed under the MIT License. See the LICENSE file for more information.

## Contact
For questions, suggestions, or support, please contact us at e.schioccola@bytecareitalia.com.

Thank you for using GroupChatAgent! We hope this library helps you build powerful and collaborative agent-based systems.