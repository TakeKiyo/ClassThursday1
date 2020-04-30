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

bifX = []
bifY = []
lis_r = [i/100 for i in range(100,301,1)]
for r in lis_r:
    dataX, dataY= do_logistic_growth(100.0, r, 1.0, 300)
    bifX += [r]*50
    bifY +=dataY[251:301]
plt.plot(bifX, bifY,'.')

plt.xlabel("r")
plt.ylabel("population size")
plt.show()
