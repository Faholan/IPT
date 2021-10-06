# Ex 1

def f(m,n):
    if m == 0: return(0)
    else:
        return(f(m-1,n)+n)
        
# f(m,n) calcule le produit mn
        
def g(n):
    if n == 1: return(1)
    elif n % 2 == 0: return(g(n-1))
    else: return(n*g(n-2))
    
# g(n) calcule le produit des nombres impairs <=n

# Ex 3

def renverse(tab):
    def aux(i,j):
        if i<j:
            tab[i],tab[j]=tab[j],tab[i]
            aux(i+1,j-1)
    aux(0,len(tab)-1)
    
l = [1,2,3,4,5]
renverse(l); l
l = [1,2,3,4,5]
l.reverse(); l

        
# Ex 4

def thue(n):
    if n == 0: return(0)
    elif n % 2 == 0: return(thue(n//2))
    else: return(1 - thue(n//2))

len([n for n in range(2020) if thue(n) == 1])

# Ex 5

def periode(p):   # version itérative
    u,uu,m = 1,1,1
    while u != 0 or (u == 0 and uu != 1):
        u, uu = uu, (u + uu) % p
        m += 1
    return(m)
    
def periode2(p):     # version récursive
    def aux(x,y,i):
        if x==0 and y==1: return i
        else:
            return aux(y,(x+y)%p,i+1)
    return aux(1,1,1)

    
def crible(n):    # crible d'Erathostène
    pile = [k for k in range(2,n+1)] 
    res = []
    while pile != []:
        a = pile.pop(0)
        for x in pile:
            if x%a == 0: pile.remove(x)
        res.append(a)
    return(res)
    
primes = crible(100)
[(p,periode(p)) for p in primes]
    
    
# Ex 6

def mini_local(t):
    k = 1
    while t[k+1] <= t[k]: k += 1
    return t[k]
    
def min_local(t):
    def aux(i,j):
        if i == j: return t[i]
        if j == i+2: return t[i+1]
        k = (i+j)//2
        if t[k-1]>= t[k]:
            if t[k] <= t[k+1]: return t[k]
            else: return aux(k,j)
        else:
            return aux(i,k)
    return aux(0,len(t)-1)
    
t = [10,8,6,7,5,4,8,12,7,2,9]
mini_local(t)
min_local(t)
t = [10,9,8,7,6,5,4,3,2,5]
mini_local(t)
min_local(t)
    

# Ex 7

coefbinom = {(1,0) : 1, (1,1) : 1}

def binom(n,p):
    if p > n: return(0)
    if p == 0: return(1)
    else: return(binom(n-1,p) + binom(n-1,p-1))
    
def binom2(n,p):
    if p > n: return(0)
    if p == 0: return(1)
    else:
        if (n,p) not in coefbinom:
            coefbinom[n,p] = binom2(n-1,p) + binom2(n-1,p-1)
        return(coefbinom[n,p])
        
# Ex 8

def ppdiv(n):
    p = 2
    while n % p != 0 and p*p <= n:
        p += 1
    if p*p > n:
        return(n,1)
    ordre = 0
    while n % p == 0:
        ordre += 1
        n = n//p
    return(p,ordre)
    
def decompose(n):
    if n == 1: return([])
    (p,ordre) = ppdiv(n)
    m = n//(p**ordre)
    l = decompose(m)
    l.insert(0,(p,ordre))
    return(l)
    
def isprime(n):
    return ppdiv(n)[0] == n
    
def liste(n):
    return [p for p in range(2,n+1) if isprime(p)]
    

# Ex 9

def phi(n):
    def aux(L,nb):
        if len(L) == 0: return(nb)
        else:
            x = L.pop(0)
            if n % x == 0:
                return aux([k for k in L if k % x != 0],nb) 
            else: return aux(L,nb+1)
    return(aux(list(range(2,n)),1))
            
# Ex 10

def horner(p,x):
    if len(p) == 1: return p[0]
    p[-2] += p[-1] * x
    return horner(p[:-1],x)
    
# Ex 11

def palindrome(mot):
    def aux(i,j):
        if i >= j:
            return(True)
        else:
            if mot[i] != mot[j]:
                return(False)
            else:
                return(aux(i+1,j-1))
    return(aux(0,len(mot)-1))
    
def palindrome(mot):
    n = len(mot)
    if n <= 1:
        return(True)
    else:
        return(mot[0]==mot[n-1] and palindrome(mot[1:n-1]))	

# Ex 12

import sys
sys.setrecursionlimit(100000)

def bissextile(n):
    return (n % 4 == 0) and (n % 100 != 0 or n % 400 == 0)
    
d = {0:'lundi', 1:'mardi', 2:'mercredi', 3:'jeudi', 4:'vendredi', 5:'samedi', 6:'dimanche'}
    
def aux(j,m,a):
    if a>=2018:
        if j==1 and m==1:
            if a==2018: return 0
            else: return 1+aux(31,12,a-1)
        else:
            if j>=2: return 1+aux(j-1,m,a)
            else:
                if m-1 in [1,3,5,7,8,10,12]:
                    return 31+aux(1,m-1,a)
                else:
                    if m-1 in [4,6,9,11]:
                        return 30+aux(1,m-1,a)
                    else:
                        if not bissextile(a): return 28+aux(1,2,a)
                        else: return 29+aux(1,2,a)
    else:
        if m==12: return aux(1,1,a+1)+j-32
        else:
            if m in [1,3,5,7,8,10]:
                return aux(1,m+1,a)+j-32
            else:
                if m in [4,6,9,11]:
                    return aux(1,m+1,a)+j-31
                else:
                    if not bissextile(a): return aux(1,3,a)+j-29
                    else: return aux(1,3,a)+j-30
                
                        
def date(j,m,a):
    return d[aux(j,m,a) % 7]
    
date(6,10,2021)


                        

        
    
    
    