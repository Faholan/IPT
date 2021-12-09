# TRAITEMENT D'IMAGE

import matplotlib.pyplot as plt
import matplotlib.image  as mpimg
import numpy             as np
import os

# Manipulation d'images

s = os.getcwd()   # donne le répertoire courant
os.listdir()     # liste les fichiers du repertoire courant
chemin = 'F:/Pro/IPT/Cours/New'+"/Traitement d'image"  # repertoire de travail
os.chdir(chemin)  # modifie le répertoire de travail

imgC = mpimg.imread('esterel.jpg')   # charge une image
print(imgC.shape)   # taille de l'image
imgC[500,500]    # couleurs d'un pixel
plt.imshow(imgC)    # prépare l'affichage
plt.show()    # affichage
plt.close()   # ferme la fenêtre graphique

imgG = convertir_en_gris(imgC)
print(imgG.shape)
plt.imshow(imgG)
plt.savefig('esterel_gris.jpg')    # sauve la nouvelle image au format voulu
plt.show()
plt.close()

# Composantes d'une image couleur

def rvb(im):
    h,l = im.shape[0],im.shape[1]
    r = np.zeros((h,l,3),dtype = np.uint8)
    v = np.zeros((h,l,3),dtype = np.uint8)
    b = np.zeros((h,l,3),dtype = np.uint8)
    for i in range(h):
        for j in range(l):
            r[i,j,0],v[i,j,1], b[i,j,2] = im[i,j,0], im[i,j,1], im[i,j,2]
    return(r,v,b)

# Conversion en niveaux de gris

def nuance_gris(P):
    '''
    P : numpy.ndarray, [r,g,b] numpy.uint8;
    '''
    g  = np.uint8(0.2115*P[0]) + np.uint8(0.7154*P[1])+ np.uint8(0.0721*P[2])
    return g

def convertir_en_gris(img):
    '''
    img : numpy.ndarray (N x M x 3) avec
        img[i,j] : numpy.ndarray dim 1 et taille 3
        d'entiers uint8.
    '''
    assert isinstance(img, np.ndarray) and img.ndim == 3

    N, M, R  = img.shape
    imgG     = np.zeros((N, M), dtype = np.uint8)

    for n in range(0, N):
        for m in range(0, M):
            g   = nuance_gris(img[n,m])
            imgG[n, m] = g
    return imgG

def negatif(img):
    return -img

def contraste(img):
    '''
    img : numpy.ndarray (N x M x 3)
    On applique f(x) =  arctan(20x-10)/pi + 1/2
    '''
    return np.uint8(255*(np.arctan(20.*img-10)*2/np.pi + 1))

def histogramme_niveaux(T):
    '''
    T : numpy.ndarray, tableau à deux dimensions
        représentant une image en niveaux de gris;
    '''
    assert isinstance(T, np.ndarray) and T.ndim == 2
    px, py = T.shape
    H      = [int(0) for i in range(0,256)]

    for i in range(0, px):
        for j in  range(0,py):
            H[T[i,j]] += 1
    # affichage de l'histo
    for g in range(0, len(H)):
        plt.plot([g, g], [0, H[g]], color = 'black')
        plt.plot( g,  H[g], 'bo')

    plt.grid(True)
    plt.show()
    plt.close()
    return H

def negatif(img):
    assert isinstance(img, np.ndarray)
    return -np.uint8(img)


#=================================================================

def convolution_xy(T, C, d, x, y):
    '''
    T : numpy.ndarray, tableau à deux dimensions
        représentant une image;
    C : numpy.ndarray, tableau (2d+1)x(2d+1) à
        deux dimensions représentant un noyau de convolution;
    d : int (tel que C est de taille (2d+1)x(2d+1)
    '''
    g = 0 # couleur ou niveau de gris
    for i in range(-d, d+1):
        for j in range(-d, d+1):
            g +=  int(T[x+i,y+j])*C[d-i, d-j]
    return  g

def convolution(T, C):
    '''
    T : numpy.ndarray, tableau à deux dimensions
        représentant une image;
    C : numpy.ndarray, tableau (2d+1)x(2d+1) à
        deux dimensions représentant un noyau de convolution;
        C est de taille (2d+1)x(2d+1).
    '''
    assert isinstance(T, np.ndarray) and T.ndim == 2
    assert isinstance(C, np.ndarray) and C.ndim == 2
    px, py  = T.shape
    p, q    = C.shape

    assert p == q  and p % 2 == 1

    d       = (p-1)//2
    T1      = np.zeros((px,py), dtype = float)-1
    # T1[x,y) =255; image blanche.
    for x in range(d, px-d):
        for y in range(d, py-d):
            T1[x,y] = convolution_xy(T, C, d, x, y)
    return T1

def contours_Sobel(T, s):
    '''
    T : numpy.ndarray, tableau à deux dimensions
        représentant une image;
    s  : int, seuil pour tronquer la norme du gradient.
    '''
    assert isinstance(T, np.ndarray) and T.ndim == 2

    C_lissage = np.ones((5,5), dtype = int)/25
    Sobel_x   = np.matrix([[1,2,1],[0,0,0],[-1, -2,-1]], dtype = int)
    Sobel_y   = Sobel_x.transpose()

    T0 = convolution(T, C_lissage)
    GX = convolution(T0, Sobel_x)
    GY = convolution(T0, Sobel_y)

    px, py = T.shape
    TC = np.zeros((px,py), dtype = np.uint8)-1 #image blanche.

    for x in range(0, px):
        for y in range(0, py):
            g = max(abs(int(GX[x,y])), abs(int(GY[x,y])) )
            if g > s:
                TC[x,y] = np.uint8(0)
    return TC

#=================================================================

C_lissage     = np.matrix([[1,2,1],[2, 4, 2],[1,2,1]], dtype = int)/16
C_contraste   = np.matrix([[0,-1,0],[-1, 5, -1],[0 ,-1,0]], dtype = int)
    #----------------------------------------------------
C_contraste_5 = np.matrix(np.zeros((5,5), dtype = int))
for i in range(0,5):
    C_contraste_5[i,i]    = -1
    C_contraste_5[i, 4-i] = -1
C_contraste_5[2,2] = 9
    #----------------------------------------------------
Sobel_x = np.matrix([[1,2,1],[0,0,0],[-1, -2,-1]], dtype = int)
Sobel_y = Sobel_x.transpose()
    #----------------------------------------------------

# Tests

name =  'ski'
T = mpimg.imread(name + '.jpg')
T = convertir_en_gris(T)
plt.imshow(T, cmap ='gray')
plt.savefig('X%s_gris.jpg'%(name))
plt.show()
plt.close()
histogramme_niveaux(T)

print('Go for contoursSobel(T, s = 60, name = %s)')
TCS = contours_Sobel(T, 60)
plt.imshow(TCS, cmap ='gray' )
plt.savefig('X%s_Sobel_%s.jpg'%(name, 60))
plt.show()
plt.close()
