-- Question 14
SELECT sc_nom FROM Scene WHERE EXTRACT(year FROM sc_creation) = '2021' ;

-- Question 15
SELECT sc_id, COUNT(sc_id) AS num_src FROM Source GROUP BY sc_id ;

-- Question 16
SELECT sp_id, ob_x, ob_y, ob_z, sp_rayon FROM Objet
    JOIN Sphere ON Sphere.sp_id = Objet.ob_id
    JOIN Scene USING (sc_id) WHERE sc_nom = 'woodbox'
;

-- Question 17
SELECT Objet_a.ob_id AS objr_id,
    so_id,
    Objet_b.ob_id AS objo_id
    FROM Objet AS Objet_a
    JOIN Objet AS Objet_b ON Objet_a.sc_id = Objet_b.sc_id
    JOIN Source ON Objet_a.sc_id = Source.sc_id
    JOIN Scene ON Objet_a.sc_id = Scenea.sc_id
    WHERE sc_nom = 'woodbox' AND OCCULTE(sc_id, Objet_a.ob_id, so_id, Objet_b.ob_id)
;
