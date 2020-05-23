class TwoDPose:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0

    def from_message(self, message):
        # esempio: MSG_VEL X=0.3 Y=0.4 T=0
        data = message.split(" ")
        if data[0] != "MSG_POSE":
            return
        vel_left = data[1].split("=")[1]
        vel_right = data[2].split("=")[1]

    # questo è il messaggio che l'orchestrator manda per aggiornare la posa
    def get_message_string(self):
        return "MSG_POSE X=" + str(self.x) + " Y=" + str(self.y) + " T=" + str(self.theta)
