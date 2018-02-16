from Coin import *
from Wallet import *
from DQNetwork import *
from Action import *


class BuyAndHold:
    """
        Baseline model BUY and HOLD
    """

    def __init__(self, coinName):
        self.coin = Coin(coinName)
        self.wallet = Wallet()
        self.bought = False

    def applyAction(self, action, amount=None):
        if action == Action.BUY:
            self.wallet.buy(self.coin.getCurrentValue(), self.wallet.cash / self.coin.getCurrentValue())

    def step(self):
        if not self.bought:
            self.applyAction(Action.BUY)
            self.bought = True
        else:
            self.applyAction(Action.HOLD)
        done, _ = self.coin.move()
        if done:
            return False
        else:
            return self.wallet.getCurrentMoney(self.coin.getCurrentValue())

    def test(self):
        self.coin.reset()
        self.wallet.reset()

        all_in = np.float(self.wallet.cash) / np.float(self.coin.getCurrentValue())
        self.applyAction(Action.BUY, all_in)

        while True:
            isDone, nextExternalState = self.coin.move()
            self.applyAction(Action.HOLD)

            if isDone:
                cum_return = self.wallet.getReturnRate(self.coin.getCurrentValue())
                print("return :", cum_return)
                print("Cash :", self.wallet.cash)
                print("Coin :", self.wallet.coins)
                print("cash used :", self.wallet.cashUsed)
                print("Final total money :", self.wallet.getCurrentMoney(self.coin.getCurrentValue()))
                print("Percentage Profit :",
                      self.wallet.getProfitsPercents(self.wallet.getCurrentMoney(self.coin.getCurrentValue())))
                break


if __name__ == "__main__":
    t = BuyAndHold("test_HSI")
    t.test()
