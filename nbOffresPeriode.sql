SELECT date_trunc('day', Date_publication) as jour, COUNT(*) as nb
FROM Offre
GROUP BY jour;

SELECT date_trunc('month', Date_publication) as mois, COUNT(*) as nb
FROM Offre
GROUP BY mois;
