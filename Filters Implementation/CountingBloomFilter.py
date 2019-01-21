import sympy
import random
import numpy as np
import matplotlib.pyplot as plt
import pymysql.cursors

#Create a hash function for text - converting it first into an integer
def strToInt(str1):
    value = 0
    for n, c in enumerate(str1):
        value += ord(c) * 128**n
    return value
 
class countingFilter:
    def __init__(self, M, NHash, maxParam):
        #Initialize Filter Table with Zeros
        self.M = M # --> 0
        self.maxParam = maxParam #--> 0
        self.countTable=np.zeros(M,dtype= int)

        # P - Primes Generator for Universal Hash Functions
        #e.g.: NHash = 3, P = [33018497, 20314969, 30891281]    
        self.P = [] #--> 3
        while len(self.P) < NHash:
            p = sympy.randprime(M, 2*M)
            if p not in self.P:
                self.P.append(p)

        # A, B - Random Generation for Parameters a, b of each Universal Hash Function 
        #e.g.: NHash = 3, A = [50725, 28788, 38992], B = [74739, 53707, 13081]
        self.A = [] #--> 4
        self.B = [] #--> 5
        firstVisA = 1
        firstVisB = 1
        while len(self.A) < NHash:
            while firstVisA == 1 or (a in self.A):
                a = random.randint(1, self.maxParam)
                firstVisA = 0

            while firstVisB == 1 or (b in self.B):
                b = random.randint(1, self.maxParam)
                firstVisB = 0

            self.A.append(a)
            self.B.append(b)
            
    # Query the Filter for a certain Code
    def queryFilter(self, word):
        strVal = strToInt(word)
        notfound=False
        for a, b, p in zip(self.A,self.B,self.P):
            x = ((strVal * a + b)%p)%self.M
            if self.countTable[x] == 0:
                notfound=True
                break
        return notfound
    
    # Store The URL in DB and insert into filter Table
    def insert(self, code):
        strVal = strToInt(code)
        for a, b, p in zip(self.A, self.B, self.P):
            x = ((strVal * a + b)%p)%self.M
            self.countTable[x]+=1
    def delete(self, code):
            notFound = self.queryFilter(code)
            if notFound == False:
                strVal = strToInt(code)
                for a, b, p in zip(self.A, self.B, self.P):
                    x = ((strVal * a + b)%p)%self.M
                    if self.countTable[x] > 0:
                        self.countTable[x]-=1