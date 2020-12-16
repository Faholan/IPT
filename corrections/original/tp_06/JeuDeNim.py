# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:02:35 2013

@author: test
"""


from numpy.random import randint

def jeuDeNim(nAllumette,nMax):
    """
    - 'nAllumette' correspond au nombre total initial d'allumettes
    - 'nMax' correspond au nombre maximal d'allumettes que peut prendre un joueur
    - fait appel à une fonction 'introduction' pour commencer le jeu
    - tant qu'il reste suffisamment d'allumettes, le joueur et l'ordinateur jouent à tour de rôle (via les fonctions 'tourJoueur' et 'tourOrdi')
    - la partie étant finie, on affiche le résultat
    """
    niveau=introduction(nAllumette,nMax)
    estFini=False
    while not estFini:
        nAllumette,estFini=tourJoueur(nAllumette,nMax,estFini)# au joueur de jouer, et on actualise les valeurs des variables
        if not estFini:
            nAllumette,estFini=tourOrdi(nAllumette,nMax,estFini,niveau)#à l'ordinateur de jouer, et on actualise les valeurs des variables
    print("\n"+estFini)

def introduction(nAllumette,nMax):
    """
    - On affiche le but du jeu et on recupère le niveau de difficulté de l'ordinateur
    - On ne gère pas les erreurs d'entrée du joueur (s'il ne met pas de chiffre en console, cela plante...)
    """
    print("Un ensemble de {} allumettes sont disposées devant vous.".format(nAllumette))
    print("A chaque étape vous pouvez retirer entre 1 et {} allumettes.".format(nMax))
    print("Le joueur qui prend le dernier bâton a perdu.")
    print("Vous jouez contre l'ordinateur et vous jouez en premier")
    return(int(input("Choisissez le niveau de l'ordinateur de 1 (facile) à 10 (difficile) ")))


def tourJoueur(nAllumette,nMax,estFini):
    """
    - affiche l'état actuel du jeu
    - le joueur retire un certain nombre d'allumettes
    - on modifie l'état de la partie (via la variable estFini).
    Remarque : une chaine de caractère non vide est considérée comme True, sinon elle est considérée comme False
    """
    print("\n***Votre tour. Allumettes disponibles :" + "|"*nAllumette)
    nbAllumetteJoueur=-1
    while nbAllumetteJoueur not in range(1,nMax+1):
        nbAllumetteJoueur=int(input("Combien d'allumettes souhaitez-vous retirer (entre 1 et {}) ?".format(nMax)))
    print("Vous avez pris {} allumette(s).".format(nbAllumetteJoueur))
    nAllumette=nAllumette-nbAllumetteJoueur
    if (nAllumette<=0):
        estFini="Vous avez pris la dernière allumette. Vous avez perdu."
    elif (nAllumette==1):
        estFini="L'ordinateur prend la dernière allumette. Vous avez gagné."
    return(nAllumette,estFini)


def tourOrdi(nAllumette,nMax,estFini,niveau):
    """
    - Selon son niveau, l'ordinateur a une certaine probabilité de répondre aléatoirement
    - on modifie l'état de la partie (via la variable estFini).
    """
    print("\n***Tour de l'ordinateur. Allumettes disponibles :"+"|"*nAllumette)
    if niveau>randint(1,10):
        nbAllumetteOrdinateur=nMax-(-nAllumette%(nMax+1)) #to do: verifier sur papier que ce "reste"  convient bien
        if nbAllumetteOrdinateur==0:
            nbAllumetteOrdinateur=randint(1,nMax+1)
    else:
        nbAllumetteOrdinateur=randint(1,nMax+1)
    print("L'ordinateur prend {} allumettes.\n".format(nbAllumetteOrdinateur))
    nAllumette=nAllumette-nbAllumetteOrdinateur
    if nAllumette==1:
        estFini="Vous devez prendre la dernière allumette. Vous avez perdu."
    elif nAllumette<=0:
        estFini="L'ordinateur a pris la dernière allumette...Vous avez gagné !"
    return(nAllumette,estFini)
