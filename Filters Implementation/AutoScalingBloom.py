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
    
class autoFilter:
    def __init__(self, M, NHash, maxParam,theta,T):
        #Initialize Filter Table with Zeros
        
        self.M = M 
        self.maxParam = maxParam 
        self.theta=theta # Theta : Threshold of count to set bit as positive in table
        self.T=T  #T: Threshold of dot product with table to consider element as existing in table.
        self.countTable=np.zeros(M,dtype= int)
        self.bloomTable = np.zeros(M, dtype = int) 
        self.tableSize = self.bloomTable.nbytes / 1024 / 8 

        # P - Primes Generator for Universal Hash Functions
        #e.g.: NHash = 3, P = [33018497, 20314969, 30891281]    
        self.P = [] 
        while len(self.P) < NHash:
            p = sympy.randprime(M, 2*M)
            if p not in self.P:
                self.P.append(p)

        # A, B - Random Generation for Parameters a, b of each Universal Hash Function 
        #e.g.: NHash = 3, A = [50725, 28788, 38992], B = [74739, 53707, 13081]
        self.A = [] 
        self.B = [] 
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
        res=np.zeros(self.M,dtype=int)
        for a, b, p in zip(self.A,self.B,self.P):
            x = ((strVal * a + b)%p)%self.M
            res[x]=1
        dp=np.dot(res,self.bloomTable)
        if(dp>self.T):
            notFound=False
        else:
            notFound=True
        return notFound
    # insert into filter Table
    def insert(self, code):
        notFound = True
        strVal = strToInt(code)
        for a, b, p in zip(self.A, self.B, self.P):
            x = ((strVal * a + b)%p)%self.M
            self.countTable[x]+=1
            if(self.countTable[x]>self.theta):
                self.bloomTable[x] = 1
    #Delete code from Table
    def delete(self, code):
            notFound = self.queryFilter(code)
            if notFound == False:
                strVal = strToInt(code)
                for a, b, p in zip(self.A, self.B, self.P):
                    x = ((strVal * a + b)%p)%self.M
                    if self.countTable[x] > 0:
                        self.countTable[x]-=1
                        if(self.countTable[x]<self.theta):
                            self.bloomTable[x]=0