import random
import numpy as np
import matplotlib.pyplot as plt
    
class randomWalk:
    def __init__(self,steps,iterations=10):
        self.steps=steps
        self.iterations=iterations
        
    def walk(self) -> position:
        position=0
        for i in [random.randint(0,1) for j in range(self.steps)]:
            if i==1:
                position+=1
            else:
                position-=1
                
        return position
    
    def distData(self) -> position data:
        pos_x,freq_y = [i for i in range(-self.steps,self.steps + 1)],\
                         [0 for i in range(-self.steps,self.steps + 1)]
        count=0
        while count<self.iterations:
            p,r = self.walk(),p + self.steps
            freq_y[r]+=1 
            count+=1
        
        return pos_x,freq_y
    
    def distPlot(self) -> walk plot:
        return plt.plot(self.distData()[0],self.distData()[1])