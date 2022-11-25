from data import goal_coords
from state import *
import json


class SimulatorInterface:
    def __int__(self):
        pass

    def successor(self, state, action):
        print('successor', action, state)  # todo delete
        self.validate_action_input(action, state)
        return state.take_action(action)

    def copy_state(self, state):
        _copy = State(None, state.sticking_cubes)
        _copy.coords = state.coords[:]
        return _copy

    def perceive(self, state):
        return json.dumps({'Coordinates': state.coords, 'sticky_cubes': state.sticking_cubes})

    def goal_test(self, state):
        for i in range(27):
            is_goal = True
            (x, y, z) = (state.coords[i][0], state.coords[i][1], state.coords[i][2])
            normalized_coords = self.normalize_coords(state, [x, y, z])
            for coord in normalized_coords:
                if coord not in goal_coords:
                    is_goal = False
                    break
            if is_goal:
                return True
        return False

    def normalize_coords(self, state, root):
        normalized_coords = []
        for coord in state.coords:
            normalized_coords.append([coord[0] - root[0], coord[1] - root[1], coord[2] - root[2]])
        return normalized_coords

    def validate_action_input(self, action, state):
        if not action['degree'] in [90, -90, 180]:
            raise 'invalid degree'
        if not (0 <= action['index1'] < 26 and 0 < action['index2'] <= 26):
            raise 'invalid index range'
        if abs(action['index1'] - action['index2']) != 1:
            raise 'invalid index'
        if action not in self.valid_actions(state):
            raise 'invalid action'

    def valid_actions(self, state):
        actions = []
        for i in range(26):
            cube_actions = self.find_actions_per_cube(i, i + 1, state)
            for action in cube_actions:
                actions.append(action)
        print('VALID ACTIONS', actions)  # todo delete
        return actions

    def find_actions_per_cube(self, i, j, state):
        actions = []
        if 1 < i < 26:

            v_check = self.is_vertical(state, [i - 1, i, i + 1])
            if v_check:
                actions.append({'index1': i, 'index2': j, 'degree': 90})
                actions.append({'index1': i, 'index2': j, 'degree': -90})
                actions.append({'index1': i, 'index2': j, 'degree': 180})
                return actions
        sticking_indexes = self.find_sticking(i, state.sticking_cubes)
        if len(sticking_indexes) > 0:
            actions.append({'index1': i, 'index2': j, 'degree': 90})
            actions.append({'index1': i, 'index2': j, 'degree': -90})
            actions.append({'index1': i, 'index2': j, 'degree': 180})
        return actions

    def is_vertical(self, state, indexes):
        return not self.is_joint_axis(state, indexes)

    def is_joint_axis(self, state, indexes):
        [a, b, c] = indexes
        joint_axis1 = self.find_joint_axis(state, a, b)
        joint_axis2 = self.find_joint_axis(state, b, c)
        if (joint_axis1 and joint_axis2) and joint_axis2 == joint_axis1:
            return True
        return False

    def find_joint_axis(self, state, i, j):
        if state.coords[i][1] == state.coords[j][1] and state.coords[i][2] == state.coords[j][2]:
            return 'x'
        elif state.coords[i][2] == state.coords[j][2] and state.coords[i][0] == state.coords[j][0]:
            return 'y'
        elif state.coords[i][0] == state.coords[j][0] and state.coords[i][1] == state.coords[j][1]:
            return 'z'
        else:
            return ''

    def find_sticking(self, i, sticking_cubes):
        indexes = []
        while i <= 25:
            if [i, i + 1] in sticking_cubes or [i + 1, i] in sticking_cubes:
                if i not in indexes:
                    indexes.append(i)
            else:
                return indexes
            i = i + 1
        return indexes
