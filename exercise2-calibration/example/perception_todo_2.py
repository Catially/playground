#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.planning.proto.planning_pb2 import Trajectory
from modules.planning.proto.planning_pb2 import Point
from cyber_py import cyber
import sys

sys.path.append("../")


# TODO
def translation_view(x, y):
    x_r = 125.3 - 0.003918 * x - 0.1418 * y
    y_r = 48.78 - 0.1446 * x - y * 0.008061
    return x_r, y_r


class Exercise(object):

    def __init__(self, node):
        self.node = node
        self.planning_path = Trajectory()

        # TODO create reader
        self.node.create_reader("/perception/get_point",
                                Trajectory, self.callback)
        # TODO create writer
        self.writer = self.node.create_writer(
            "/perception/translation_point", Trajectory)

    def callback(self, data):
        # TODO
        # print(data.frame_no)
        # TODO reshape
        self.reshape(data)
        # TODO publish, write to channel
        if not cyber.is_shutdown():
            self.write_to_channel()

    def write_to_channel(self):
        # TODO
        self.writer.write(self.planning_path)

    def reshape(self, data):

        # print(data)

        point_array = data.point
        self.planning_path = Trajectory()

        for i, point in enumerate(point_array):
            point_xy = Point()
            new_x, new_y = translation_view(point.x, point.y)

            point_xy.x = new_x
            point_xy.y = new_y
            self.planning_path.point.append(point_xy)


if __name__ == '__main__':
    cyber.init()

    # TODO update node to your name
    exercise_node = cyber.Node("read_point")
    exercise = Exercise(exercise_node)

    exercise_node.spin()

    cyber.shutdown()
