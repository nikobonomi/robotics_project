from math import pow, atan2, sqrt
import numpy as np


class ErrorComputing:

    # compute the distance beetwen 2 poses
    @staticmethod
    def euclidean_distance(actual_pose, goal_pose):
        return sqrt(pow((goal_pose.position.x - actual_pose.position.x), 2) +
                    pow((goal_pose.position.y - actual_pose.position.y), 2))

    # compute the theta from the current pose to the goal
    @staticmethod
    def steering_angle(actual_pose, goal_pose):
        return atan2(goal_pose.position.y - actual_pose.position.y, goal_pose.position.x - actual_pose.position.x)

    # compute the difference beetwen 2 angles
    @staticmethod
    def angle_difference(angle1, angle2):
        return np.arctan2(np.sin(angle1-angle2), np.cos(angle1-angle2))
