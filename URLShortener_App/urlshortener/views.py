# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
import sympy
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import pymysql.cursors

# Connect to the Database
def connectToDB(dbName = 'urls'):
    return pymysql.connect(host="$$$$", user="$$$$", passwd="$$$$", db='urls', 
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
# Insert to Database
def updateDB(code, url, tName, dbName = 'urls'):
    connection = connectToDB(dbName)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `SF` (`url`, `code`) VALUES (%s, %s)"
            cursor.execute(sql, (url, code))
        connection.commit()
    finally:
        connection.close()

# Select From Database
def queryURLFromDB(code, dbName = 'urls'):
    connection = connectToDB(dbName)
    try:
        with connection.cursor() as cursor:
            if len(code) == 0:
                sql = "SELECT `code` FROM `SF`"
                #cursor.execute(sql, (tName,))
                cursor.execute(sql)
                result = cursor.fetchall()
            else:
                sql = "SELECT `url` FROM `SF` WHERE `code`=%s"
                cursor.execute(sql, (code,))
                result = cursor.fetchone()
            
            return result
    finally:
        connection.close()

#Create a hash function for text - converting it first into an integer
def strToInt(str1):
    value = 0
    for n, c in enumerate(str1):
        value += ord(c) * 128**n
    return value

#Random Code Generator for the Shortened URL
def genCode():
    rands = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
    code = ''
    while len(code) < 8:
        code += chr(random.choice(rands))
    return code

# Standard Bloom Filter Class
class stdFilter:
    def __init__(self, M, NHash, maxParam):
        #Initialize Filter Table with Zeros
        self.M = M # --> 0
        self.maxParam = maxParam #--> 0
        self.bloomTable = np.zeros((M, 1), dtype = bool) #--> 1
        self.tableSize = self.bloomTable.nbytes / 1024 / 8 #--> 2

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
        self.tName = 'SF' #--> 7

    # Query the Filter for a certain Code
    def queryFilter(self, word):
        notFound = False
        strVal = strToInt(word)
        for a, b, p in zip(self.A, self.B, self.P):
            x = ((strVal * a + b)%p)%self.M
            if self.bloomTable[x] != 1:
                notFound = True
                break
        return notFound
    
    # Store The URL in DB and insert into filter Table
    def insertURL(self, code):
        strVal = strToInt(code)
        for a, b, p in zip(self.A, self.B, self.P):
            x = ((strVal * a + b)%p)%self.M
            self.bloomTable[x] = 1

    def fillFil(self, results):
    	for res in results:
    	    strVal = strToInt(res['code'])
    	    for a, b, p in zip(self.A, self.B, self.P):
    	        x = ((strVal * a + b)%p)%self.M
    	        self.bloomTable[x] = 1

def shorten(optFilter, url):
    results = queryURLFromDB('', 'SF')
    fil = stdFilter(200000, 3, 10000)
    fil.fillFil(results)
    notFound = True
    code = ''
    attempts = 0
    sTime = time.time() #start time
    
    if optFilter == 'yes':
        while notFound == True:
            code = genCode() #Generate Random Code Corresponding to the URL
            notFound = fil.queryFilter(code)
            attempts += 1
        fil.insertURL(code)
    else:
        while notFound == True:
            code = genCode() #Generate Random Code Corresponding to the URL
            results = queryURLFromDB(code)
            if results == None:
                notFound = False
            attempts += 1
            
    eTime = time.time() #end time
    updateDB(code, url, 'SF')
    
    return code, eTime - sTime, attempts



# Create your views here.
def home(request):
    if 'c' in request.GET:
        code = request.GET['c']
        result = queryURLFromDB(code)
        return redirect(result['url'])
    if 'optradio' in request.GET and 'url' in request.GET:
        optFilter = request.GET['optradio']
        url = request.GET['url']
        code, tim, attempts = shorten(optFilter, url)
        #print('####### code:', code)
        #print('####### atts:', attempts)
        #print('####### time:', tim)
        return render(request, 'urlshortener/index.html', {'code':code, 'time':str(tim), 'attempts':str(attempts)})
    return render(request, 'urlshortener/index.html', {'code':'NA', 'time':'NA', 'attempts':'NA'})