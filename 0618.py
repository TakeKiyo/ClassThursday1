import matplotlib

import matplotlib.animation as animation


import numpy as np
import matplotlib.pyplot as plt
import random as rnd

def calcAvg(th):
    # set parameters
    N= 100
    T= 100
    W= 30
    SEED=101
    agents= []

    TH=th
    colorlist=['red', 'blue']
    averageSatisfaction=[]

    ## define functions
    def clip(x):
        if x<0:
            return(x+W)
        elif x>=W:
            return(x-W)
        else:
            return(x)


    ## define classes
    class Agent(object):

        def __init__(self,sp):
            self.x= rnd.randint(0, W-1)
            self.y= rnd.randint(0, W-1)
            self.p= sp
            self.s= 0

        def randomwalk(self):
            self.x+= rnd.randint(-1, 1)
            self.y+= rnd.randint(-1, 1)
            self.x= clip(self.x)
            self.y= clip(self.y)

        def isOverlapped(self):
            for a in agents:
                if((a.x==self.x and a.y==self.y) and (a!=self)):
                    return(True)
            return(False)

        def findNewSpace(self):
            self.randomwalk()
            if(self.isOverlapped()==True):
                self.findNewSpace()

        def updateSatisfaction(self):
            neighbors= [agent for agent in agents  if (abs(agent.x-self.x)<=1 and abs(agent.y-self.y)<=1) and agent!=self]
            neighborsCount= len(neighbors)
            sameCount= len([agent for agent in neighbors if (agent.p==self.p)])
            self.s= (float(sameCount)/float(neighborsCount) if neighborsCount!=0 else 0.0)

        def seek(self):
            self.updateSatisfaction()
            if(self.s<TH):
                self.findNewSpace()


    # initialize variables
    rnd.seed(SEED)
    agents=[Agent(i%2) for i in range(N)]
    for a in agents:
        a.findNewSpace()


    fig = plt.figure()


    # main loop (call back function for animation)
    def main_loop(t):
        step()
        # update(t)

    # events in a step
    def step():
        rnd.shuffle(agents)
        for a in agents:
            a.seek()
        averageSatisfaction.append(np.average([a.s for a in agents]))

    # update function for graph
    def update(t):
        fig.clear()
        ax1= fig.add_subplot(2, 2, 1)
        x= [a.x for a in agents]
        y= [a.y for a in agents]
        c=[colorlist[a.p] for a in agents]
        ax1.scatter(x, y, color=c)
        ax1.axis([-1, W, -1, W])
        ax1.set_title('t = ' + str(t))
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')

        ax2= fig.add_subplot(2, 2, 3)
        s= [a.s for a in agents]
        ax2.hist(s, 10)
        ax2.set_xlabel('satisfaction')
        ax2.set_ylabel('frequency')

        ax3= fig.add_subplot(2, 2, 4)
        ax3.plot(averageSatisfaction)
        ax3.set_xlabel('t')
        ax3.set_ylabel('averageSatisfaction')

        plt.tight_layout()

    for t in range(T):
        main_loop(t)
    # print(averageSatisfaction[-1])
    return averageSatisfaction[-1]
ani = animation.FuncAnimation(fig, main_loop, np.arange(0, T), interval=1, repeat=False)
plt.show()

lis = [float(x/100) for x in range(101)]
ans = []
for th in lis:
    tmp = []
    for i in range(10):
        tmp.append(calcAvg(th))
    ans.append(float(sum(tmp)/10))
    print(th)


plt.rcParams["font.size"] = 20
plt.rcParams['figure.figsize'] = 12,10

plt.plot(th, ans)
plt.xlabel("th")
plt.ylabel("satiscaction")
plt.show()
