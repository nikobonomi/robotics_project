import tkinter as tk
import robot.TwoDRobot as Robot
from typing import List


class SreGui:
    def __init__(self, w=800, h=500):
        self._root = tk.Tk()
        self._width = w
        self._height = h
        self._canvas = tk.Canvas(self._root, width=self._width, height=self._height)
        self._canvas.pack()

        self._robots: List[Robot] = []
        self._robot = self._canvas.create_polygon(w / 2, h / 2, w / 2 + 20, h / 2, w / 2 + 10, h / 2 - 20)

        self._root.mainloop()

    def new_robot(self, robot: Robot):
        self._robots.append(robot)


gui = SreGui()
