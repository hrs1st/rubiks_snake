from state import *
from simulatorInterface import *
from data import *
from agent import *

if __name__ == "__main__":
    state = State(sample_input1['coordinates'], sample_input1['sticky_cubes'])
    agent = Agent()
    simulation = SimulatorInterface()

    agent.act(state)
