# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:45:32 2017

@author: nawatalab
"""

import random


class Gene():
    def __init__(self, ID, a1, a2):
        self.id = ID
        self.alpha1 = a1
        self.alpha2 = a2
        self.fitness = 0
        
    def inputFitness(self, fit):
        self.fitness = fit
    
    def outputFitness(self):
        return self.fitness
    
    def outputAlpha1(self):
        return self.alpha1
    
    def outputAlpha2(self):
        return self.alpha2
    
        
    def mutation(self, probability):
        if probability > random.uniform(0, 1):
            self.alpha1 = random.uniform(0, 1)
        
        if probability > random.uniform(0, 1):
            self.alpha2 = random.uniform(0, 1)
        
        
    
  


