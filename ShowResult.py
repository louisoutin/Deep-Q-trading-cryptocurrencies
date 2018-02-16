from Coin import *
from Wallet import *
from DQNetwork import *
from Action import *


class ShowResult:
    """
        Baseline model BUY and HOLD
    """

    def __init__(self, coinName, listActions):
        self.coin = Coin(coinName)
        self.wallet = Wallet()
        self.listActions = listActions

    def applyAction(self, action, amount=None):
        if action == Action.BUY:
            self.wallet.buy(self.coin.getCurrentValue(), self.wallet.cash / self.coin.getCurrentValue())
        elif action == Action.SELL:
            self.wallet.sell(self.coin.getCurrentValue(), self.wallet.coins)

    def step(self):
        self.applyAction(self.listActions[0])
        self.listActions = self.listActions[1:]
        done, _ = self.coin.move()
        if done:
            return False
        else:
            return self.wallet.getCurrentMoney(self.coin.getCurrentValue())

