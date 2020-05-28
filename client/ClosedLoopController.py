import numpy as np
import random

from messaging.MessagingClient import MessagingClient
from messaging.messages.ColoredTileSensorMsg import ColoredTileSensorMsg
from messaging.messages.HoleSensorMsg import HoleSensorMsg
from messaging.messages.ProximitySensorMsg import ProximitySensorMsg
from messaging.messages.TwoDPoseMsg import TwoDPoseMsg
from messaging.messages.VelocityMsg import VelocityMsg
from utils.ErrorComputing import ErrorComputing
from utils.PID import PID


class ClosedLoopController:

    def __init__(self, freq):
        self.x_pid = PID(freq, 1., 0, 1.)
        self.z_pid = PID(freq, 2.5, 0, 1.5)

        self.messaging = MessagingClient()
        self.messaging.add_listener(self.handle_server_message)

        self.pose = TwoDPoseMsg()
        self.velocity = 0

        self.proximity = {
            "f_r": -1,
            "f_l": -1,
        }

        self.hole = {
            "h": False
        }

        self.colored = {
            "c_t": False
        }

        self.sensor_color = ""

    def handle_server_message(self, message):
        # mi assicuro che sia il messaggio giusto
        if message.is_type(TwoDPoseMsg):
            self.pose = message
        if message.is_type(HoleSensorMsg):
            self.hole[message.sensor_name] = message.sensor_value
        if message.is_type(ProximitySensorMsg):
            self.proximity[message.sensor_name] = message.sensor_value
        if message.is_type(ColoredTileSensorMsg):
            self.colored[message.sensor_name] = message.sensor_value
            self.sensor_color = message.sensor_color

    def get_pose(self):
        return self.pose

    def set_speed(self, x=0, z=0):
        message = VelocityMsg()
        message.x = np.clip(x, 0, 20)
        message.z = np.clip(z, -0.4, 0.4)

        # Publishing our vel_msg
        self.messaging.publish_message(message)

    def is_near_wall(self, proximity=12):
        # se uno qualunque dei sensori e` inferiore a proximity allora ritorna true, se no false
        for key, value in self.proximity.items():
            if (key == "f_l" or key == 'f_r') and proximity > value > 0:
                return True
        return False

    def is_near_hole(self):
        for key, value in self.hole.items():
            if value:
                return True
        return False

    def step_straight(self, vel = 10):
        # rospy.loginfo("Wall is near: %s" % self.is_near_wall())
        if self.is_near_wall():
            print("Wall crash prevention system active")
            x_vel = 0
        elif self.is_near_hole():
            print("Hole fall prevention system active")
            x_vel = 0
        else:
            x_vel = vel

        if self.colored['c_t']:
            print("sensed color" + self.sensor_color)

        self.set_speed(x_vel)

    def step_to_point(self, goal):
        distance_error = ErrorComputing.euclidean_distance(self.pose, goal)
        target_angle = ErrorComputing.steering_angle(self.pose, goal)
        angle_error = ErrorComputing.angle_difference(target_angle, self.pose.theta)
        # Linear velocity in the x-axis.
        x_vel = self.x_pid.compute(distance_error)

        # Angular velocity in the z-axis.
        z_vel = self.z_pid.compute(angle_error)

        self.set_speed(x_vel, z_vel)

    def step_to_angle(self, target_angle):
        error = ErrorComputing.angle_difference(target_angle, self.pose.theta)

        z_vel = self.z_pid.compute(error)

        self.set_speed(0, z_vel)

    def is_at_position(self, position, tolerance=12):
        distance_error = ErrorComputing.euclidean_distance(self.pose, position)
        return distance_error < tolerance

    def is_at_angle(self, target, tolerance=.5):
        error = ErrorComputing.angle_difference(target, self.pose.theta)
        # rospy.loginfo("Current theta %.5f, back theta: %.5f, error: %.5f" % (self.theta, target, error))
        return abs(error) < tolerance

    def face_wall(self):
        if self.is_facing_wall():
            return

        error = self.proximity["f_r"] - self.proximity["f_l"]

        z_vel = self.z_pid.compute(error)
        self.set_speed(0, z_vel)

    def is_facing_wall(self, tol=.5):
        err_center = abs(self.proximity["f_r"] - self.proximity["f_l"])
        if err_center == 0.:
            return False

        return err_center < tol

    def is_sensor_back_wall(self, tol=.5):

        err_center = abs(self.proximity["b_r"] - self.proximity["b_l"])
        if err_center == 0.:
            return False

        return err_center < tol

    def sensor_back_wall(self):
        if self.is_sensor_back_wall():
            return

        error = self.proximity["b_r"] - self.proximity["b_l"]
        # Mean of the errors

        z_vel = self.z_pid.compute(error * 3)
        self.set_speed(0, z_vel)

    def get_back_theta_random(self):
        if self.pose.theta > 0:
            final_theta = self.pose.theta - np.pi
        else:
            final_theta = self.pose.theta + np.pi

        final_theta = final_theta + random.uniform(-np.pi / 2, np.pi / 2)

        print("Current theta %.5f, back theta: %.5f" % (self.pose.theta, final_theta))

        return final_theta

    def get_back_theta(self):
        if self.pose.theta > 0:
            final_theta = self.pose.theta - np.pi
        else:
            final_theta = self.pose.theta + np.pi

        print("Current theta %.5f, back theta: %.5f" % (self.pose.theta, final_theta))

        return final_theta

