from scipy.spatial.transform import Rotation as R
import numpy as np


class State:
    def __init__(self, coords, sticking_cubes):
        self.coords = coords
        self.sticking_cubes = sticking_cubes

    def take_action(self, action):
        print('take action', action)  # todo delete
        (i, j, degree) = (action['index1'], action['index2'], action['degree'])
        coords_backup = self.coords[:]
        begin = min(i, j)
        end = max(i, j)

        if end < 25:
            is_joint = self.is_joint_axis([begin, end, end + 1])
            if is_joint:
                sticking_indexes = self.find_sticking(begin, self.sticking_cubes)
                if len(sticking_indexes) > 0:
                    axis = self.find_joint_axis(begin, end)
                    if sticking_indexes[-1]['is_v']:
                        last_index = len(self.coords) - 1
                    else:
                        last_index = sticking_indexes[-1]['index2']
                    self.rotate(axis, begin, last_index, degree)
            else:
                axis = self.find_joint_axis(begin, end)
                self.rotate(axis, begin, len(self.coords) - 1, degree)  # fixme this case
        else:
            axis = self.find_joint_axis(begin, end)
            self.rotate(axis, begin, end, degree)

        if not self.validate_move(self.coords):
            self.coords = coords_backup[:]

    def rotate(self, axis, i, j, degree):
        print('rotate', axis, i, j, degree)  # todo delete
        begin = min(i, j)
        end = max(i, j)
        begin_coord = self.coords[begin]
        if degree == 180:
            for i in range(begin, end):
                coord = self.coords[i]
                if axis == 'x':
                    x = begin_coord[0]
                else:
                    x = begin_coord[0] + np.sign(begin_coord[0] - coord[0]) * abs(begin_coord[0] - coord[0])
                if axis == 'y':
                    y = begin_coord[1]
                else:
                    y = begin_coord[1] + np.sign(begin_coord[1] - coord[1]) * abs(begin_coord[1] - coord[1])
                if axis == 'z':
                    z = begin_coord[2]
                else:
                    z = begin_coord[2] + np.sign(begin_coord[2] - coord[2]) * abs(begin_coord[2] - coord[2])
                self.coords[i] = [x, y, z]
        elif degree == 90 or degree == -90:
            for i in range(begin, end):
                coord = self.coords[i]
                if axis == 'x':
                    x = begin_coord[0]
                else:
                    x = begin_coord[0] + np.sign(degree) * np.sign(
                        (begin_coord[2] - coord[2]) if axis == 'y' else (begin_coord[1] - coord[1])) * abs(
                        (begin_coord[2] - coord[2]) if axis == 'y' else (begin_coord[1] - coord[1]))
                if axis == 'y':
                    y = begin_coord[1]
                else:
                    y = begin_coord[0] + np.sign(degree) * np.sign(
                        (begin_coord[0] - coord[0]) if axis == 'z' else (begin_coord[2] - coord[2])) * abs(
                        (begin_coord[0] - coord[0]) if axis == 'z' else (begin_coord[2] - coord[2]))
                if axis == 'z':
                    z = begin_coord[2]
                else:
                    z = begin_coord[2] + np.sign(degree) * np.sign(
                        (begin_coord[1] - coord[1]) if axis == 'x' else (begin_coord[0] - coord[0])) * abs(
                        (begin_coord[1] - coord[1]) if axis == 'x' else (begin_coord[0] - coord[0]))
                self.coords[i] = [x, y, z]
        else:
            raise 'wrong degree input'

    def find_joint_axis(self, i, j):
        if self.coords[i][1] == self.coords[j][1] and self.coords[i][2] == self.coords[j][2]:
            return 'x'
        elif self.coords[i][2] == self.coords[j][2] and self.coords[i][0] == self.coords[j][0]:
            return 'y'
        elif self.coords[i][0] == self.coords[j][0] and self.coords[i][1] == self.coords[j][1]:
            return 'z'
        else:
            return ''

    def is_joint_axis(self, indexes):
        [a, b, c] = indexes
        joint_axis1 = self.find_joint_axis(a, b)
        joint_axis2 = self.find_joint_axis(b, c)
        if (joint_axis1 and joint_axis2) and joint_axis2 == joint_axis1:
            return True
        return False

    def find_sticking(self, i, sticking_cubes):
        indexes = []
        res = []
        while i < 26:
            obj = {}
            if [i, i + 1] in sticking_cubes or [i + 1, i] in sticking_cubes:
                if i not in indexes:
                    is_v = not self.is_joint_axis([i, i + 1, i + 2])
                    indexes.append(i)
                    obj['index'] = i
                    obj['is_v'] = is_v
                    obj['index2'] = i + 1
                    res.append(obj)
                    if is_v:
                        return res
            else:
                return res
            i = i + 1
        return res

    def validate_move(self, coords):
        for index in range(len(coords)):
            for i in range(index, len(coords)):
                if coords[index] == coords[i]:
                    print('INVALID MOVE', coords[index], coords[i])  # todo delete
                    return False
        print('VALID MOVE')  # todo delete
        return True
