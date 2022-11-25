import json
import random
import sys
from state import *
from simulatorInterface import *
from time import time


class Agent:
    def __init__(self):
        self.actions = []
        self.visited = []
        self.depth = 10

    def act(self, percept):
        print('in act function', percept)
        print(self.actions, self.visited)

        if len(self.actions) == 0:
            t0 = time()

            initial_state = State(percept.coords, percept.sticking_cubes)

            while 1:
                result = self.iterative_deepening_search(initial_state)

                if type(result) is dict and result['goal_reached']:
                    self.actions = result['path']
                    print('\n\nGoal Reached!')
                    print('\npath: ', result['path'])
                    print('\ncoords: ', initial_state.coords)
                    break

                self.depth = self.depth + 10

            print('run time: ', time() - t0)

    def iterative_deepening_search(self, root_state):
        for depth in range(self.depth):
            result = self.depth_limited_search(root_state, depth)
            if type(result) is dict and result['goal_reached']:
                print('ids result', result)
                return result

    def depth_limited_search(self, state, depth):
        print('depth limited search:', depth)

        interface = SimulatorInterface()
        path = []

        if self.is_visited(state.coords, depth):
            print('state already visited')
            return None

        if interface.goal_test(state):
            print('reached goal', path)
            return {'path': path, 'state': state, 'goal_reached': True}

        if depth < 1:
            return path

        valid_actions = interface.valid_actions(state)

        for action in valid_actions:
            child = interface.copy_state(state)
            if interface.validate_action_input(action, state):
                if interface.successor(child, action):
                    path = self.depth_limited_search(child, depth - 1)
                    print(path)
                    if type(path) != list and type(path) is dict and path['goal_reached']:
                        pa = path['path']
                        pa.append(action)
                        print('ended depth limited search', path)
                        return {'path': pa, 'goal_reached': True}
        return {'path': path, 'goal_reached': False}

    def is_visited(self, coords, depth):
        print('in is visited', depth)
        distances = [depth]
        for index, coord in enumerate(coords):
            distances_per_cube = []
            for i in range(index + 1, len(coords)):
                distances_per_cube.append([coord[0] - coords[i][0], coord[1] - coords[i][1], coord[2] - coords[i][2]])
            distances.append(distances_per_cube)
        if distances in self.visited:
            return True
        else:
            self.visited.append(distances)
            return False
