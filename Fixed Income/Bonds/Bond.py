import numpy as np
from scipy.optimize import newton


class Bond:
    def __init__(self, face_value, maturity, coupon_rate):
        self.face_value = face_value
        self.maturity = maturity
        self.coupon_rate = coupon_rate

    def calculate_price(self, rates):
        bond_price = 0
        if not isinstance(rates, list):
            rates = [rates] * (2 * self.maturity)
        for semi_annual_counter in np.arange(0.5, self.maturity + 0.5, 0.5):
            bond_price += self.coupon_rate * self.face_value * np.exp(
                -rates[int(semi_annual_counter * 2) - 1] * semi_annual_counter)
        return bond_price + self.face_value * np.exp(-rates[2 * self.maturity - 1] * self.maturity)

    def calculate_yield(self, price, initial_guess=None):
        if initial_guess is None:
            initial_guess = 0.5 * self.coupon_rate * self.face_value / price
        return newton(lambda rates: price - self.calculate_price(rates), initial_guess)

    @staticmethod
    def annuity_price(rates, maturity=None):
        if maturity is None:
            maturity = int(len(rates) / 2)
        annuity_price = 0
        for semi_annual_counter in np.arange(0.5, maturity + 0.5, 0.5):
            annuity_price += np.exp(-rates[int(semi_annual_counter * 2) - 1] * semi_annual_counter)
        return annuity_price

    @staticmethod
    def calculate_par_yield(rates, maturity=-1):
        if maturity == -1:
            maturity = int(len(rates) / 2)
        numerator = 2 * (1 - np.exp(-rates[2 * maturity - 1] * maturity))
        denominator = Bond.annuity_price(rates, maturity)
        return numerator / denominator
