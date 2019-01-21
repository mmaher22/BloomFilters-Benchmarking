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
	
#Class of Ternary Bloom Filter
class terFilter:
    def __init__(self, M, NHash, maxParam): #M = Filter Size - NHash = Number of Hash Functions - maxParam = maximum value of a,b parameters of universal hash functions
        #Initialize Filter Table with Zeros
        self.M = M #-->0.1
        self.maxParam = maxParam #--> 0.2
        self.bloomTable = np.zeros((M, 1), dtype = 'int8') #--> 1
        self.tableSize = self.bloomTable.nbytes / 1024 / 4 #--> 2

        # P - Primes Generator for Universal Hash Functions
        #e.g.: NHash = 3, P = [33018497, 20314969, 30891281]    
        self.P = [] #--> 3
        while len(self.P) < NHash:
            p = sympy.randprime(M, M*2)
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
        
        self.dbName = 'urls' #--> 6 
        self.tName = 'TF' #--> 7 ########################### TAKE CARE #################################

    # Query the Filter for a certain Code
    def queryFilter(self, code):
        notFound = False
        flag = False
        strVal = strToInt(code)
        for a, b, p in zip(self.A, self.B, self.P):
            x = ((strVal * a + b)%p)%self.M
            #print('RR:', self.bloomTable[x])
            if self.bloomTable[x] == 0:
                notFound = True
                break
            elif self.bloomTable[x] == 1:
                flag = True
                
        if notFound == True:
            return -1 # -1 = element not found
        elif flag == False:
            return 0
        else:
            return 1 #1 = element foundTrue
    
    
    # Store The URL in DB and insert into filter Table
    def insert(self, code):
        strVal = strToInt(code)
        for a, b, p in zip(self.A, self.B, self.P):
            x = ((strVal * a + b)%p)%self.M
            self.bloomTable[x] += 1
            if self.bloomTable[x] > 2:
                self.bloomTable[x] = 2
                
        #updateDB(code, url, self.dbName, self.tName) #Insert to Database
    
    # Delete an Element from the Table
    def delete(self, code):
        res = queryFilter(self, code)
        
        if res == 1:
            strVal = strToInt(code)
            for a, b, p in zip(self.A, self.B, self.P):
                x = ((strVal * a + b)%p)%self.M
                if self.bloomTable[x] == 1:
                    self.bloomTable[x] = 0        