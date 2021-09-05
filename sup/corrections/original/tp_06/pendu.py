# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 18:23:40 2013

@author: test
"""
#from string
from numpy.random import randint

dico=["abracadabra","hxquatre","gilet","jaune","ordinateur","pendu","caillou"]
#on fabrique un petit dico pour varier un peu les mots à chercher

def motTrouve(motSecret,lettreEssaye):
    """
    - vérifie si le mot cherché est trouvé. Retourne un booléen
    """
    estTrouve=True
    for lettre in motSecret:
        if lettre not in lettreEssaye:
            estTrouve=False
    return estTrouve

def entreLettre(lettreEssaye):
    """
    -recupère une lettre, après avoir testé la nature de ce qui est rentré en console
    """
    while True:
        essai=input("A vous de jouer ! Entrez une lettre\n")
        essai=essai.lower() #passe en minuscule le caractère
        if essai=="":
            print("il faut entrer quelque chose")
        elif len(essai)!=1 :
            print("il faut entrer une seule lettre")
        elif not(essai.isalpha()):#moins élégant mais fonctionne aussi : elif essai not in "azertyuiopqsdfghjklmwxcvbn"
            print("il faut écrire une lettre")
        elif essai in lettreEssaye:
            print("Vous avez déjà proposé cette lettre. Choisissez en une autre")
        else:
            return essai #on sort de la boucle 'while' et on renvoie la lettre choisie

def affichageResultat(motSecret,lettreEssaye,nbErreur,erreurMax):
    """
    -affiche l'état de la partie
    """
    mauvaiseLettre=[]
    for lettre in lettreEssaye:
        if lettre not in motSecret:
            mauvaiseLettre.append(lettre)
    print("Vous avez déjà testé les lettres suivantes :",mauvaiseLettre)
    motPartiel=motSecret
    for lettre in motSecret:
        if lettre not in lettreEssaye:
            motPartiel=motPartiel.replace(lettre,"-")
    print("L'état actuel du mot recherché est : {}".format(motPartiel))
    nbEssaiRestant=erreurMax-nbErreur
    print("Vous avez encore droit à {} erreur(s)".format(nbEssaiRestant))


def introduction(motSecret):
    """
    - affiche la longueur du mot cherché
    - récupère le nombre d'erreurs maximal. On vérifie que le joueur rentre bien un nombre
    """
    print("Bienvenu dans le jeu du pendu.")
    print("Vous cherchez un mot de {} lettres".format(len(motSecret)))
    while True:
        nbErrMax=input("Choisissez le nombre d'erreur maximal\n")
        if nbErrMax=="":
            print("il faut entrer quelque chose")
        elif not(nbErrMax.isdigit()):
            print("il faut écrire un nombre")
        else:
            return int(nbErrMax)


def pendu():
    """
    -choisit le mot secret de façon aléatoire parmi une liste prédéfinie
    -fait appel aux diverses fonctions...
    -affiche un message à la fin de la partie
    """
    motSecret=dico[randint(0,(len(dico)))]
    lettreEssaye=[]
    nbErreur=0
    erreurMax=introduction(motSecret)
    while nbErreur<=erreurMax and not motTrouve(motSecret,lettreEssaye):
        affichageResultat(motSecret,lettreEssaye,nbErreur,erreurMax)
        newLettre=entreLettre(lettreEssaye)
        lettreEssaye.append(newLettre)
        if newLettre in motSecret:
            print("Vous avez trouvé une nouvelle lettre du mot secret!")
        else:
            nbErreur+=1
            print("La lettre '{}' n'est pas dans le mot secret".format(newLettre))
    if nbErreur==erreurMax+1:
        print("Vous avez perdu!")
        print("Le mot secret était : "+motSecret)
    else:
        print("Bravo! Vous avez trouvé le mot secret : "+motSecret)
