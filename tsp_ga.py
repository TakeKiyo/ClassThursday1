import matplotlib.pyplot as plt
 
#for Canopy users
import matplotlib.animation as animation
 
#for EPD users
#matplotlib.use('TkAgg')  
 
import math
import numpy as np
import matplotlib.pyplot as plt
import random as rnd
 
 
 
CoordinateX = [37,49,52,20,40,21,17,31,52,51,42,31,5,12,36,52,27,17,13,57,62,42,
16,8,7,27,30,43,58,58,37,38,46,61,62,63,32,45,59,5,10,21,5,30,39,32,25,25,48,56,30]
CoordinateY = [52,49,64,26,30,47,63,62,33,21,41,32,25,42,16,41,23,33,13,58,42,57,57,52,
38,68,48,67,48,27,69,46,10,33,63,69,22,35,15,6,17,10,64,15,10,39,32,55,28,37,40]
L = len(CoordinateX)

def gtypeToPtype(gtype):
    dist = 0;
    for i in range(L-1):
        dist += math.sqrt(pow((CoordinateX[gtype[i+1]]-CoordinateX[gtype[i]]),2)+pow((CoordinateY[gtype[i+1]]-CoordinateY[gtype[i]]),2))
    dist += math.sqrt(pow((CoordinateX[gtype[L-1]]-CoordinateX[gtype[0]]),2)+pow((CoordinateY[gtype[L-1]]-CoordinateY[gtype[0]]),2))
    return(dist)
    
def fitnessFunction(p):
    return(p)
 

   
## define classes
class Agent(object):
     
    def __init__(self, gtype):
        self.genotype= gtype[:]
        self.phenotype= None
        self.fitness= 0
   
    def getOffspring(self):
        o = Agent(self.genotype)
   
        for i in range(L):
            if (rnd.random()<MUT):
                firstIdx = rnd.randint(0,L-1)
                secondIdx = rnd.randint(0,L-1)
                while firstIdx == secondIdx:
                    secondIdx = rnd.randint(0,L-1)   
                tmp = o.genotype[firstIdx]
                o.genotype[firstIdx] = o.genotype[secondIdx]
                o.genotype[secondIdx] = tmp
                  
        return(o)
  
    def develop(self, dfunc):
        self.phenotype= dfunc(self.genotype)
  
    def evaluate(self, efunc):
        self.fitness= efunc(self.phenotype)
         
 
def selectAnAgentByRoulette(pop):
    total= sum([i.fitness for i in pop])
    val= rnd.random()*total
    for i in pop:
        val-= i.fitness
        if (val<0):
            return(i)
    
def selectAnAgentByTournament(pop):
    leng = len(pop)

    # 2つを選んで，適応度の小さいほうを使用
    # firstIdx = rnd.randint(0,leng-1)
    # secondIdx = rnd.randint(0,leng-1)
    # while firstIdx == secondIdx:
    #     secondIdx = rnd.randint(0,leng-1)  
    # if pop[firstIdx].fitness < pop[secondIdx].fitness:
    #     return pop[firstIdx]
    # else:
    #     return pop[secondIdx]

    # 10個選んで，適応度の一番小さいpopを返す
    dic = {}
    for i in range(10):
        Idx = rnd.randint(0,leng-1)
        dic[Idx] = pop[Idx].fitness
    dic2 = sorted(dic.items(), key=lambda x:x[1])       
    return pop[dic2[0][0]]
   
def crossover(a1, a2):
    tmp1 = rnd.randint(1, L-1)
    tmp2 = rnd.randint(1, L-1)
    maxPoint = max(tmp1,tmp2)
    point= min(tmp1,tmp2)
    for i in range(point, maxPoint):
        a1.genotype[i], a2.genotype[i]= a2.genotype[i], a1.genotype[i]
    a1_sub = a1.genotype[point:maxPoint]
    a2_sub = a2.genotype[point:maxPoint]
    rest_a1 = list(set(range(L))-set(a1.genotype))
    rest_a2 = list(set(range(L))-set(a2.genotype))
    rnd.shuffle(rest_a1)
    rnd.shuffle(rest_a2)
    for i in range(point):
        if a1.genotype[i] not in a1_sub:
            pass
        else:
            a1.genotype[i] =rest_a1[0]
            rest_a1.pop(0)
        if a2.genotype[i] not in a2_sub:
            pass
        else:
            a2.genotype[i] =rest_a2[0]
            rest_a2.pop(0)
    for i in range(maxPoint,L):
        if a1.genotype[i] not in a1_sub:
            pass
        else:
            a1.genotype[i] =rest_a1[0]
            rest_a1.pop(0)
        if a2.genotype[i] not in a2_sub:
            pass
        else:
            a2.genotype[i] =rest_a2[0]
            rest_a2.pop(0)


  
  
  
# initialize variables
SEED=101
T=100
N= 30
G= 100
# L= 20
MUT= 0.02
CROSS= 0.2
rnd.seed(SEED)
tmpList = list(range(L))
population= [Agent(rnd.sample(tmpList,len(tmpList))) for i in range(N)]
fig= plt.figure()
   
#some variables for graphs
averageFitness= []
bestFitness= []
best= population[0]
pp= []
pf= []
 
# main loop (call back function for animation)
def main_loop(t):
    step()
    update(t)
 
# events in a step
def step():
    global population, tmpX,tmpY
    #fitness evaluation
    best= population[0]
    for a in population:
        a.develop(gtypeToPtype)
        a.evaluate(fitnessFunction)
        if(a.fitness < best.fitness):
            best= a
    averageFitness.append(np.average([a.fitness for a in population]))
    bestFitness.append(best.fitness)     
    

    tmpX = []
    tmpY = [] 
    for i in range(L):
        tmpX.append(CoordinateX[best.genotype[i]])
        tmpY.append(CoordinateY[best.genotype[i]]) 
    tmpX.append(CoordinateX[best.genotype[0]])
    tmpY.append(CoordinateY[best.genotype[0]]) 

                         
 
    print(str(best.genotype)+":"+str(best.fitness))
    #evolution
    newpop= []
    for i in range(int(N/2)):
        n1= selectAnAgentByTournament(population).getOffspring()
        n2= selectAnAgentByTournament(population).getOffspring()
 
        if rnd.random()<CROSS:
            crossover(n1, n2)
        newpop.append(n1)
        newpop.append(n2)
     
    population = newpop
         
# update function for graph
def update(t):
    fig.clear()
      
    ax1= fig.add_subplot(2, 1, 1)
    ax1.plot(averageFitness)
    ax1.set_title('g = ' + str(t))
    ax1.plot(bestFitness)
    ax1.set_xlabel("generaiton")
    ax1.set_ylabel("average / best fitness")    

    ax2= fig.add_subplot(2, 1, 2)
    ax2.plot(CoordinateX, CoordinateY,'.')
    ax2.plot(tmpX, tmpY)
    ax2.set_ylabel("fitness")
 
    fig.tight_layout()
     
     
ani = animation.FuncAnimation(fig, main_loop, np.arange(0, T), interval=25, repeat=False)
plt.show()
