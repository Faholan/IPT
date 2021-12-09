import time

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

# grille facile
M1 = [[0,1,0,0,5,2,0,0,7],[0,8,0,7,0,0,0,1,0],[9,0,2,0,6,1,5,0,0],
[4,0,0,2,0,0,7,0,0],[8,0,1,0,7,0,2,0,4],[0,0,7,0,0,5,0,0,9],
[0,0,6,5,3,0,9,0,8],[0,9,0,0,0,4,0,5,0],[2,0,0,9,8,0,0,7,0]]

# grille moyenne
M2 = [[0,6,0,0,0,0,9,8,5],[0,0,5,6,0,9,0,0,0],[0,0,7,0,0,0,0,4,0],
[0,2,0,9,0,0,0,0,8],[0,7,0,5,0,1,0,6,0],[1,0,0,0,0,3,0,9,0],
[0,1,0,0,0,0,4,0,0],[0,0,0,3,0,6,8,0,0],[6,5,9,0,0,0,0,1,0]]

# grille difficile
M3 = [[0,0,0,3,0,1,0,0,0],[0,0,0,0,0,0,3,7,0],[2,0,8,0,9,0,0,5,0],
[6,9,0,0,0,2,0,0,0],[4,0,1,0,3,0,2,0,7],[0,0,0,9,0,0,0,1,5],
[0,1,0,0,7,0,8,0,3],[0,4,6,0,0,0,0,0,0],[0,0,0,4,0,3,0,0,0]]

t1 = time.process_time()
sudoku(M3)
t2 = time.process_time()
print(t2-t1)




