AUTEUR : LOUIS OUTIN et MARWAN LAKRADI // M2 Informatique Caen, projet annuel.

DEEP Q LEARNING APPLIED TO CRYPTOCURRENCIES TRADING.

Requirements:

- Python 3.5
- Numpy
- Tensorflow and Keras
- Pandas
- stockstats (not used in the model but present in the code for trying different strategies)

For installing theses dependencies, you can simply use pip in your terminal.

Content of the code:

- Action:
	Enum class containing the 3 actions
- BuyAndHold:
	Class who preform the Buy and Hold strategie given a Coin and Wallet object.
- Coin:
	Class loading a history csv file to transform it into usable data by the agent and interactive to move forward over days.

- DQNetwork:
	Class containing the Keras model of the neural network and the main methods of the Deep Q learning algorithm.

- generatorMarket:
	Script to generate simple stock market models to experiment easy tests.
- ShowResult:
	Show the difference between a given list of actions and the buy and hold strategy.
- TraderAgent:
	Main class containing the trading algorithm (training or testing mode or both)
- Wallet:
	Class representing the agent's money and provide method to interact with the market.

Running instructions.

1) Download the .csv file of the market you want to trade on and split it into trainning set and testing set.
2) Set the coinName and the nameModel of the TraderAgent in the TraderAgent.py file.
Exemple : t = TraderAgent("test_ETH_USD", 'model_ETH_USD.h5')
	  -> Will load the testing dataset with the model corresponding to it

3) Run it as "python3 TraderAgent.py" 

For Trainning it takes about 1-2hours to get good result and for the Testing with Online learning, it should be around 3-5minute depending on the test dataset size too.

