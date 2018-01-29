import numpy
import pytest
import random
import sys

class WaTor():
   def __init__(self, creatures = None, energies = None, shape = None, nfish = None, nsharks = None, age_fish=5, age_shark=10, energy_eat=3, energy_initial=0): 
      
      ok = 0
      if hasattr(creatures, 'shape'):
         if nsharks != None or nfish != None or shape != None:
            raise ValueError("Mnoho parametru")
      else:
         ok = 0
         creatures = numpy.zeros(shape)
         size0 = creatures.shape[0]
         size1 = creatures.shape[1]
            
         if nfish == None or nsharks == None or nfish > size0*size1 or nsharks > size0*size1:  
            raise ValueError("Malo parametru")
         while ok < nfish:
            ran1 = random.randint(0, size0-1) 
            ran2 = random.randint(0, size1-1) 
            if creatures[ran1,ran2] == 0: 
               creatures[ran1,ran2] = random.randint(1, age_fish)
               ok += 1
               
         ok = 0      
         while ok < nsharks:
            ran1 = random.randint(0, size0-1) 
            ran2 = random.randint(0, size1-1) 
            if creatures[ran1,ran2] == 0: 
               creatures[ran1,ran2] = -1*random.randint(1, age_shark)
               ok += 1      
      
      if hasattr(energies, 'shape'):
         if energies.shape[0] != creatures.shape[0] or energies.shape[1] != creatures.shape[1]:
            raise ValueError("Spatne rozmery")
         if energy_initial != 0:
            raise ValueError("Mnoho parametru")   
      else:
         if energy_initial == 0:
            energy_initial = 5
         energies = numpy.zeros(creatures.shape)  
         for i in range(0, creatures.shape[0]):
            for j in range(0, creatures.shape[1]):
               if creatures[i,j] < 0: 
                  energies[i,j] = energy_initial
                  
      self.energies = energies
      self.creatures = creatures
      self.age_fish = age_fish
      self.age_shark = age_shark
      self.energy_eat = energy_eat  
      self.opti = 0         
         
   def tick(self):
      energies = self.energies
      creatures = self.creatures
      
      energies = energies - 1
      creatures2 = creatures.copy()
      value = 0
      
      size0 = creatures.shape[0]
      size1 = creatures.shape[1]
      
      # Fish
      for i in range(0, creatures.shape[0]):
         for j in range(0, creatures.shape[1]):
            if creatures[i,j] <= 0:
               continue
            
            ways = 0   
            if creatures2[(i+1)%size0,j] == 0:
               ways += 1
            if creatures2[(i-1)%size0,j] == 0:
               ways += 1
            if creatures2[i,(j+1)%size1] == 0:
               ways += 1
            if creatures2[i,(j-1)%size1] == 0:
               ways += 1
               
            if ways != 0:
               if creatures[i,j] == self.age_fish:
                  value = 0
               else:
                  value = creatures[i,j] 
               while True:
                  ran = random.randint(1, 4) 
                  if ran == 1 and creatures2[(i+1)%size0,j] == 0:
                     creatures2[(i+1)%size0,j] = value + 1  
                     break
                  if ran == 2 and creatures2[(i-1)%size0,j] == 0:
                     creatures2[(i-1)%size0,j] = value + 1
                     break
                  if ran == 3 and creatures2[i,(j+1)%size1] == 0:
                     creatures2[i,(j+1)%size1] = value + 1   
                     break
                  if ran == 4 and creatures2[i,(j-1)%size1] == 0:
                     creatures2[i,(j-1)%size1] = value + 1
                     break
               if creatures[i,j] == self.age_fish:
                  creatures2[i,j] = 1
               else:
                  creatures2[i,j] = 0       
            else:
               if creatures[i,j] == self.age_fish:
                  creatures2[i,j] = self.age_fish
                  continue
               else:
                  creatures2[i,j] = creatures[i,j] + 1 
         
      creatures = creatures2.copy() 
      energies2 = energies.copy()
             
      # Sharks                                   
      for i in range(0, creatures.shape[0]):
         for j in range(0, creatures.shape[1]):
            if creatures[i,j] >= 0:  
               continue
            ways = 0   
            if creatures2[(i+1)%size0,j] > 0:
               ways += 1
            if creatures2[(i-1)%size0,j] > 0:
               ways += 1
            if creatures2[i,(j+1)%size1] > 0:
               ways += 1
            if creatures2[i,(j-1)%size1] > 0:
               ways += 1
               
            if ways != 0:  # je tam ryba
               if creatures[i,j] == -1*self.age_shark:
                  value = 0
                  creatures2[i,j] = -1
                  energies2[i,j] = energies[i,j]
               else:
                  value = creatures[i,j] 
                  creatures2[i,j] = 0      
               while True:
                  ran = random.randint(1, 4) 
                  if ran == 1 and creatures2[(i+1)%size0,j] > 0:
                     creatures2[(i+1)%size0,j] = value - 1
                     energies2[(i+1)%size0,j] = energies[i,j] + self.energy_eat
                     break
                  if ran == 2 and creatures2[(i-1)%size0,j] > 0:
                     creatures2[(i-1)%size0,j] = value - 1                                                                               
                     energies2[(i-1)%size0,j] = energies[i,j] + self.energy_eat
                     break
                  if ran == 3 and creatures2[i,(j+1)%size1] > 0:
                     creatures2[i,(j+1)%size1] = value - 1
                     energies2[i,(j+1)%size1] = energies[i,j] + self.energy_eat
                     break
                  if ran == 4 and creatures2[i,(j-1)%size1] > 0:
                     creatures2[i,(j-1)%size1] = value - 1
                     energies2[i,(j-1)%size1] = energies[i,j] + self.energy_eat
                     break
            else:      # neni tam ryba
               ways = 0   
               if creatures2[(i+1)%size0,j] == 0:
                  ways += 1 
               if creatures2[(i-1)%size0,j] == 0:
                  ways += 1
               if creatures2[i,(j+1)%size1] == 0:
                  ways += 1
               if creatures2[i,(j-1)%size1] == 0:
                  ways += 1
               
               if ways != 0:
                  if creatures[i,j] == -1*self.age_shark:
                     value = 0
                     creatures2[i,j] = -1
                     energies2[i,j] = energies[i,j]
                  else:
                     value = creatures[i,j] 
                     creatures2[i,j] = 0  
                  while True:
                     ran = random.randint(1, 4) 
                     if ran == 1 and creatures[(i+1)%size0,j] == 0:
                        creatures2[(i+1)%size0,j] = value - 1
                        energies2[(i+1)%size0,j] = energies[i,j]
                        break
                     if ran == 2 and creatures[(i-1)%size0,j] == 0:
                        creatures2[(i-1)%size0,j] = value - 1                                
                        energies2[(i-1)%size0,j] = energies[i,j]
                        break
                     if ran == 3 and creatures[i,(j+1)%size1] == 0:
                        creatures2[i,(j+1)%size1] = value - 1 
                        energies2[i,(j+1)%size1] = energies[i,j]
                        break
                     if ran == 4 and creatures[i,(j-1)%size1] == 0:
                        creatures2[i,(j-1)%size1] = value - 1                                                                   
                        energies2[i,(j-1)%size1] = energies[i,j]
                        break
               else:  # neni misto
                  if creatures[i,j] == -1*self.age_shark:
                     creatures2[i,j] = -1*self.age_shark
                     continue
                  else:
                     creatures2[i,j] = creatures[i,j] - 1
                       
      creatures = creatures2.copy()   
      energies = energies2.copy() 
      
      # Shark energy out               
      for i in range(0, creatures.shape[0]):
         for j in range(0, creatures.shape[1]):
            if creatures[i,j] < 0 and energies[i,j] == 0:
               creatures[i,j] = 0
               
      self.creatures = creatures
      self.energies = energies
      
      return self 
       
                  
   def count_fish(self):
      boolarr = self.creatures > 0
      return numpy.sum(boolarr, dtype='int16')
   
   def count_sharks(self):
      boolarr = self.creatures < 0
      return numpy.sum(boolarr, dtype='int16')
      
   def setAge_fish(self, age):
      """
      Set age of fish to breed.
      
      :param: ``age`` Age of fish.
      :rets: ``None``
      """
      
      self.age_fish = age
   
   def setAge_shark(self, age): 
      """
      Set age of shark to breed.
      
      :param: ``age`` Age of shark.
      :rets: ``None``
      """
      
      self.age_shark = age

   def setEnergy_eat(self, eat): 
      """
      Set amount of energy which shark gains after eating fish.
      
      :param: ``eat`` Amount of energy.
      :rets: ``None``
      """
      
      self.eat = eat

   def setOpti(self, sum, opti_perc):
      """
      Set amount of creatures to add for optimalize simulation.
      
      :param: ``sum`` Amount of creatures in array.
      :param: ``opti_perc`` Percentage of creatures to add.
      :rets: ``None``
      """
      
      self.opti = numpy.floor(sum*opti_perc/100) + 1


   def optimalize(self):
      """
      Makes equilibrium between species by adding creatures to array if they start to die off.
      
      :rets: ``limit_fish, limit_shark`` Amount of added creatures.
      """
   
      limit = 0

      if self.count_fish() <= self.opti:
         # Add fish
         size0 = self.creatures.shape[0]
         size1 = self.creatures.shape[1]
         limit = int(self.opti-self.count_fish())
         ran = numpy.random.random_integers(0, size0*size1-1, limit)
         ran_fish = numpy.random.randint(low=1, high=self.age_fish+1, size=limit)
         ok = 0

         while ok < limit:
            if self.creatures[int(ran[ok]/size1), ran[ok]%size1] != 0:
               ran[ok] += 1
               ran[ok] %= size0*size1
               continue
            self.creatures[int(ran[ok]/size1), ran[ok]%size1] = ran_fish[ok]
            ok += 1

      limit_fish = limit 
      limit = 0  

      if self.count_sharks() <= self.opti:
         # Add shark
         size0 = self.creatures.shape[0]
         size1 = self.creatures.shape[1]
         limit = int(self.opti-self.count_sharks())
         ran = numpy.random.random_integers(0, size0*size1-1, limit)
         ran_shark = numpy.random.randint(low=1, high=self.age_shark+1, size=limit)
         ok = 0

         while ok < limit:
            if self.creatures[int(ran[ok]/size1), ran[ok]%size1] != 0:
               ran[ok] += 1
               ran[ok] %= size0*size1
               continue
            self.creatures[int(ran[ok]/size1), ran[ok]%size1] = -1*ran_shark[ok]
            ok += 1
            
      return limit_fish, limit     



