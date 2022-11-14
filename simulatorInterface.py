from state import *
from data import goal_coords
import json


class SimulatorInterface:
    def __int__(self):
        pass

    def successor(self, state, action):
        action = json.loads(action)
        self.validate_action_input(action, state)
        return state.take_action(action)

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
        for i in range(25):
            actions.append(self.find_actions_per_cube(i, i + 1, state))
        return actions

    def find_actions_per_cube(self, i, j, state):
        actions = []
        if i > 1:
            prev_c = state.coords[i - 1]
            current_c = state.coords[i]
            next_c = state.coords[i + 1]

            v_check = self.is_vertical([prev_c, current_c, next_c])
            if v_check:
                actions.append([
                    {'index1': i, 'index2': j, 'degree': 90},
                    {'index1': i, 'index2': j, 'degree': -90},
                    {'index1': i, 'index2': j, 'degree': 180}
                ])
                return actions
        sticking_indexes = self.find_sticking(i, state)
        if len(sticking_indexes) > 0:
            actions.append([
                {'index1': i, 'index2': j, 'degree': 90},
                {'index1': i, 'index2': j, 'degree': -90},
                {'index1': i, 'index2': j, 'degree': 180}
            ])
        return actions

    def is_vertical(self, coords):
        for i in range(3):
            if coords[0][i] == coords[1][i] == coords[2][i]:
                return False
        return True

    def find_sticking(self, i, state):
        indexes = []
        while i < 26:
            if [i + 1, i + 2] in state.sticking_cubes or [i + 2, i + 1] in state.sticking_cubes:
                if i not in indexes:
                    indexes.append(i)
                indexes.append(i + 1)
            else:
                return indexes
            i += 1
        return indexes
