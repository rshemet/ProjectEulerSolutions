prime = 600851475143
import numpy as np
import time


start = time.time()

#Question3

def CheckPrime(x):
    primecheck = True
    for i in range(2,int(x**0.5+1)):
        if x % i == 0:
            primecheck = False
            return primecheck
    return primecheck

def GetFactors(z):
    factors_list = []
    for i in range(1, int(z**0.5+1)):
        if z%i == 0:
            factors_list.append(i)
            factors_list.append(int(z/i))
    return factors_list

def GetAnswer3(input):
    factors = GetFactors(input)
    prime_factors = []
    for i in range(0, len(factors)):
        if CheckPrime(factors[i]):
            prime_factors.append(factors[i])
    return max(prime_factors)

#Question4

def CheckPalindrome(x):
    ans = False
    x=str(x)
    if x[::-1] == x:
        ans = True
    return ans

def GetAnswer4():
    range_lim = 1000
    palindromeMax = [0,0,0]
    for i in range(100,range_lim):
        for j in range(100,range_lim):
            if CheckPalindrome(i*j) and i*j > palindromeMax[2]:
                palindromeMax = [i,j,i*j]
    return palindromeMax[2]

#Question5

def DivisibleByRange(x):
    bottom_range = 1
    top_range = 20
    ans = True
    for i in range(bottom_range, top_range):
        if x % i != 0:
            ans = False
            return ans
    return ans

def GetAnswer5():
    # Basically, manually broke down the sequence into prime factors
    return 2*2*2*2*3*3*5*7*11*13*17*19

#Question6

def GetAnswer6():
    # Calculated by writing out a polynomial expansion
    sum = 0
    for i in range(1,101):
        for j in range(1,101):
            if i != j:
                sum += i*j
    return sum

#Question7



#Question9

def FindTriplet(hyp):
    triplets = []
    for a in range(1,hyp-1):
        b = np.sqrt(hyp**2-a**2)
        if int(b) == b:
            triplets.append([a,int(b),hyp])
            return triplets
    return "No Triplet"

#Question11

stop = time.time()

print("\nTime elapsed: ", stop - start, " sec.")