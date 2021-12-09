import numpy as np

def distance(A):
    n = len(A)
    Ak = np.copy(A)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                Ak[i,j] = min(Ak[i,j],Ak[i,k]+Ak[k,j])
    return(Ak)

def distancepred(A):
    n = len(A)
    Ak = np.copy(A)
    Pk = [[ -1 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if 0 < A[i,j] < np.inf:
                Pk[i][j] = i
    for k in range(1,n):
        for i in range(n):
            for j in range(n):
                if Ak[i,j] > Ak[i,k-1] + Ak[k-1,j]:
                    Ak[i,j] = Ak[i,k-1] + Ak[k-1,j]
                    Pk[i][j] = Pk[k-1][j]
    return(Ak,Pk)
    
def chemin(Pn,i,j):
    s,ch = j,[j]
    while s != i:
        s = Pn[i][s]
        ch.append(s)
    ch.reverse()
    return(ch)
                
    
A = np.array([[0,10,15,28],[10,0,np.inf,20],[15,np.inf,0,12],[28,20,12,0]])
distance(A)
(An,Pn) =  distancepred(A)
chemin(Pn,2,1)

dico = {'Paris':0, 'Marseille':1, 'Lyon':2, 'Toulouse':3, 'Nice':4,'Nantes':5, 'Bordeaux':6, 'Lille':7, 'Strasbourg':8, 'Montpellier':9, 'Brest':10, 'Nancy':11, 'Rouen':12, 'Orléans':13, 'Tours':14, 'Dijon':15, 'Besançon':16, 'Grenoble':17, 'Clermont-Ferrand':18, 'Rennes':19, 'Poitiers':20, 'Amiens':21 }

invdico = {dico[ville] : ville for ville in dico}

distances = [(0,2,465),(2,1,314),(2,18,164),(15,2,194),(2,17,112),(11,2,404),(11,15,214),(11,8,159),(11,0,385),(1,4,199),(1,9,169),(3,6,245),(3,9,247),(6,20,258),(20,5,219),(20,18,319),(20,14,105),(14,5,216),(14,13,117),(14,19,257),(14,18,240),(13,0,132),(13,12,252),(13,19,305),(13,5,335),(13,18,300),(13,11,449),(21,0,145),(21,11,420),(21,7,145),(21,12,120),(21,8,526),(12,0,136),(12,19,311),(12,14,310),(19,5,113),(19,10,242),(19,0,349),(5,10,295),(5,6,347),(7,0,225),(12,7,256),(11,7,418),(7,8,525),(7,15,502),(7,2,691),(2,9,303),(16,15,92),(16,2,255),(16,8,243),(16,11,206),(16,0,410),(17,1,306),(17,9,295),(0,3,679),(0,6,584),(18,9,332)]

def matadj(l,n):
    m = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i != j:
                m[i,j] = np.inf
    for (i,j,d) in l:
        m[i,j],m[j,i] = d,d
    return(m)
    
# test
l = [(0,1,10),(2,4,20),(0,3,12),(2,3,8),(3,4,15),(1,2,6)]
matadj(l,5)

D = matadj(distances,22)

(An,Pn) = distancepred(D)
chemin(Pn,0,5)

def distancevilles(a,b):
    return(An[dico[a],dico[b]])
    
def cheminvilles(a,b):
    l = chemin(Pn,dico[a],dico[b])
    return([invdico[k] for k in l])
    
distancevilles('Brest','Nice')
cheminvilles('Brest','Nice')
distancevilles('Strasbourg','Toulouse')
cheminvilles('Strasbourg','Toulouse')


    











                