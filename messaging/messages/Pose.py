class Pose:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0

    # questo è il messaggio che l'orchestrator manda per aggiornare la posa
    def get_message_string(self):
        return "MSG_POSE X=" + str(self.x) + " Y=" + str(self.y) + " T=" + str(self.theta)
