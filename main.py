from state import *
from simulatorInterface import *
from data import *
from agent import *

if __name__ == "__main__":
    state = State(sample_input3['coordinates'], sample_input3['sticky_cubes'])
    simulation = SimulatorInterface()
    agent = Agent()

    print(state, simulation, agent)  # todo delete

    while True:
        print('inside main loop')  # todo delete

        action = agent.act(state)

        if type(action) is list:
            print('Goal reached with actions: ', action)
            break

        simulation.successor(state, action)
