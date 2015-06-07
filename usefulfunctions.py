#usr/bin/env python
import time
from time import time as t
import math
from math import *
import sys
from sys import exit
from operator import add, sub, mul, div
import os
import pprint
from pprint import pprint as pp

from libvector3 import *

import physics
import mailer

#from numpyhelper import *

lg2 = log2 = lambda x: math.log(x, 2)
lg10 = log10 = lg = lambda x: math.log(x, 10)
ln = math.log
rad = math.radians
deg = math.degrees

avg = lambda seq: sum(seq) / float(len(seq))

def pd(o, filterText=None, onlyHidden=True):
    """'Print Dir'
    Performs print("\\n".join(dir(o)))
    If onlyHidden is True, it won't print things starting with _,
    that is print("\\n".join([x for x in dir(o) if not x.startswith("_")]))
    
    If filterText is not None, only prints things where
    filterText is in each string from the dir.
    """
    
    if onlyHidden:
        if filterText is None:
            print("\n".join([x for x in dir(o) if not x.startswith("_")]))
        else:
            print("\n".join([x for x in dir(o)
                if not x.startswith("_") and filterText in x]))
    else:
        if filterText is None:
            print("\n".join(dir(o)))
        else:
            print("\n".join([x for x in dir(o) if filterText in x]))
            
"""Performs pprint.pprint(dir(o)), but also removes strings
    starting with noStartFilter (default: '__')
    and requires filterWord to be in the string
    
    only prints things where filterText is in each string from the dir.
    
    Example: ppd(math, "asin") -> pprint.pprint(['asin', 'asinh'])"""
def ppd(o, filterText="", noStartFilter="__"):
    if noStartFilter:
        pprint.pprint([x for x in dir(o) 
            if not x.startswith(noStartFilter)
            and filterText in x])
    else:
        pprint.pprint(filter(lambda x: filterText in x, dir(o)))

def ls(fr, to=None, n=100):
    """Linspace function, returns a list of n values from 'fr' to 'to'.
    If no 'to' is specified, returns values 0 to 'fr' instead"""
    if to == None:
        fr, to = 0.0, fr
    stepSize = (to-fr) / float(n)
    return [fr + stepSize*i for i in range(int(n))]
        
linspace = ls

def product(seq):
    if len(seq) == 0: return None
    v = seq[0]
    for val in list(seq)[1:]:
        v *= val
    return v

def isPrime(n):
    if n == 2: return True
    if n % 2 == 0: return False
    s = int(sqrt(n) + 1)

    for i in range(3, s, 2):
        if n % i == 0:
            return False
    return True
    
#~ def det(a,b,c=None): #determinant for vectors or lists
    #~ if type(a) == type([]): a = V3(*a)
    #~ if type(b) == type([]): b = V3(*b)
    #~ if type(c) == type([]): c = V3(*c)
    
    #~ if c == None: #2x2 determinant, only uses x and y elements
        #~ return a.x*b.y - a.y*b.x
    
    #~ return a.x*b.y*c.z + a.y*b.z*c.x + a.z*b.x*c.y -\
        #~ (a.x*b.z*c.y + a.y*b.x*c.z + a.z*b.y*c.x)

"""
def all(seq): #Copy of the all function found in python 2.6
    for item in seq:
        if not bool(item): return False
    return True
"""

def isSubset(A, B):
    for a in A:
        if a not in B:
            return False
    return True

def fibr(n): #ultra slow recursive fib function
    if n <= 2: return 1
    return fib(n-1) + fib(n-2)

def fib(n):
    if n <= 2: return 1
    fibList = [1,1]
    while len(fibList) < n:
        fibList.append(sum(fibList[-2:]))
    return fibList[-1]

def fac(n):
    if n <= 1: return 1
    return fac(n-1)*n
    
def clamp(value, minValue, maxValue):
    """Returns value, with minimum/maximum values minValue/maxValue
    """
    return min(max(value, minValue), maxValue)
    
