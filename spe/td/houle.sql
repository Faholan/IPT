-- Question 19
SELECT idBouee, nomSite FROM Bouee WHERE localisation='Mediterranee' ;

SELECT idBouee FROM Bouee WHERE idBouee NOT IN (SELECT idBouee FROM Tempete) ;

SELECT MAX(Hmax) AS Htop, nomSite FROM Tempete INNER JOIN Bouee USING (idBouee) GROUP BY nomSite ;
SELECT MAX(Hmax) AS Htop, nomSite FROM Tempete NATURAL JOIN Bouee GROUP BY nomSite ;
