-- TD Marches
-- Copyright (C) 2021  Faholan <https://github.com/Faholan>

SELECT COUNT(*) FROM Participant WHERE ne >= 1999 AND ne <= 2003 ;;

SELECT diff, AVG(duree) FROM Rando GROUP BY diff ;;

SELECT pnom FROM Participant WHERE diff_max < (SELECT diff FROM Rando WHERE rid = 42) ;;

SELECT MIN(rid) AS rid, rnom FROM Rando HAVING COUNT(*) > 1 GROUP BY rnom ;;
