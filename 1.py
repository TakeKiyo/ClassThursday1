# 課題提出用
import matplotlib.pyplot as plt

#図の大きさとフォントサイズを設定
plt.rcParams["font.size"] = 20
plt.rcParams['figure.figsize'] = 12,10
def do_logistic_growth(k, r, n0, t):
    nt= n0
    datax=[]
    datay=[]

    datax.append(0)
    datay.append(nt)

    for i in range(t):
        nt= nt+r*nt*(1.0-nt/k)
        datax.append(i+1)
        datay.append(nt)

    return(datax, datay)
dataX, dataY= do_logistic_growth(100.0, 1.88 , 1.0, 20)
plt.plot(dataX, dataY,label=str(i))
dataX, dataY= do_logistic_growth(100.0, 1.96 , 1.0, 20)
plt.plot(dataX, dataY,label=str(i))
dataX, dataY= do_logistic_growth(100.0, 2.74 , 1.0, 20)
plt.plot(dataX, dataY)
plt.xlabel("time")
plt.ylabel("population size")
plt.show()
