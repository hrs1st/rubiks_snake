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

    def act(self, percept):
        print('in act function', percept)  # todo delete
        print(self.actions, self.visited)  # todo delete

        search = self.iterative_deepening_search

        if len(self.actions) == 0:
            print('in act if')  # todo delete

            t0 = time()

            initial_state = State(percept.coords, percept.sticking_cubes)
            while 1:
                result = search(initial_state)
                if type(result) is list:
                    print('found actions', result)  # todo delete
                    self.actions = result
                    break
                if type(result) is State:
                    print('found goal state', result)  # todo delete
                    return self.actions

            print('run time: ', time() - t0)

        action = self.actions[0]
        self.actions = self.actions[1:]
        print('picked an action', action)  # todo delete
        return action

    def iterative_deepening_search(self, root_state):
        print('inside ids', root_state)  # todo delete
        path = []
        goal_reached = False
        input_state = root_state
        for depth in range(1, 2):
            print('INPUT STATE', input_state)
            (state, action) = self.depth_limited_search(input_state)
            if not (state and action):
                continue
            elif not action:
                print('ids state', state)  # todo delete
                goal_reached = True
                break
            print('ids action', action)  # todo delete
            path.append(action)

            if self.is_visited(state.coords, depth):
                print('state is visited', state)  # todo delete
                continue

            input_state = state

        if goal_reached:
            return {'path': path, 'goal_reached': True}

    def is_visited(self, coords, depth):
        print('in is visited', depth)  # todo delete
        distances = [depth]
        for index, cube in enumerate(coords):
            distances_i = []
            for i in range(index + 1, len(coords)):
                distances_i.append([cube[0] - coords[i][0], cube[1] - coords[i][1], cube[2] - coords[i][2]])
            distances.append(distances_i)
        if distances in self.visited:
            return True
        else:
            self.visited.append(distances)
            return False

    def depth_limited_search(self, state):
        print('inside depth dfs')  # todo delete

        interface = SimulatorInterface()

        if interface.goal_test(state):
            print('GOAL: ', state)  # todo delete
            # return state
            raise state

        valid_actions = interface.valid_actions(state)
        for i in range(len(valid_actions)):
            action = random.choice(valid_actions)
            print('action', action)  # todo delete
            print('moving down')  # todo delete
            child_state = interface.copy_state(state)
            interface.validate_action_input(action, state)
            child_state = interface.successor(child_state, {'index1': 23, 'index2': 24, 'degree': 180})
            return child_state, action
        return None
