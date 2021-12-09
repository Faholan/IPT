import time

def voisins(i,j):
    cases = [(i+1,j+2),(i+2,j+1),(i-1,j+2),(i-2,j+1),(i+1,j-2),(i+2,j-1),(i-1,j-2),(i-2,j-1)]
    return([(x,y) for (x,y) in cases if x>=0 and x<=8 and y>=0 and y<=8])

def test(M,i,j,num):
    for k in range(9):
        if M[i][k] == num or M[k][j] == num:
            return False
    ip = int(i/3)*3
    jp = int(j/3)*3
    for k in range(3):
        for l in range(3):
            if M[ip+k][jp+l] == num:
                return False
    for (k,l) in voisins(i,j):
        if M[k][l] == num:
            return False
    return True

def trouvezero(M):
    for i in range(9):
        for j in range(9):
            if M[i][j] == 0:
                return (i,j)
    return (10,10)

def sudoku(M):
    (i,j) = trouvezero(M)
    if i == 10:
        print(M)
    else:
        for k in range(1,10):
            if test(M,i,j,k):
                M[i][j] = k
                sudoku(M)
            M[i][j] = 0

t1 = time.process_time()
M = [[4,0,0,0,0,0,0,0,9],[9,0,3,0,0,0,4,0,1],[0,0,0,0,9,0,3,0,0],
[3,0,0,0,6,0,1,9,7],[0,0,0,1,0,7,0,0,0],[0,8,7,0,0,0,6,2,0],
[0,1,0,0,0,0,0,3,0],[0,0,0,0,1,0,0,0,0],[0,0,0,9,0,3,0,0,0]]
sudoku(M)
t2 = time.process_time()
print(t2-t1)


