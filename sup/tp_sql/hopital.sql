-- Clés étrangères :

-- Table service

-- FOREIGN KEY (DIRECTEUR) REFERENCES docteur(NUMERO)

-- Table chambre

-- FOREIGN KEY (CODE_SERVICE) REFERENCES service(CODE)
-- FOREIGN KEY (SURVEILLANT) REFERENCES infirmier(NUMERO)

-- Table employe

-- Table docteur
-- FOREIGN KEY (NUMERO) REFERENCES employe(NUMERO)

-- Table infirmier
-- FOREIGN KEY (NUMERO) REFERENCES employe(NUMERO)
-- FOREIGN KEY (CODE_SERVICE) REFERENCES service(CODE)

-- Table hospitalisation
-- FOREIGN KEY (NO_MALADE) REFERENCES malade(NUMERO)
-- FOREIGN KEY (CODE_SERVICE) REFERENCES service(CODE)
-- FOREIGN KEY (NO_CHAMBRE) REFERENCES chambre(NO_CHAMBRE)

-- ou :
-- FOREIGN KEY (CODE_SERVICE, NO_CHAMBRE) REFERENCES chambre(CODE_SERVICE, NO_CHAMBRE)

-- Table soigne
-- FOREIGN KEY (NO_DOCTEUR) REFERENCES docteur(NUMERO)
-- FOREIGN KEY (NO_MALADE) REFERENCES malade(NUMERO)

-- R1

SELECT prenom, nom FROM malade
    WHERE mutuelle='MAAF'
;

-- R2

SELECT prenom, nom FROM infirmier
    INNER JOIN employe USING(numero)
    WHERE rotation='NUIT'
    ORDER BY nom
;

-- R3

SELECT service.nom AS nomservice, batiment, employe.prenom AS prenomdirecteur, employe.nom AS nomdirecteur, specialite FROM service
    INNER JOIN docteur ON service.directeur = docteur.numero
    INNER JOIN employe USING(numero)
    ORDER BY service.nom
;

-- R4

SELECT lit, no_chambre, service.nom AS nomservice, prenom, malade.nom, mutuelle FROM hospitalisation
    INNER JOIN service ON hospitalisation.code_service = service.code
    INNER JOIN malade ON hospitalisation.no_malade = malade.numero
    WHERE batiment = 'B' AND mutuelle LIKE 'MN%'
;

-- R5

SELECT code_service, ROUND(SUM(salaire) / SUM(1), 2) AS moyenne_salaire FROM infirmier
    GROUP BY code_service
    ORDER BY code_service
;

-- R6
SELECT service.nom, ROUND(SUM(nb_lits) / SUM(1), 2) AS moyenne_lits FROM chambre
    INNER JOIN service ON code_service = code
    WHERE service.batiment='A'
    GROUP BY service.nom
    ORDER BY service.nom
;

-- R7
WITH docteurs AS (
    SELECT no_malade, SUM(1) AS docteurs FROM soigne
    GROUP BY no_malade
), specialites AS (
    SELECT no_malade, SUM(1) AS specialites FROM (
        SELECT DISTINCT no_malade, specialite FROM soigne
        INNER JOIN docteur ON no_docteur = numero
    ) AS t
    GROUP BY no_malade
) SELECT nom, prenom, docteurs, specialites FROM docteurs
    INNER JOIN specialites USING(no_malade)
    INNER JOIN malade ON no_malade = malade.numero
    WHERE docteurs > 3
    ORDER BY nom
;

-- R8
WITH infirmier AS (
    SELECT code_service, SUM(1) AS infirmiers FROM infirmier
    GROUP BY code_service
), malades AS (
    SELECT code_service, SUM(1) AS malades FROM hospitalisation
    GROUP BY code_service
) SELECT nom, ROUND(infirmiers::numeric / malades, 4) AS rapport FROM service
    INNER JOIN infirmier ON code_service = code
    INNER JOIN malades USING(code_service)
    ORDER BY nom
;

-- R9
SELECT prenom, nom FROM docteur
    INNER JOIN employe USING(numero)
    WHERE numero IN (
        SELECT no_docteur FROM soigne
        WHERE no_malade IN (
            SELECT no_malade FROM hospitalisation
        )
    )
    ORDER BY nom
