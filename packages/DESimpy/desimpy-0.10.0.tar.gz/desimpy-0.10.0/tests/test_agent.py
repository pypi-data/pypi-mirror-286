from abc import ABC
from des import Agent  # Adjust the import according to your module structure

# Create a concrete subclass of Agent for testing
class ConcreteAgent(Agent):
    pass

def test_agent_initialization():
    agent = ConcreteAgent(name="TestAgent")
    assert agent.name == "TestAgent"

def test_agent_repr():
    agent = ConcreteAgent(name="TestAgent")
    assert repr(agent) == "ConcreteAgent(name=TestAgent)"

