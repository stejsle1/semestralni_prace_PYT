import numpy
import pytest
import cython
import sys
cimport numpy
import random

class WaTor():

   def __init__(self, creatures = None, numpy.ndarray[numpy.float64_t, ndim=2] energies = None, tuple shape = None, numpy.int64_t nfish = -1, numpy.int64_t nsharks = -1, numpy.int64_t age_fish=5, numpy.int64_t age_shark=10, numpy.int64_t energy_eat=3, numpy.int64_t energy_initial=0): 
   
      """
      Init WaTor instance
      
      :param: ``creatures`` Array of creatures with theirs age
      :param: ``energies`` Array of energies of sharks
      :param: ``shape`` Size of array   
      :param: ``nfish`` Number of fish in array
      :param: ``nsharks`` Number of sharks in array
      :param: ``age_fish`` Age of fish to breed
      :param: ``age_shark`` Age of shark to breed
      :param: ``energy_eat`` Amount of energy after eating fish
      :param: ``energy_initial`` Amount of energy at begining
      :rets: ``self`` Instance
      """
      
      cdef int ok, size0, size1, a
      
      ok = 0
      if hasattr(creatures, 'shape'):
         creatures.astype(int, copy=False)
         if nsharks >= 0 or nfish >= 0 or shape != None:
            raise ValueError("Mnoho parametru")
      else:
         ok = 0
         creatures = numpy.zeros(shape)
         size0 = creatures.shape[0]
         size1 = creatures.shape[1]
            
         if nfish < 0 or nsharks < 0 or nfish > size0*size1 or nsharks > size0*size1:  
            raise ValueError("Malo parametru")
            
         #ran = random.sample(range(0, size0*size1), nfish + nsharks)
         #ran = numpy.frombuffer(numpy.random.bytes(size0*size1),dtype=numpy.uint16, count=nfish+nsharks)
         ran = numpy.random.random_integers(0, size0*size1-1, nfish + nsharks)
         ran_fish = numpy.random.randint(low=1, high=age_fish+1, size=nfish)
         ran_shark = numpy.random.randint(low=1, high=age_shark+1, size=nsharks)
         a = 0   
          
         while ok < nfish:
            if creatures[int(ran[ok]/size1), ran[ok]%size1] != 0:
               ran[ok] += 1
               ran[ok] %= size0*size1
               continue
            creatures[int(ran[ok]/size1), ran[ok]%size1] = ran_fish[a]
            ok += 1
            a += 1
             
         a = 0      
         while ok < nsharks + nfish:
            if creatures[int(ran[ok]/size1), ran[ok]%size1] != 0:
               ran[ok] += 1 
               ran[ok] %= size0*size1
               continue
            creatures[int(ran[ok]/size1), ran[ok]%size1] = -1*ran_shark[a]
            ok += 1  
            a += 1   
           
      if hasattr(energies, 'shape'):
         if energies.shape[0] != creatures.shape[0] or energies.shape[1] != creatures.shape[1]:
            raise ValueError("Spatne rozmery")
         if energy_initial != 0:
            raise ValueError("Mnoho parametru")   
      else:
         if energy_initial == 0:
            energy_initial = 3
         energies = numpy.zeros((creatures.shape[0], creatures.shape[1]))  
         for i in range(0, creatures.shape[0]):
            for j in range(0, creatures.shape[1]):
               if creatures[i,j] < 0: 
                  energies[i,j] = energy_initial
                  
      self.energies = energies
      self.creatures = creatures
      self.age_fish = age_fish
      self.age_shark = age_shark
      self.eat = energy_eat 
      self.initEnergy = energy_initial           
         
   
   def tick(self):
      """
      Move creatures to next chronon.
      
      Move fish by 1 position, move shark by 1 position, decrease energies. Sharks eat fish if they are next to them. Old creatures breed descendant.
      
      :rets: ``self`` Instance
      """
      
      cdef int size0, size1, value, ways, i, j, a
      
      energies = self.energies
      creatures = self.creatures
      
      creatures2 = creatures.copy()
      value = 0

      energies = energies - 1
      
      size0 = creatures.shape[0]
      size1 = creatures.shape[1]
      
      ran = numpy.random.randint(low=1, high=5, size=size0*size1)
      a = 0
      
      # Fish
      with cython.boundscheck(False):
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
               if creatures[i,j] >= self.age_fish:
                  value = 0
               else:
                  value = creatures[i,j] 
               while True:
                  a += 1
                  if a >= size0*size1:
                     ran = numpy.random.randint(low=1, high=5, size=size0*size1)
                     a = 0 
                  if ran[a] == 1 and creatures2[(i+1)%size0,j] == 0:
                     creatures2[(i+1)%size0,j] = value + 1
                     break
                  if ran[a] == 2 and creatures2[(i-1)%size0,j] == 0:
                     creatures2[(i-1)%size0,j] = value + 1
                     break
                  if ran[a] == 3 and creatures2[i,(j+1)%size1] == 0:
                     creatures2[i,(j+1)%size1] = value + 1   
                     break
                  if ran[a] == 4 and creatures2[i,(j-1)%size1] == 0:
                     creatures2[i,(j-1)%size1] = value + 1
                     break
               if creatures[i,j] >= self.age_fish:
                  creatures2[i,j] = 1
               else:
                  creatures2[i,j] = 0       
            else:
               if creatures[i,j] >= self.age_fish:
                  creatures2[i,j] = self.age_fish
                  continue
               else:
                  creatures2[i,j] = creatures[i,j] + 1 
         
      creatures = creatures2.copy() 
      energies2 = energies.copy()
          
      # Sharks
      with cython.boundscheck(False):                                   
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
               if creatures[i,j] <= -1*self.age_shark:
                  value = 0
                  creatures2[i,j] = -1
                  energies2[i,j] = energies[i,j]
               else:
                  value = creatures[i,j] 
                  creatures2[i,j] = 0      
               while True:  
                  a += 1
                  if a >= size0*size1:
                     ran = numpy.random.randint(low=1, high=5, size=size0*size1)
                     a = 0
                  if ran[a] == 1 and creatures2[(i+1)%size0,j] > 0:
                     creatures2[(i+1)%size0,j] = value - 1
                     energies2[(i+1)%size0,j] = energies[i,j] + self.eat
                     break
                  if ran[a] == 2 and creatures2[(i-1)%size0,j] > 0:
                     creatures2[(i-1)%size0,j] = value - 1                                                                               
                     energies2[(i-1)%size0,j] = energies[i,j] + self.eat
                     break
                  if ran[a] == 3 and creatures2[i,(j+1)%size1] > 0:
                     creatures2[i,(j+1)%size1] = value - 1
                     energies2[i,(j+1)%size1] = energies[i,j] + self.eat
                     break
                  if ran[a] == 4 and creatures2[i,(j-1)%size1] > 0:
                     creatures2[i,(j-1)%size1] = value - 1
                     energies2[i,(j-1)%size1] = energies[i,j] + self.eat
                     break
            else:      # neni tam ryba
               ways = 0   
               if creatures[(i+1)%size0,j] == 0:
                  ways += 1 
               if creatures[(i-1)%size0,j] == 0:
                  ways += 1
               if creatures[i,(j+1)%size1] == 0:
                  ways += 1
               if creatures[i,(j-1)%size1] == 0:
                  ways += 1
               
               if ways != 0:
                  if creatures[i,j] <= -1*self.age_shark:
                     value = 0
                     creatures2[i,j] = -1
                     energies2[i,j] = energies[i,j]
                  else:
                     value = creatures[i,j] 
                     creatures2[i,j] = 0  
                  while True:
                     a += 1
                     if a >= size0*size1:
                        ran = numpy.random.randint(low=1, high=5, size=size0*size1)
                        a = 0
                        
                     if ran[a] == 1 and creatures[(i+1)%size0,j] == 0:
                        creatures2[(i+1)%size0,j] = value - 1
                        energies2[(i+1)%size0,j] = energies[i,j]
                        break
                     if ran[a] == 2 and creatures[(i-1)%size0,j] == 0:
                        creatures2[(i-1)%size0,j] = value - 1                                
                        energies2[(i-1)%size0,j] = energies[i,j]
                        break
                     if ran[a] == 3 and creatures[i,(j+1)%size1] == 0:
                        creatures2[i,(j+1)%size1] = value - 1 
                        energies2[i,(j+1)%size1] = energies[i,j]
                        break
                     if ran[a] == 4 and creatures[i,(j-1)%size1] == 0:
                        creatures2[i,(j-1)%size1] = value - 1                                                                   
                        energies2[i,(j-1)%size1] = energies[i,j]
                        break
               else:  # neni misto
                  if creatures[i,j] <= -1*self.age_shark:
                     creatures2[i,j] = -1*self.age_shark
                     continue
                  else:
                     creatures2[i,j] = creatures[i,j] - 1
                       
      creatures = creatures2.copy()   
      energies = energies2.copy() 
      
      # Shark energy out 
      
      with cython.boundscheck(False):              
       for i in range(0, creatures.shape[0]):
         for j in range(0, creatures.shape[1]):
            if creatures[i,j] < 0 and energies[i,j] == 0:
               creatures[i,j] = 0            
      self.creatures = creatures
      self.energies = energies
      
      return self 
       
                  
   def count_fish(self):
      """
      Return actual amount of fish in array.
      
      :rets: ``int`` Number of fish in array.
      """
      
      cdef int result
      boolarr = self.creatures > 0
      return numpy.sum(boolarr, dtype='int64')
   
   def count_sharks(self):  
      """
      Return actual amount of sharks in array.
      
      :rets: ``int`` Number of sharks in array.
      """
      
      cdef int result
      boolarr = self.creatures < 0
      return numpy.sum(boolarr, dtype='int64')

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


