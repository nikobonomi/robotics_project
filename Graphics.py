import math
import tkinter as tk
import robot.TwoDRobot as Robot
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

        self._robots: Dict[Robot] = {}
        self._sensors: Dict[Sensor] = {}
        # self._robot = self._canvas.create_polygon(w / 2, h / 2, w / 2 + 20, h / 2, w / 2 + 10, h / 2 - 20)
        self.update_canvas()

    def new_robot(self, robot: Robot):
        self._robots[robot] = self._canvas.create_polygon(robot.get_robot_draw_points())
        for sensor in robot.sensors:
            self.new_sensor(sensor)
        self.update_canvas()

    def new_sensor(self, sensor: Sensor):
        self._sensors[sensor] = self._canvas.create_polygon(sensor.vertexes, fill="red")
        self.update_canvas()

    def draw_axis(self):
        # disegno gli assi
        self._canvas.create_line(0, 0, 100, 0, width=1, fill='red', dash=(4, 2))
        self._canvas.create_line(0, 0, 0, 100, width=1, fill='green', dash=(4, 2))

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

    def step_gui(self):

        for robot in self._robots.keys():
            cartesian_pose = robot.get_cartesian_pose()
            # calcolo la rotazione del robot all'origine
            points = self.rotate(robot.get_robot_draw_points(), cartesian_pose.theta)
            # points = robot.get_robot_draw_points()
            # porto il robot all'origine con i punti ruotati
            self._canvas.coords(self._robots[robot], points)
            # lo muovo al posto giusto
            self._canvas.move(self._robots[robot], cartesian_pose.x, cartesian_pose.y)

            # aggiorno la posizione dei sensori
            for sensor in robot.sensors:
                widget: List[int] = self._sensors[sensor]

                points = self.rotate(sensor.vertexes, cartesian_pose.theta)
                self._canvas.coords(widget, points)
                self._canvas.move(widget, cartesian_pose.x, cartesian_pose.y)

            # # cerco un sensore
            # # vertex, widget = self._sensors[robot]
            # # if vertex is not None:
            #     # calcolo la rotazione del robot all'origine
            #     points = self.rotate(vertexes, cartesian_pose.theta)
            #     # points = robot.get_robot_draw_points()
            #     # porto il robot all'origine con i punti ruotati
            #     self._canvas.coords(widget, points)
            #     # lo muovo al posto giusto
            #     self._canvas.move(widget, cartesian_pose.x, cartesian_pose.y)

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