;

-- R10
SELECT prenom, nom FROM docteur
    INNER JOIN employe USING(numero)
    WHERE numero NOT IN (
        SELECT no_docteur FROM soigne
        WHERE no_malade IN (
            SELECT no_malade FROM hospitalisation
        )
    )
    ORDER BY nom
;

-- R11
WITH doct_m AS (
    SELECT no_docteur, SUM(1) AS malade FROM soigne
    WHERE no_malade IN (
        SELECT no_malade FROM hospitalisation
    )
    GROUP BY no_docteur
) SELECT prenom, nom, COALESCE(malade, 0) FROM docteur
    INNER JOIN employe USING(numero)
    LEFT OUTER JOIN doct_m ON no_docteur = numero
    ORDER BY nom
;

-- R12

SELECT batiment, no_chambre FROM chambre
INNER JOIN service ON service.code = chambre.code_service
    WHERE (code_service, no_chambre) IN (
        SELECT DISTINCT code_service, no_chambre FROM hospitalisation
    )
;

-- R13

SELECT batiment, no_chambre FROM chambre
    INNER JOIN service ON chambre.code_service = service.code
    WHERE (no_chambre, code_service) NOT IN (
        SELECT no_chambre, code_service FROM hospitalisation
    )
;

-- R14

WITH chambre_malades AS (
    SELECT SUM(1) AS count, code_service, no_chambre FROM hospitalisation GROUP BY (code_service, no_chambre)
) SELECT batiment, no_chambre, nb_lits, COALESCE(count, 0) FROM chambre
    INNER JOIN service ON chambre.code_service = service.code
    LEFT OUTER JOIN chambre_malades USING(code_service, no_chambre)
    ORDER BY (batiment, no_chambre)
;

-- R15

WITH doc_serv AS (
    SELECT SUM(1) AS services, no_docteur FROM (
        SELECT DISTINCT code, no_docteur FROM service
        INNER JOIN hospitalisation ON hospitalisation.code_service = service.code
        INNER JOIN soigne USING(no_malade)
    ) AS t GROUP BY no_docteur
) SELECT prenom, nom FROM docteur
    INNER JOIN employe USING(numero)
    INNER JOIN doc_serv ON docteur.numero = doc_serv.no_docteur
    WHERE services IN (
        SELECT SUM(1) AS services FROM service
    )
    ORDER BY (nom, prenom)
;

-- R16

WITH doc_chambres AS (
    SELECT SUM(1) AS chambres, no_docteur FROM (
        SELECT DISTINCT code_service, no_chambre, no_docteur FROM chambre
        INNER JOIN hospitalisation USING(code_service, no_chambre)
        INNER JOIN soigne USING(no_malade)
        INNER JOIN employe ON chambre.surveillant = employe.numero
        WHERE employe.nom='Roddick'
    ) AS t GROUP BY no_docteur
) SELECT prenom, nom FROM docteur
    INNER JOIN employe USING(numero)
    INNER JOIN doc_chambres ON docteur.numero = doc_chambres.no_docteur
    WHERE chambres IN (
        SELECT SUM(1) AS chambres FROM chambre
        INNER JOIN employe ON chambre.surveillant = employe.numero
        WHERE employe.nom='Roddick'
    )
;

-- R17

SELECT prenom, malade.nom FROM hospitalisation
    INNER JOIN malade ON malade.numero = hospitalisation.no_malade
    INNER JOIN soigne USING(no_malade)
    INNER JOIN service ON service.code = hospitalisation.code_service
    wHERE no_docteur = directeur
    ORDER BY nom
;

-- R18

WITH malade_chambre AS (
    SELECT SUM(1) AS malades, no_chambre FROM hospitalisation
    INNER JOIN service ON hospitalisation.code_service = service.code
    WHERE nom='Cardiologie'
    GROUP BY no_chambre
) SELECT no_chambre FROM chambre
    INNER JOIN service ON service.code = chambre.code_service
    LEFT OUTER JOIN malade_chambre USING(no_chambre)
    WHERE nom='Cardiologie' AND malades != nb_lits
;
