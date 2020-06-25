import matplotlib

import matplotlib.animation as animation


import numpy as np
import matplotlib.pyplot as plt
import random as rnd


# set parameters
N= 100
T= 100
W= 30
SEED=101
agents= []
PR = 0.03
PI = 0.5

TH=0.3
colorlist=['blue','red','green','orange']
averageSatisfaction=[]
sList = []
iList = []
rList = []
eList = []

## define functions
def clip(x):
    if x<0:
        return(x+W)
    elif x>=W:
        return(x-W)
    else:
        return(x)

#p:0=>s p:1=>i p:2=>r p:2=>e(自覚症状なし)

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
        if self.p==1:
            if rnd.random() <= 0.3:
                self.randomwalk()
                if(self.isOverlapped()==True):
                    self.findNewSpace()
        else:
            self.randomwalk()
            if(self.isOverlapped()==True):
                self.findNewSpace()


    def getInfected(self):
        if self.p == 0:
            if rnd.random() <= 0.2:
                self.p = 1
            else:
                self.p = 3

    def updateInfected(self):
        neighbors= [agent for agent in agents  if (abs(agent.x-self.x)<=1 and abs(agent.y-self.y)<=1) and agent!=self]
        neighborsCount= len(neighbors)
        if self.p == 1 or self.p == 3:
            for agent in neighbors:
                if rnd.random() <= PI:
                    agent.getInfected()
        if self.p == 1:
            if rnd.random() <= PR:
                self.p = 2
        if self.p == 3:
            if rnd.random() <= 0.3:
                self.p = 1

    def getCondition(self):
        return self.p

    def seek(self):
        self.updateInfected()
        self.findNewSpace()


# initialize variables
rnd.seed(SEED)
agents=[Agent(0) for i in range(N)]
agents.append(Agent(1))
print(agents)
for a in agents:
    a.findNewSpace()


fig = plt.figure()


# main loop (call back function for animation)
def main_loop(t):
    step()
    update(t)
    # print(sList)

# events in a step
def step():
    rnd.shuffle(agents)
    sCnt = 0
    iCnt = 0
    rCnt = 0
    eCnt = 0
    for a in agents:
        a.seek()
        if a.getCondition() == 0:
            sCnt += 1
        elif a.getCondition() == 1:
            iCnt += 1
        elif a.getCondition()==2:
            rCnt += 1
        else:
            eCnt += 1
    averageSatisfaction.append(np.average([a.s for a in agents]))
    sList.append(sCnt)
    iList.append(iCnt)
    rList.append(rCnt)
    eList.append(eCnt)

# update function for graph
def update(t):
    fig.clear()
    ax1= fig.add_subplot(2, 3, 1)
    x= [a.x for a in agents]
    y= [a.y for a in agents]
    c=[colorlist[a.p] for a in agents]
    ax1.scatter(x, y, color=c)
    ax1.axis([-1, W, -1, W])
    ax1.set_title('t = ' + str(t))
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')

    ax2= fig.add_subplot(2, 3, 2)
    ax2.plot(sList)
    ax2.set_xlabel('t')
    ax2.set_ylabel('susceptible')

    ax3= fig.add_subplot(2, 3, 3)
    ax3.plot(iList)
    ax3.set_xlabel('t')
    ax3.set_ylabel('infected')

    ax4= fig.add_subplot(2, 3, 4)
    ax4.plot(rList)
    ax4.set_xlabel('t')
    ax4.set_ylabel('recovered')

    ax5= fig.add_subplot(2, 3, 5)
    ax5.plot(eList)
    ax5.set_xlabel('t')
    ax5.set_ylabel('exposed')

    plt.tight_layout()

ani = animation.FuncAnimation(fig, main_loop, np.arange(0, T), interval=1, repeat=False)
plt.show()
