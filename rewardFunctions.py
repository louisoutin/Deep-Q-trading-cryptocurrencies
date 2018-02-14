def accumulatedWealth(action):
    a = Action.

    price_t = self.getCurrentValue()
    price_t_minus_1 = self.getValueAt(self.currentIndex - 1)
    price_t_minus_n = self.getValueAt(self.currentIndex - 10)

    r = (1 + a * (price_t - price_t_minus_1) / price_t_minus_1) * price_t_minus_1 / price_t_minus_n

    return r

def dailyProfit():

