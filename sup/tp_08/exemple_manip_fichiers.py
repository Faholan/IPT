# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 17:55:23 2014

@author: test
"""

### Liste des lignes d un fichier en lecture
#1# On lit toutes lignes d un coup, puis on les affiche : 1ere methode
###

import os
os.chdir(input())

fichier = open("baston.txt", "r")
lignes = fichier.readlines()
fichier.close()
print(lignes)
print("### fin du 1 ###")
###
#2# On lit toutes lignes d un coup, puis on les affiche : 2e methode
###

fichier = open("baston.txt", "r")
lignes = fichier.readlines()
fichier.close()
for a in lignes:
    print(a)
print("### fin du 2 ###")
###
#3# On lit toutes lignes d un coup, puis on les affiche :
### 3e methode= on enleve le saut de ligne inutile
for a in lignes:
    print(a, end="")
print("")  # Mettre en commentaire cette ligne pour voir
print("### fin du 3 ###")

### Changer de repertoire : 1ere methode=prefixer le nom du fichier
#4#
###
fichier = open("fichierEntree/grosseBaston.txt", "r")
lignes = fichier.readlines()
fichier.close()
for a in lignes:
    print(a, end="")
print("")
print("### fin du 4 ###")

### Changer de repertoire : 2e methode=changer de repertoire de travail
#5#  Il faut enlever les guillemets et ecrire le chemin du repertoire
###  a la place des points d interrogation
"""
import os
# print(os.getcwd)
os.chdir("C:/???")
# attention ce changement est definitif...
fichier = open("grosseBaston.txt", "r")
lignes = fichier.readlines()
fichier.close()
for a in lignes:
    print (a)
os.chdir("C:/???")
# ...il faut donc remettre a la fin le repertoire initial
print("### fin du 5 ###")
"""
### Lecture ligne par ligne
#6# readline SANS "s"
###
fichier = open("baston.txt", "r")
print(fichier.readline())  # On lit la 1ere ligne
print(fichier.readline())  # On lit la 2e ligne
fichier.close()
# enlever le prochain diese pour voir...
# print(fichier.readline())
# ...On ne lit pas la 3e ligne:
# le fichier ayant ete ferme on ne peut plus le lire !
print("### fin du 6 ###")

### Lecture ligne par ligne
#7# On affiche toute les lignes avec readline SANS "s"
###astuce1 : a la fin du fichier, l appel de readline renvoie une ligne vide
###astuce2 : un string non vide (resp. vide) est evalue comme True(resp. False)
fichier = open("baston.txt", "r")
ligne = fichier.readline()
while ligne:
    print(ligne, end="")
    ligne = fichier.readline()
print("")
fichier.close()
print("### fin du 7 ###")

### Iteration sur l'objet de type file
#8#
###
fichier = open("baston.txt", "r")
for ligne in fichier:
    print(ligne, end="")
print("")
fichier.close()
print("### fin du 8 ###")

### Iteration sur l'objet de type file
#9# On calcule le nombre de caracteres
###
fichier = open("baston.txt", "r")
s = 0
for ligne in fichier:
    s += len(ligne)
fichier.close()
print(s)  # surpris du resultat ?
print("### fin du 9 ###")

#### Lecture caractere par caractere
#10#  read(n) lit n caracteres
####
fichier = open("baston.txt", "r")
lettre = fichier.read(1)
while lettre:
    print(lettre)
    lettre = fichier.read(1)
fichier.close()
print("### fin du 10 ###")

#### Ecriture dans un fichier
#11#
####
destination = open("fichierSortie/bulletinMeteo.txt","w")
destination.write("Canberra : 18\nSidney : 20\n")
destination.write("Melbourne : 19\n")
destination.close()
print("### fin du 11 ###")

#### Extraction de donnees
#12# .split("car") repartit les donnees, separee par "car" dans un tableau
#### .strip() enleve le superflu
fichier = open("fichierEntree/tennis.txt", "r")
print(fichier.readline())
print(fichier.readline().split(","))
print(fichier.readline().strip().split(","))
fichier.close()
print("### fin du 12 ###")

#### Extration de donnees et reecriture
#13#
####
fichier = open("fichierEntree/tennis.txt", "r")
lignes = fichier.readlines()
fichier.close()
fichier = open("fichierSortie/tennisBis.txt", "w")
for joueuse in lignes:  # "joueuse" est une chaine de caracteres
    info = joueuse.strip().split(",")  # "info" est bien un tableau
    fichier.write(f"{info[0]}\t{info[1]}\t{info[2]}\n")
fichier.close()
print("### fin du 13 ###")

"""

from math import sqrt

def est_premier(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    for k in range(2, 1+int(sqrt(n))):
        if n%k == 0:
            return False
    return True
"""
######## Quelques graphiques avec Matplotlib ########
# il faut enlever les 2 prochains triples guillemets pour voir quelquechose
# Observer les valeurs de t et y. Reflechir a la signification de chaque ligne
#
"""
from math import sqrt, pi
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(-pi, 3*pi, 1000)
y = np.cos(t)

plt.plot(t, y)
plt.savefig("fichierSortie/cosinus.pdf")
plt.show()
"""
# Observer le resultat produit par chaque commande ci-dessous
# Dans les commandes ci-dessus, inserer progressivement, avant le savefig,
# les lignes ci-dessous
"""
plt.grid()
plt.axhline(color="black")
plt.axvline(color="black")
ys = np.sin(t)
plt.plot(t,ys)
plt.legend(["cosinus", "sinus"], loc="upper left")
"""
