from Bond import Bond
import numpy as np


class ZeroBond(Bond):
    def __init__(self, face_value, maturity):
        super(ZeroBond, self).__init__(face_value, maturity, 0)

    def calculate_price(self, rates):
        return self.face_value * np.exp(-rates[2 * self.maturity - 1] * self.maturity)