def solve(varExpression, startStop,
        startIt=1e4, passes=3, epsilon=1e-2, silent=False,
        firstPassInfo=None):
    """Crappy numeric solver. Call like this:
    solve("varYouWant:calculation|prerequicites", [minVal, maxVal])
    Where prerequicities can be ommited.
    Example:
    x = solve("x:cos(x)==x", [0,10])
    P = solve("P: P=U*I |R=500; I=1.3; U=R*I", [0,1e5])
    """
    
    var, expression = map(lambda x: x.strip(), varExpression.split(":"))
    
    #== becomes = and so on
    expression = expression.replace("==", "=")
    
    #exponentiation is most likely what was intended
    expression = expression.replace("^", "**")
    
    if " where " in expression and "|" not in expression:
        #replace the rightmost " where " with " | "
        expression = " | ".join(expression.rsplit(" where ", 1))
    
    if "|" in expression:
        expression, prereq = expression.split("|",1)
        prereq = prereq.strip()
        exec(prereq)
    
    if "=" not in expression:
        #we don't know what the expression should be, so we guess 0.0
        expression += "=0.0"
    vl, hl = expression.split("=")
    
    #print "vl: %s, hl: %s" % (vl, hl)

    start, stop = startStop
    if start > stop: #exchange places
        stop, start = start, stop

    stepSize = (float(stop) - float(start)) / startIt

    if not silent:
        print("stepSize: %s, startIt: %s" % (stepSize, startIt))

    bestVal = None
    bestDelta = None
    highestEpsilon = 1e90
    i = start
    
    while i <= stop:
        exec("%s = %s" % (var, i))

        try:
            delta = eval(vl) - eval(hl)
            if abs(delta) < highestEpsilon:
                highestEpsilon = abs(delta)
                bestVal = i
                bestDelta = delta
        except e:
            print e
            pass
        i += stepSize

    if not silent:
        if firstPassInfo:
            whichPass = firstPassInfo - passes
        else:
            whichPass = 1
            firstPassInfo = passes + 1
        
        print("pass: %s/%s, bestVal: %s, bestDelta: %s" %
            (whichPass, firstPassInfo-1, bestVal, bestDelta))

    if passes > 1:
        if abs(2*stepSize/startIt) < 1e-19:
            if not silent:
                print "At lowest stepsize, Can't get better precision!"
            return bestVal
        
        #recursively call itself until all passes are completed)
        newStartStop = [bestVal - stepSize, bestVal + stepSize]
        return solve(varExpression, newStartStop,
            startIt, passes-1, epsilon, silent, firstPassInfo)
    return bestVal
    
def integral(f, rng): #function, range
    return sum(f(rng[i-1])*(rng[i]-rng[i-1]) for i in range(1, len(rng)))
        
def deriv(f, h=1e-5):
    """Returns an approximation of the derivated function with dx = h
    Example: diff(lambda x: x**2)(4) should be around 8 as d/dx x**2 == 2*x"""
    return lambda x: (f(x+h) - f(x-h))/(2*h)
    
def dre(p, s):
    """DoRegExp
    
    Performs regexp search with pattern p on string s and prints
        results and groups (including groupDict if existing)"""
    import re
    m = re.match(p, s)
    #m = re.findall(p, s)
    if m:
        print " Group:", m.group()
        print "Groups:", m.groups()
        groupDict = m.groupdict()
        if groupDict:
            print " GDict:", groupDict
    else:
        print "No matches!"
    return m

def dre2(p, s):
    """DoRegExp
    
    Performs regexp search with pattern p on string s and prints
        results and groups"""
    import re
    m = re.match(p, s)
    #m = re.findall(p, s)
    if m:
        print " Group:", m.group()
        print "Groups:", m.groups()
        #return m
    else:
        print "No matches!"
        #return None
    
def say(text, isInteger=False): #requires pyttsx
    import pyttsx
    engine = pyttsx.init()
    if isInteger or type(text) == int:
        text = sayNumberString(int(text))
    engine.say(text)
    engine.runAndWait()

def rot13(text):
    import codecs
    return codecs.encode(text, 'rot_13')
    
def sayNumberString(n):
    s = str(n)
    if s[0] == "-":
        s = s[1:]
        sayMinus = True
    else:
        sayMinus = False
    phrases = ["thousand", "million", "billion", "trillion", "quadrillion"]
    i = 0
    s_out = ""
    largestPhrase = (len(s)-1)/3
    while len(s) > 3:
        phrase = phrases[i]
        i += 1
        s_out = " " + phrase + " " + s[-3:] + s_out
        s = s[:-3]
    s_out = s + s_out
    
    if sayMinus:
        return "minus " + s_out
    return s_out
    
cd = os.chdir

def testFunctions():
    print("***Testing Functions. All should say True.")
    print("product:", product(range(1,4+1)) == 24)
    print("isPrime:", all(isPrime(x) for x in [2,3,5,7,11]))
    print("isSubset:", isSubset([3,4,5],[3,4,5,6]))
    val = solve("x:x=sin(rad(45))", [0,1], silent=True)
    print("solve:", abs(val-0.70710) < 1e-5)

if __name__ == "__main__":
    testFunctions()
