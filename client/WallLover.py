#!/usr/bin/env python
from enum import Enum

from client.ClosedLoopController import ClosedLoopController
from utils.RateKeeper import RateKeeper


class WallLoverState(Enum):
    SearchingWall = 0,
    FacingWall = 1,
    TurningBack = 2,
    TurningBackSensor = 3,
    Going2mFromWall = 4,
    End = 5


class WallLover:

    def __init__(self):
        FREQ = 10

        self.rate_keeper = RateKeeper(10)

        # uso il controller in controller.py per far muovere il robottino
        self.controller = ClosedLoopController(FREQ)

        self.wall_ahead = False
        self.target_theta = 0
        self.goal = None
        self.state = WallLoverState.SearchingWall

    def step(self):
        if self.state == WallLoverState.SearchingWall:
            self.controller.step_straight(100)
            if self.controller.is_near_wall():
                print("The wall is near")
                self.controller.set_speed()
                self.state = WallLoverState.FacingWall

        elif self.state == WallLoverState.FacingWall:
            self.controller.face_wall()
            if self.controller.is_facing_wall():
                print("The wall is in front of me")
                self.controller.set_speed()
                self.state = WallLoverState.TurningBack
                self.target_theta = self.controller.get_back_theta()

        elif self.state == WallLoverState.TurningBack:
            self.controller.step_to_angle(self.target_theta)
            if self.controller.is_at_angle(self.target_theta, .25):
                print("The wall is at by back with odometry")
                self.controller.set_speed()
                self.state = WallLoverState.TurningBackSensor

        elif self.state == WallLoverState.TurningBackSensor:
            self.controller.sensor_back_wall()
            if self.controller.is_sensor_back_wall():
                print("The wall is at by back with sensors")
                self.controller.set_speed()
                self.state = WallLoverState.SearchingWall

        elif self.state != WallLoverState.End:
            self.state = WallLoverState.SearchingWall

