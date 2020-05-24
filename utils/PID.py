class PID:

    def __init__(self, freq, p=0, i=0, d=0, ):
        self.p = p
        self.i = i
        self.d = d
        self.last_e = None
        self.sum_e = 0
        self.dt = 1.0 / freq  # freq is on Hz, so d1 is 1sec / freq

    def compute_derivative(self, error):
        if self.last_e is not None:
            return (error - self.last_e) / self.dt
        else:
            return 0

    def compute(self, error):

        derivative = self.compute_derivative(error)  # compute the derivative for the current step

        self.last_e = error
        self.sum_e += error * derivative

        return self.p * error + self.d * derivative + self.i * self.sum_e
