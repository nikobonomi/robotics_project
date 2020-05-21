import time


# classe che aiuta a mantenere un ciclo di aggiornamenti costante
class RateKeeper:
    def __init__(self, hz):
        self.sleep_duration = 1000/hz
        self.last_run_ms = RateKeeper.get_current_ts()

    @staticmethod
    def get_current_ts():
        return int(round(time.time() * 1000))

    def wait_cycle(self):
        # calcolo la differenza dall'ultima esecuzione a quella corrente
        difference = RateKeeper.get_current_ts() - self.last_run_ms
        # calcolo il tempo rimanente da aspettare
        wait_time = self.sleep_duration-difference

        # se c'è del tempo da aspettare aspetto
        if wait_time > 0 :
            time.sleep(wait_time/1000)

        self.last_run_ms = RateKeeper.get_current_ts()
