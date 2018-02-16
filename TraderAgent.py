from Coin import *
from Wallet import *
from DQNetwork import *
from Action import *
import pylab as plb


class TraderAgent:

    def __init__(self, coinName, nameModel):
        self.nameModel = nameModel
        self.coin = Coin(coinName)
        self.wallet = Wallet()
        self.brain = DQNetwork(self.getSizeState(), len(Action))

    def getSizeState(self):
        return self.coin.getSizeExternalState()

    def getCurrentState(self):
        """
            Return a list of value which represent a state
                state = [ internalState, externalState ]
                state = [ "coins", "cash", "currentMoney", "returns",
                            "currentPrice", "macd", "crossUpBand", "crossDownBand", "boll_ub", "boll_lb"]
        """
        currentPrice = self.coin.getCurrentValue()
        internalState = self.wallet.updateInternalState(currentPrice)
        externalState = self.coin.getExternalState()
        return externalState

    def applyAction(self, action, amount=None):
        if action == Action.BUY:
            self.wallet.buy(self.coin.getCurrentValue(), self.wallet.cash / self.coin.getCurrentValue())
        elif action == Action.SELL:
            self.wallet.sell(self.coin.getCurrentValue(), self.wallet.coins)

    def train(self, epoch):
        for i in range(epoch):
            self.coin.reset()
            self.wallet.reset()
            state = self.getCurrentState()
            f = open('log.txt', 'a')
            while True:
                action = self.brain.act(state)

                self.applyAction(Action(np.argmax(action)))

                isDone, nextExternalState = self.coin.move()  # One step ahead (CurrentValue += 1)
                # nextState = self.wallet.getInternalState(self.coin.getCurrentValue()) + nextExternalState
                nextState = nextExternalState
                rewards = self.coin.getReward()
                # print("rewards : ", rewards)
                self.brain.remember(state, rewards, nextState, isDone)
                state = nextState

                if isDone:
                    self.brain.updateTargetModel()

                    cum_return = self.wallet.getReturnRate(self.coin.getCurrentValue())
                    print("episode: {}/{}, returns: {}, epsilon: {:.2}"
                          .format(i + 1, epoch,
                                  cum_return,
                                  self.brain.epsilon))
                    # print("Next value :", self.coin.getNextValue())
                    print("Action :", action, np.argmax(action), Action(np.argmax(action)))
                    print("Cash :", self.wallet.cash)
                    print("Cash USED :", self.wallet.cashUsed)
                    print("Coin :", self.wallet.coins)

                    f.write("episode: {}/{}, returns: {}, epsilon: {:.2}"
                            .format(i + 1, epoch,
                                    cum_return,
                                    self.brain.epsilon) + "\n")
                    break
            if len(self.brain.memory) > self.brain.batch_size:
                self.brain.replay()
            if i % 10 == 0:
                self.brain.save(self.nameModel)
        self.brain.save(self.nameModel)

    def test(self):

        self.brain.targetModel = t.brain.build_online_model()
        self.brain.load(self.nameModel)

        self.brain.memory = deque(maxlen=64)

        self.coin.reset()
        self.wallet.reset()
        state = self.getCurrentState()
        print(state)
        listActions = []
        lastAction = 0
        while True:
            action = self.brain.act(state)

            self.applyAction(Action(np.argmax(action)))
            # print(Action(np.argmax(action)))
            listActions.append(Action(np.argmax(action)))
            isDone, nextExternalState = self.coin.move()
            # nextState = self.wallet.getInternalState(self.coin.getCurrentValue()) + nextExternalState

            rewards = self.coin.getReward(lastAction)
            nextState = nextExternalState
            self.brain.remember(state, rewards, nextState, isDone)

            self.brain.onlineLearning()

            lastAction = np.argmax(action)
            state = nextState

            if isDone:
                returnRate = self.wallet.getReturnRate(self.coin.getCurrentValue())
                print("Return rate :", returnRate)
                print("Cash :", self.wallet.cash)
                print("Coin :", self.wallet.coins)
                print("Final total money :", self.wallet.getCurrentMoney(self.coin.getCurrentValue()))
                print("Percentage Profit :",
                      self.wallet.getProfitsPercents(self.wallet.getCurrentMoney(self.coin.getCurrentValue())))

                return listActions

    def plotActions(self, listActions):

        xBUY = [i for i in range(len(self.coin.dataSet["open"]) - self.coin.NumPastDays - 1) if
                listActions[i] == Action.BUY]
        yBUY = [self.coin.dataSet["open"][i] for i in range(self.coin.NumPastDays, len(self.coin.dataSet["open"]) - 1)
                if listActions[i - self.coin.NumPastDays] == Action.BUY]

        xSELL = [i for i in range(len(self.coin.dataSet["open"]) - self.coin.NumPastDays - 1) if
                 listActions[i] == Action.SELL]
        ySELL = [self.coin.dataSet["open"][i] for i in range(self.coin.NumPastDays, len(self.coin.dataSet["open"]) - 1)
                 if listActions[i - self.coin.NumPastDays] == Action.SELL]

        xHOLD = [i for i in range(len(self.coin.dataSet["open"]) - self.coin.NumPastDays - 1) if
                 listActions[i] == Action.HOLD]
        yHOLD = [self.coin.dataSet["open"][i] for i in range(self.coin.NumPastDays, len(self.coin.dataSet["open"]) - 1)
                 if listActions[i - self.coin.NumPastDays] == Action.HOLD]

        plb.plot(xBUY, yBUY, 'bo', label="Buy")
        plb.plot(xSELL, ySELL, 'ro', label="Sell")
        plb.plot(xHOLD, yHOLD, 'yo', label="Hold")

        plb.legend(loc='upper right')

        plb.show()


if __name__ == "__main__":
    t = TraderAgent("test_HSI", 'modelHSI_2000.h5')

    # t.brain.load("modelDropout.h5")
    # t.train(2000)

    listActions = t.test()
    t.plotActions(listActions)

# ModelHSI 200 contre 150 (buy n hold) 200 epochs (only one dropout 0.25 between 1st and 2nd hidden layers)
# 0.0001 train lr, 0.0005 test online learning
