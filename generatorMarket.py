from datetime import date, timedelta

# Script which generate some hand cryptocurrency market

nameFile = "up_down_rep_BTC_EUR"

file = open("history/" + nameFile + ".csv", "w")
date = date(2000, 1, 1)
price = 50
goUp = False
file.write("Date,Open,High,Low,Close,Adj Close,Volume\n")
for i in range(200):
    file.write(str(date)+","+str(price)+",225.0,200.0,220.0,220.0,250.0""\n")
    if i % 20 == 0:
        goUp = not goUp
    if goUp:
        price += 1
    else:
        price -= 1
    date += timedelta(days=1)

file.close()
