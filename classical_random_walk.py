import random
import numpy as np
import matplotlib.pyplot as plt
import csv
    
class randomWalk:
    def __init__(self,steps,samples=1000,bias=0):
        self.steps=steps
        self.samples=samples
        self.probability=1/2 + bias/2
        
    def finalPosition(self):
        position=0
        weight=[1 - self.probability, self.probability]
        
        for i in np.random.choice([0,1], self.steps, p=weight):
            if i==1:
                position+=1
            else:
                position-=1
                
        return position
    
    def walkData(self):
        pos_x,freq_y = [i for i in range(-self.steps,self.steps + 1)],\
                         [0 for i in range(-self.steps,self.steps + 1)]
        count=0
        while count<self.samples:
            p = self.finalPosition()
            r = p + self.steps
            freq_y[r]+=1 
            count+=1
        
        return pos_x,freq_y
    
    def walkPlot(self):
        return plt.plot(self.walkData()[0],self.walkData()[1])
    
    def exportToCSV(self, name='randomwalkdata'):
        data = [(a, x, y) for a, (x, y) in enumerate(zip(self.walkData()[0], self.walkData()[1]))]

        file = "{}.csv".format(name)

        with open(file, mode="w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(["a", "pos_x", "freq_y"])

            writer.writerows(data)

        return "Data saved to {}".format(file)
