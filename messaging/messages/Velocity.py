class Velocity:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0

    # questo è il messaggio da inviare all'orchestrator
    def get_message_string(self):
        return "MSG_VEL X=" + str(self.x) + " Y=" + str(self.y) + " T=" + str(self.theta)

