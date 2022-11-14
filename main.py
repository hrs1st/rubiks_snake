from state import *
from simulatorInterface import *
from data import sample_input

if __name__ == "__main__":
    state = State(sample_input['Coordinates'], sample_input['sticky_cubes'])
    simulation = SimulatorInterface()
