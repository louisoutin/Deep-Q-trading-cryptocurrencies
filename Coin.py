import pandas as pd
from stockstats import *
import matplotlib.pyplot as plt
import numpy as np

class Coin:
    """
        Represent the market of a cryptocurrency over a period
    """
    NumPastDays = 200
    def __init__(self, coinName="ethereum"):
        self.coinName = coinName

        dataSet = pd.read_csv("history/" + self.coinName + ".csv", parse_dates=["Date"])
        dataSet.index = dataSet.sort_values(by=['Date']).index
        dataSet = dataSet.sort_index()
        self.dataSet = StockDataFrame.retype(dataSet)

        self.length = len(self.dataSet)
        self.currentIndex = self.NumPastDays+1
        self.externalStateFeatures = ["currentPrice"]
        self.externalState = {}
        self.updateExternalState()

    def updateExternalState(self):
        self.externalState["currentPrice"] = self.getCurrentValue()
        self.externalState["macd"] = self.dataSet['macd'][self.currentIndex]
        self.externalState["crossUpBand"] = self.crossingUpperBand()
        self.externalState["crossDownBand"] = self.crossingLowerBand()
        self.externalState['boll_ub'] = self.dataSet['boll_ub'][self.currentIndex]
        self.externalState['boll_lb'] = self.dataSet['boll_lb'][self.currentIndex]
        # add more
        return self.externalState

    def getExternalState(self):
        return self.getDeltaValues()

    def getSizeExternalState(self):
        return self.NumPastDays

    def getCurrentValue(self):
        return self.dataSet["open"][self.currentIndex]

    def getState(data, t, n):
        print(data, t, n)
        d = t - n + 1
        block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1]  # pad with t0
        res = []
        for i in xrange(n - 1):
            res.append(sigmoid(block[i + 1] - block[i]))

        print([res])
        return np.array([res])

    def sigmoid(self,x):
        import math
        # Prevent overflow
        x = np.float(x)
        ans = np.float(1 / (1 + math.exp(-x*0.2)))
        return ans

    def getDeltaValues(self):
        n = self.NumPastDays
        deltas = []
        for i in range(n):
            if self.currentIndex-(i+1) < 0:
                delta = 0.5
            else:
                currentValue = self.dataSet["open"][self.currentIndex-i]
                previousValue = self.dataSet["open"][self.currentIndex-(i+1)]
                delta = self.sigmoid(currentValue - previousValue)
            deltas.append(delta)
        return deltas

    def getValueAt(self, t):
        """
            Return the value of dataSet "OPEN" key at day "t"

            :param t: day "t"
        """
        if t >= self.length:
            return self.dataSet["open"][self.length - 1]
        if t < 0:
            return self.dataSet["open"][0]
        return self.dataSet["open"][t]

    def getNextValue(self):
        """
            Return the NEXT value of dataSet "OPEN" key if exists
        """
        if self.currentIndex + 1 >= self.length:
            return None
        return self.dataSet["open"][self.currentIndex + 1]

    def getPreviousValue(self):
        """
            Return the PREVIOUS value of dataSet "OPEN" key if exists
        """
        if self.currentIndex - 1 < 0:
            return None
        return self.dataSet["open"][self.currentIndex - 1]

    def move(self):
        """
            Return : True if we come to the last data as well as the current external state
                False otherwise
        """
        if self.currentIndex + 1 >= self.length:
            return True, self.getExternalState()
        else:
            self.currentIndex += 1
            self.updateExternalState()
            return False, self.getExternalState()

    def crossingUpperBand(self):
        if self.currentIndex == 0:
            return 0

        return 1 * (
                self.currentIndex - 1 >= 0
                and self.dataSet['boll_ub'][self.currentIndex - 1] <= self.getCurrentValue()
                and self.dataSet['boll_ub'][self.currentIndex] > self.getCurrentValue()
        )

    def crossingLowerBand(self):
        if self.currentIndex == 0:
            return 0

        return 1 * (
                self.currentIndex - 1 >= 0
                and self.dataSet['boll_lb'][self.currentIndex - 1] >= self.getCurrentValue()
                and self.dataSet['boll_lb'][self.currentIndex] < self.getCurrentValue()
        )

    def plot(self):
        """
            Display some features.
        """
        t = [i for i in range(self.length)]
        plt.plot(t, self.dataSet["open"])
        plt.plot(t, self.dataSet["macd"])
        plt.plot(t, self.dataSet["boll_lb"])
        plt.plot(t, self.dataSet["boll_ub"])
        plt.show()

    def getReward(self):
        return self.cummulatedWealth(100)

    def dailyProfit(self, action):
        """
            Instantaneous reward : (current price of the target) - (price day - 1)
        """
        a = None
        if action.value == 0:
            a = 0
        if action.value == 1:
            a = 1
        if action.value == 2:
            a = -1

        return a * ( self.getCurrentValue() - self.getPreviousValue() )

    def cummulatedWealth(self, n=5):
        """
            Reward function which maximize the long-term profit (good candidate for deep Q-trading)

            :param action:
            :param n: "n" days
            :return:
        """
        t = self.getCurrentValue()
        t_minus_1 = self.getValueAt(self.currentIndex - 1)
        t_minus_n = self.getValueAt(self.currentIndex - n)

        res1 = (1 + (1) * (t - t_minus_1) / t_minus_1) * t_minus_1 / t_minus_n
        res2 = (1 + (-1) * (t - t_minus_1) / t_minus_1) * t_minus_1 / t_minus_n
        res0 = (1 + (0) * (t - t_minus_1) / t_minus_1) * t_minus_1 / t_minus_n

        return (res0,res1,res2)

    def reset(self):
        """
            Reset the index and external states
        """
        self.currentIndex = self.NumPastDays+1
        self.updateExternalState()


if __name__ == "__main__":
    ethCoin = Coin("train_BTC_EUR_2011_2014")
    # print(ethCoin.dataSet)
    #
    # print("\n************\n")
    # k = 0
    # for i in range(982):
    #     print("\n***** Nouvelle itération *******\n")
    #     print("Current value", ethCoin.getCurrentValue())
    #     print(ethCoin.move())
    #     if ethCoin.crossingLowerBand() == True or ethCoin.crossingUpperBand() == True:
    #         k += 1
    # print(k)
    #
    # ethCoin.plot()

    ethCoin.currentIndex = ethCoin.NumPastDays
    print(ethCoin.getCurrentValue())
    print(ethCoin.getDeltaValues())
    ethCoin.move()
    print(ethCoin.getDeltaValues())
