import numpy as np
import random

from messaging.MessagingClient import MessagingClient
from messaging.messages.ProximitySensorMsg import ProximitySensorMsg
from messaging.messages.TwoDPoseMsg import TwoDPoseMsg
from messaging.messages.VelocityMsg import VelocityMsg
from utils.ErrorComputing import ErrorComputing
from utils.PID import PID


class ClosedLoopController:

    def __init__(self, freq):
        self.x_pid = PID(freq, 1., 0, 1.)
        self.z_pid = PID(freq, 3., 0, 1.)

        self.messaging = MessagingClient()
        self.messaging.add_listener(self.handle_server_message)

        self.pose = TwoDPoseMsg()
        self.theta = 0
        self.velocity = 0

        self.proximity = {
            "f_r": -1,
            "f_l": -1,
        }

    def handle_server_message(self, message):
        # mi assicuro che sia il messaggio giusto
        if message.is_type(TwoDPoseMsg):
            self.pose = message
        if message.is_type(ProximitySensorMsg):
            self.proximity[message.sensor_name] = message.sensor_value

    def get_pose(self):
        return self.pose

    def set_speed(self, x=0, z=0):
        message = VelocityMsg()
        message.x = np.clip(x, 0, 20)
        message.z = np.clip(z, -0.4, 0.4)

        # Publishing our vel_msg
        self.messaging.publish_message(message)

    def is_near_wall(self, proximity=8):
        # se uno qualunque dei sensori e` inferiore a proximity allora ritorna true, se no false
        for key, value in self.proximity.items():
            if (key == "f_l" or key != 'f_r') and proximity > value > 0:
                return True
        return False

    def step_straight(self):
        # rospy.loginfo("Wall is near: %s" % self.is_near_wall())
        if self.is_near_wall():
            print("Wall crash prevention system active")
            return
        else:
            x_vel = self.x_pid.compute(10)

            self.set_speed(x_vel)

    def step_to_point(self, goal):
        distance_error = ErrorComputing.euclidean_distance(self.pose, goal)
        target_angle = ErrorComputing.steering_angle(self.pose, goal)
        angle_error = ErrorComputing.angle_difference(target_angle, self.theta)
        # Linear velocity in the x-axis.
        x_vel = self.x_pid.compute(distance_error)

        # Angular velocity in the z-axis.
        z_vel = self.z_pid.compute(angle_error)

        self.set_speed(x_vel, z_vel)

    def step_to_angle(self, target_angle):
        error = ErrorComputing.angle_difference(target_angle, self.theta)

        z_vel = self.z_pid.compute(error)

        self.set_speed(0, z_vel)

    def is_at_position(self, position, tolerance=10):
        distance_error = ErrorComputing.euclidean_distance(self.pose, position)
        return distance_error < tolerance

    def is_at_angle(self, target, tolerance=.5):
        error = ErrorComputing.angle_difference(target, self.theta)
        # rospy.loginfo("Current theta %.5f, back theta: %.5f, error: %.5f" % (self.theta, target, error))
        return abs(error) < tolerance

    def face_wall(self):
        if self.is_facing_wall():
            return

        error = self.proximity["c-right"] - self.proximity["c-left"]

        z_vel = self.z_pid.compute(error)
        self.set_speed(0, z_vel)

    def is_facing_wall(self, tol=.001):
        err_center = abs(self.proximity["c-right"] - self.proximity["c-left"])
        if err_center == 0.:
            return False

        return err_center < tol

    def sensor_back_wall(self):
        if self.is_sensor_back_wall():
            return

        error = self.proximity["b-left"] - self.proximity["b-right"]
        # Mean of the errors

        z_vel = self.z_pid.compute(error * 3)
        self.set_speed(0, z_vel)

    def is_sensor_back_wall(self, tol=.0001):

        err_center = abs(self.proximity["b-right"] - self.proximity["b-left"])

        if err_center == 0.:
            return False

        return err_center < tol

    def get_back_theta_random(self):
        if self.theta > 0:
            final_theta = self.theta - np.pi
        else:
            final_theta = self.theta + np.pi

        final_theta = final_theta + random.uniform(-np.pi / 2, np.pi / 2)

        print("Current theta %.5f, back theta: %.5f" % (self.theta, final_theta))

        return final_theta

    def get_back_theta(self):
        if self.theta > 0:
            final_theta = self.theta - np.pi
        else:
            final_theta = self.theta + np.pi

        print("Current theta %.5f, back theta: %.5f" % (self.theta, final_theta))

        return final_theta

