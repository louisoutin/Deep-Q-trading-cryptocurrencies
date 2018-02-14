from Coin import *
from Wallet import *
from DQNetwork import *
from Action import *


class BuyAndHold:



    def __init__(self, coinName="ethereum"):
        self.coin = Coin(coinName)
        self.wallet = Wallet()

    def applyAction(self, action, amount=None):
        if action == Action.BUY:
            self.wallet.buy(self.coin.getCurrentValue(), amount)
        elif action == Action.SELL:
            self.wallet.sell(self.coin.getCurrentValue(), amount)

    def test(self):
        self.coin.reset()
        self.wallet.reset()
        print(self.wallet.cash,self.coin.getCurrentValue())
        self.applyAction(Action.BUY,np.float(self.wallet.cash)/np.float(self.coin.getCurrentValue()))

        while (True):
            isDone, nextExternalState = self.coin.move()
            self.applyAction(Action.HOLD)


            if isDone:
                cum_return = self.wallet.getReturnRate(self.coin.getCurrentValue())
                print("return :", self.wallet.getReturnRate(self.coin.getCurrentValue()))
                print("Cash :", self.wallet.cash)
                print("Coin :", self.wallet.coins)
                print("cash used :", self.wallet.cashUsed)
                print("Final total money :", self.wallet.getCurrentMoney(self.coin.getCurrentValue()))
                print("Percentage Profit :", self.wallet.getProfitsPercents(self.wallet.getCurrentMoney(self.coin.getCurrentValue())))

                break


if __name__ == "__main__":
    t = BuyAndHold("test_HSI")
    t.test()


    # ajouter cash total (transformed coins) a la fin
    # ajouter le pourcentage de fait
    # --> Basline model BUY and HOLD
