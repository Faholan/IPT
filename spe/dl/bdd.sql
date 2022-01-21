-- Problème 1

-- Question 1
/*
Astre : PRIMARY KEY (nomAstre)
Planète : PRIMARY KEY (nomAstre, nomPlanète)
Astrophysicien : PRIMARY KEY (nom, prénom)
Astéroïde : PRIMARY KEY (nomAstéroïde)
Collision : PRIMARY KEY (nomAstre, nomPlanète, nomAstéroïde)
*/

-- Question 2
/*
Planète :
    FOREIGN KEY nomAstre REFERENCES Astre.nomAstre
Astéroïde :
    FOREIGN KEY nom REFERENCES Astrophysicien.nom ;
    FOREIGN KEY prénom REFERENCES Astrophysicien.prénom
Collision :
    FOREIGN KEY nomAstre REFERENCES Astre.nomAstre ;
    FOREIGN KEY nomPlanète REFERENCES Planète.nomPlanète ;
    FOREIGN KEY nomAstéroïde REFERENCES Astéroïde.nomAstéroïde
*/

-- Question 3
-- a
SELECT nomAstre
    FROM Astre
    WHERE diamètre > 1000000
;

-- b
SELECT nomPlanète
    FROM Planète
    WHERE nomAstre = 'Soleil'
        AND tempsRévolution > 500
;

-- Question 4
-- a
SELECT DISTINCT nom, prénom
    FROM Astéroïde
;

-- b
SELECT nom, prénom
    FROM Astrophysicien
    WHERE (nom, prénom) NOT IN (
        SELECT nom, prénom
        FROM Astéroïde
    )
;

-- c
SELECT nomAstre
    FROM Astre
    WHERE nomAstre NOT IN (
        SELECT nomAstre
        FROM Planète
        WHERE nomAstre, nomPlanète NOT IN (
            SELECT nomAstre, nomPlanète
            FROM Collision
        )
    )
;

-- Question 5
-- a
SELECT nom, prénom, COUNT(nomAstéroïde)
    FROM Astrophysicien
    LEFT JOIN Astéroïde USING (nom, prénom)
    GROUP BY (nom, prénom)
;

-- b
SELECT nomAstre
    FROM Astre
    JOIN (
        SELECT nomAstre, COUNT(*) AS num_planetes
        FROM Planète
        GROUP BY nomAstre
    ) AS Planètes_num USING (nomAstre)
    HAVING num_planetes = MAX(num_planetes)
;

-- c
SELECT nomAstre, nomPlanète
    FROM Planète
    JOIN (
        SELECT nomAstre, nomPlanète, COUNT(*) AS num_collisions
        FROM Collision
        GROUP BY (nomAstre, nomPlanète)
    ) AS Collisions_num USING (nomAstre, nomPlanète)
    HAVING num_collisions = MAX(num_collisions)
;


-- Problème 2

CREATE TABLE Fabricant (
    Numero INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL
) ;

CREATE TABLE Produit (
    Numero INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL,
    Prix INTEGER NOT NULL,
    FOREIGN KEY Numfab REFERENCES Fabricant.Numero
) ;

CREATE TABLE Client (
    Numero INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL,
    Prenom TEXT NOT NULL,
    DateNaissance DATE,
    Ville TEXT,
    Adresse TEXT
) ;

CREATE TABLE Commande (
    FOREIGN KEY Numclient REFERENCES Client.Numero,
    FOREIGN KEY Numproduit REFERENCES Produit.Numero,
    Date DATE NOT NULL,
    Quantite INTEGER NOT NULL
) ;

ALTER TABLE Commande ADD CONSTRAINT Commande_primary
    PRIMARY KEY (Numclient, Numproduit, Date)
;

-- Question 1
-- Table fabricant : Numero
-- Table Produit : Numero
-- Table Client : Numero
-- Table Command : Numclient, Numproduit, Date

-- Question 2

-- |    Client     |                       |  Commande  |
-- |---------------|                       |------------|
-- |     Numero    |-----------------------| Numclient  |
-- |      Nom      |                 |-----| Numproduit |
-- |    Prenom     |                 |     |    Date    |
-- | DateNaissance |                 |     |  Quantite  |
-- |     Ville     |                 |
-- |    Adresse    |                 |
--                                   |
--                                   |
--                    | Produit|     |
--                    |--------|     |
--                    | Numero |-----|
-- | Fabricant |      |  Nom   |
-- |-----------|      |  Prix  |
-- |   Numero  |------| Numfab |
-- |    Nom    |

-- Question 3
SELECT COUNT(Numero) AS n
    FROM Client
;

-- Question 4
SELECT Nom, Prenom
    FROM Client
    ORDER BY Nom ASC, Prenom ASC
;

-- Question 5
SELECT UNIQUE Nom, Prenom
    FROM Client JOIN (
        SELECT Numclient, Numproduit, COUNT(*) AS num_commands
        FROM Commande
        GROUP BY Numclient, Numproduit
    ) AS Commande_sum ON Commande_sum.Numclient = Client.Numero
    GROUP BY (Nom, Prenom)
    HAVING MAX(num_commands) > 1
;

-- Question 6
SELECT Numero, Nom
    FROM Produit
    WHERE Nom LIKE '%ski%'
;

-- Question 7
SELECT Numclient, Date, SUM(Quantite * Prix) AS Prix_total
    FROM Commande
    JOIN Produit ON Commande.Numproduit = Produit.Numero
    GROUP BY (Numclient, Date)
    ORDER BY Date ASC
;

-- Question 8
SELECT Nom, Prenom, Date, SUM(Quantite * Prix) AS Prix_total
    FROM Commande
    JOIN Produit ON Commande.Numproduit = Produit.Numero
    JOIN Client ON Command.Numclient = Client.Numero
    GROUP BY (Numclient, Date)
    ORDER BY Date ASC
;

-- Question 9
SELECT Nom, Prenom, COUNT(*) AS num_commands
    FROM Client JOIN Commande ON Client.Numero = Commande.Numclient
    GROUP BY Client.numero
    ORDER BY DateNaissance ASC
;

-- Question 10
SELECT Nom, Prenom, SUM(Quantite * Prix) AS prix_commandes
    FROM Client JOIN Commande ON Client.Numero = Commande.Numclient
    JOIN Produit ON Commande.Numproduit = Produit.Numero
    GROUP BY Client.numero
    ORDER BY nom ASC, prenom ASC
;

-- Question 11
SELECT UNIQUE Fabricant.Nom
    FROM Fabricant
    JOIN Produit ON Fabricant.Numero = Produit.Numfab
    JOIN Commande ON Produit.Numero = Commande.Numproduit
    JOIN Client ON Commande.Numclient = Client.Numero
    WHERE Client.Nom = 'Florian Chivé'
;

-- Question 12
SELECT Client.Nom, Prenom, SUM(Quantite * Prix) AS Prix_Apple
    FROM Client
    JOIN Commande ON Client.Numero = Commande.Numclient
    JOIN Produit ON Commande.Numproduit = Produit.Numero
    JOIN Fabricant ON Produit.Numfab = Fabricant.Numero
    WHERE Fabricant.Nom = 'Apple'
    GROUP BY Client.Numero
    ORDER BY (Client.Nom, Prenom) DESC
;
