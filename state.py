from scipy.spatial.transform import Rotation as R
from simulatorInterface import *


class State:
    def __init__(self, coords, sticking_cubes):
        self.coords = coords
        self.sticking_cubes = sticking_cubes

    def take_action(self, action):
        (i, j, degree) = (action['index1'], action['index2'], action['degree'])
        coords_backup = self.coords[:]

        if j < 25:
            is_joint = self.is_joint_axis([i, j, j + 1])
            if is_joint:
                sticking_indexes = self.find_sticking(i, self.sticking_cubes)
                if len(sticking_indexes) > 0:
                    axis = self.find_joint_axis(i, j)
                    if sticking_indexes[-1]['is_v']:
                        last_index = len(self.coords)
                    else:
                        last_index = sticking_indexes[-1]['index']
                    self.rotate(axis, i, last_index, degree)
            else:
                axis = self.find_joint_axis(i, j)
                self.rotate(axis, i, len(self.coords), degree)
        else:
            axis = self.find_joint_axis(i, j)
            self.rotate(axis, i, j, degree)

        if len(set(self.coords)) != len(self.coords):
            self.coords = coords_backup[:]

    def rotate(self, axis, i, j, degree):
        begin = min(i, j)
        end = max(i, j)
        for i in range(begin, end + 1):
            rotation = R.from_euler(axis, degree, degrees=True)
            rotated = rotation.apply(self.coords[i])
            rounded_coords = []
            for coord in rotated:
                rounded_coords.append(round(coord))
            self.coords[i] = rounded_coords

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
        for i in range(3):
            if self.coords[a][i] == self.coords[b][i] == self.coords[c][i]:
                return True
        return False

    def find_sticking(self, i, sticking_cubes):
        indexes = []
        while i < 26:
            if [i + 1, i + 2] in sticking_cubes or [i + 2, i + 1] in sticking_cubes:
                if i not in indexes:
                    is_v = not self.is_joint_axis([i, i + 1, i + 2])
                    indexes.append({'index': i, 'is_v': is_v})
                    if is_v:
                        return indexes
                indexes.append(i + 1)
            else:
                return indexes
            i += 1
        return indexes
