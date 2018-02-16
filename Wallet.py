class Wallet:
    """
        Represent the wallet/portfolio of an agent
    """

    COINS_PER_ORDER = 5
    STARTING_CASH = 1000

    def __init__(self):
        self.coins = 0
        self.cashUsed = 0.0
        self.cash = self.STARTING_CASH

        self.returns = 0

        self.internalStateFeatures = ["isHoldingCoins"]
        self.internalState = {}

    def updateInternalState(self, currentPrice):
        """
            We update the internal state of an agent
        :param currentPrice:
        """
        self.internalState["coins"] = self.coins
        self.internalState["cash"] = self.cash
        self.internalState["currentMoney"] = self.getCurrentMoney(currentPrice)
        self.internalState["returns"] = self.returns
        self.internalState["isHoldingCoins"] = (self.coins > 0) * 1

        return self.internalState

    def getInternalState(self, currentPrice):
        self.updateInternalState(currentPrice)
        res = []
        for feature in self.internalStateFeatures:
            res.append(self.internalState[feature])
        return res

    def getCurrentMoney(self, currentPrice):
        """
            Total amount of agent's money.

            :param currentPrice:
        """
        return self.coins * currentPrice + self.cash

    def getSizeInternalState(self):
        return len(self.internalStateFeatures)

    def getProfitsPercents(self, total):
        return total / self.STARTING_CASH * 100

    def getReturnRate(self, currentPrice):
        """
            A profit on an investment over a period of time,
            expressed as a proportion of the original investment

            :param currentPrice:
        """
        return 100 * (self.getCurrentMoney(currentPrice) - self.STARTING_CASH) / self.STARTING_CASH

    def buy(self, currentPrice, coinsToBuy=None):
        """
            Change cash to coin for the current price
            :param currentPrice:
        """
        if coinsToBuy is None:
            amount = self.COINS_PER_ORDER
        else:
            amount = coinsToBuy

        price = amount * currentPrice

        if self.cash + 0.00001 >= price:
            self.coins += amount
            self.cash -= price
            self.cashUsed += price

    def sell(self, currentPrice, coinsToSell=None):
        """
            Change coin to cash for the current price
            :param coinsToSell:
            :param currentPrice:
        """
        if coinsToSell is None:
            amount = self.COINS_PER_ORDER
        else:
            amount = coinsToSell
        if self.coins + 0.00001 >= amount:
            self.coins -= amount
            self.cash += amount * currentPrice

    def reset(self):
        """
            Reset the wallet
        """
        self.coins = 0
        self.cash = self.STARTING_CASH
        self.cashUsed = 0.0
        self.returns = 0


if __name__ == "__main__":
    w = Wallet()
    w.coins = 1.2
    print(w.getCurrentMoney(50))
    print(w.getReturnRate(5000))
