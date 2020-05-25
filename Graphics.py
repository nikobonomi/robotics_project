import math
import tkinter as tk

from environment.Obstacle import Obstacle
from environment.Tile import Tile
from robot.TwoDRobot import TwoDCartesianPose, TwoDRobot
from typing import Dict, List

from sensor.Sensor import Sensor


class SreGui:
    def __init__(self, w: int = 800, h: int = 600):
        self._root = tk.Tk()
        self._width: int = w
        self._height: int = h
        self._canvas = tk.Canvas(self._root, width=self._width, height=self._height)
        # così mette l'origine in centro al posto di in alto a sinistra
        self._canvas.configure(scrollregion=(-w / 2, -h / 2, w / 2, h / 2))

        self.draw_axis()

        self._robots: Dict[TwoDRobot] = {}
        self._sensors: Dict[Sensor] = {}
        self._tiles: Dict[Tile] = {}
        # self._robot = self._canvas.create_polygon(w / 2, h / 2, w / 2 + 20, h / 2, w / 2 + 10, h / 2 - 20)
        self.update_canvas()

    def new_robot(self, robot: TwoDRobot):
        self._robots[robot] = self._canvas.create_polygon(robot.get_robot_draw_points())
        for sensor in robot.sensors:
            self.new_sensor(sensor)
        self.update_canvas()

    def new_sensor(self, sensor: Sensor):
        self._sensors[sensor] = self._canvas.create_line(sensor.vertexes, fill="red", width=1)
        self.update_canvas()

    def new_tile(self, tile: Tile):
        self._tiles[tile] = self._canvas.create_polygon(tile.vertexes, fill=tile.filling, outline=tile.outline, width=tile.width)
        self.update_canvas()

    def draw_axis(self):
        # disegno gli assi
        self._canvas.create_line([0, 0, 100, 0], width=1, fill='red', dash=(4, 2))
        self._canvas.create_line([0, 0, 0, 100], width=1, fill='green', dash=(4, 2))

    def update_canvas(self):
        self._canvas.pack()
        self._root.update()

    @staticmethod
    def rotate(points, angle):
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        new_points = []
        for i in range(0, (len(points)), 2):
            # estraggo le coordinate
            x_old = points[i]
            y_old = points[i + 1]
            # calcolo le nuove
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            # appendo i nuovi valori alla lista di ritorno
            new_points.append(x_new)
            new_points.append(y_new)
        return new_points

    def move_widget(self, widget, points: List[int], cart_pose: TwoDCartesianPose):
        # porto il robot all'origine con i punti ruotati
        self._canvas.coords(widget, points)
        # lo muovo al posto giusto
        self._canvas.move(widget, cart_pose.x, cart_pose.y)

    def step_gui(self):
        for robot in self._robots.keys():
            cartesian_pose = robot.get_cartesian_pose()
            # calcolo la rotazione del robot all'origine
            points = self.rotate(robot.get_robot_draw_points(), cartesian_pose.theta)
            robot_widget = self._robots[robot]

            self.move_widget(robot_widget, points, cartesian_pose)

            # aggiorno la posizione dei sensori
            for sensor in robot.sensors:
                widget = self._sensors[sensor]

                # calcolo la rotazione del sensore all'origine rispetto al centro del robot
                points = self.rotate(sensor.vertexes, cartesian_pose.theta)

                self.move_widget(widget, points, cartesian_pose)

        self.update_canvas()

    def main_loop(self):
        self._root.mainloop()

# gui = SreGui()
#
# robot = DifferentialRobot(0.1)
# gui.new_robot(robot)
#
# gui.step_gui()
# gui.main_loop()
