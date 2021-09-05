--
-- Création des tables --
--

CREATE TABLE joueurs (
    nom VARCHAR(30) PRIMARY KEY,
    prenom VARCHAR(30) NOT NULL,
    age SMALLINT NOT NULL,
    nationalite VARCHAR(30) NOT NULL
);

CREATE TABLE tournoi (
    nom VARCHAR(30) PRIMARY KEY,
    pays VARCHAR(30) NOT NULL
);

CREATE TABLE gain (
    nomjoueur VARCHAR(30) NOT NULL,
    nomtournoi VARCHAR(30) NOT NULL,
    annee INTEGER NOT NULL,
    rang VARCHAR(30) NOT NULL,
    prime BIGINT NOT NULL,
    PRIMARY KEY (nomjoueur, nomtournoi, annee),
    FOREIGN KEY (nomjoueur) REFERENCES joueurs(nom),
    FOREIGN KEY (nomtournoi) REFERENCES tournoi(nom)
);

CREATE TABLE rencontre (
    nomgagnant VARCHAR(30) NOT NULL,
    nomperdant VARCHAR(30) NOT NULL,
    nomtournoi VARCHAR(30) NOT NULL,
    annee INTEGER NOT NULL,
    score VARCHAR(30) NOT NULL,
    PRIMARY KEY (nomgagnant, nomperdant, nomtournoi, annee),
    FOREIGN KEY (nomgagnant) REFERENCES joueurs(nom),
    FOREIGN KEY (nomperdant) REFERENCES joueurs(nom),
    FOREIGN KEY (nomtournoi) REFERENCES tournoi(nom)
);

CREATE TABLE sponsors (
    nom VARCHAR(30) NOT NULL,
    nomtournoi VARCHAR(30) NOT NULL,
    annee INTEGER NOT NULL,
    montant BIGINT NOT NULL,
    PRIMARY KEY (nom, nomtournoi, annee),
    FOREIGN KEY (nomtournoi) REFERENCES tournoi(nom)
);

--
-- Insertion des valeurs --
--

INSERT INTO joueurs VALUES
    ('Nadal', 'Rafael', 31, 'Espagnol'),
    ('Federer', 'Roger', 35, 'Suisse'),
    ('Djokovic', 'Novac', 34, 'Serbe'),
    ('Murray', 'Andy', 34, 'Brittanique'),
    ('Wawrinka', 'Stanislas', 37, 'Suisse'),
    ('Raonic', 'Robert', 34, 'Malgache')
;

INSERT INTO tournoi VALUES
    ('Roland Garros', 'France'),
    ('US Open', 'US'),
    ('Wimbledon', 'Royaume-Uni'),
    ('Open d Australie', 'Australie')
;

INSERT INTO sponsors VALUES
    ('BNP-Paribas', 'Roland Garros', 2017, 9000000),
    ('BNP-Paribas', 'Roland Garros', 2016, 10000000)
;

INSERT INTO rencontre VALUES
    ('Nadal', 'Wawrinka', 'Roland Garros', 2017, '6/2 - 6/3 - 6/1'),
    ('Djokovic', 'Murray', 'Roland Garros', 2016, '3/6 - 6/1 - 6/2 - 6/4'),
    ('Wawrinka', 'Djokovic', 'US Open', 2016, '6/7 - 6/4 - 7/5 - 6/3'),
    ('Murray', 'Raonic', 'Wimbledon', 2016, '6/4 - 7/6 - 7/6'),
    ('Djokovic', 'Murray', 'Open d Australie')
;

INSERT INTO gain
    SELECT nomgagnant, nomtournoi, annee, 'gagnant', 1000000 FROM rencontre
;

INSERT INTO gain
    SELECT nomperdant, nomtournoi, annee, 'finaliste', 500000 FROM rencontre
;

--
-- Interrogations --
--

SELECT nom, prenom FROM joueurs WHERE prenom='Roger' ;

SELECT annee FROM rencontre WHERE nomtournoi='Roland Garros' ;

SELECT nom, age FROM joueurs
    INNER JOIN rencontre ON nomgagnant = nom
    WHERE nomtournoi='Roland Garros'
;

SELECT nom, prenom FROM joueurs WHERE nom IN (
    SELECT nomgagnant FROM rencontre
    INNER JOIN sponsors USING(nomtournoi, annee)
    WHERE sponsors.nom='BNP-Paribas'
);

--
-- Interrogations ensemblistes ou imbriquées -
--

SELECT nomgagnant AS nom FROM rencontre UNION SELECT nomperdant FROM rencontre ;

WITH sauce AS (
    SELECT nomgagnant, nomperdant FROM rencontre WHERE nomtournoi='Wimbledon'
) SELECT nomgagnant FROM sauce UNION SELECT nomperdant FROM sauce ;

SELECT nom FROM joueurs WHERE nom NOT IN (
    SELECT nomperdant FROM rencontre
);

SELECT nom FROM joueurs WHERE nom NOT IN (
    SELECT nomjoueur FROM gain WHERE prime < 1000000
);

SELECT SUM(prime) AS gaintotal FROM gain WHERE nomjoueur='Nadal' ;

SELECT SUM(prime) AS gaintotal, nomjoueur FROM gain WHERE SUM(prime) >= 2000000 ;

WITH sauce AS (
    SELECT nomjoueur AS nom, SUM(prime) AS gaintotal FROM gain GROUP BY nomjoueur
) SELECT nom, gaintotal FROM sauce WHERE gaintotal >= 2000000 ;

WITH verse AS (
  SELECT nomtournoi AS nom, SUM(montant) AS verse, annee FROM sponsors GROUP BY annee, nomtournoi
), recus AS (
  SELECT SUM(prime) AS recus, annee FROM gain GROUP BY annee
) SELECT nom, annee FROM verse INNER JOIN recus USING(annee) WHERE verse >= recus ;
