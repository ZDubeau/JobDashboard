SELECT intitule.nom as nom_intitule,
COUNT(*) as nb_offre 
FROM offre 
INNER JOIN intitule ON intitule.id = offre.intitule
GROUP BY nom_intitule
ORDER BY nom_intitule;
***********************************************************************1
SELECT intitule.nom as nom_intitule,
COUNT(*) as nb_offre, 
date_trunc('day', offre.date_publication) as jour
FROM offre 
INNER JOIN intitule ON intitule.id = offre.intitule
WHERE offre.Date_publication > current_timestamp - interval '1 day'
GROUP BY nom_intitule, jour
ORDER BY jour;
************************************************************************2
SELECT intitule.nom as nom_intitule,
COUNT(*) as nb_offre, 
date_trunc('week', offre.date_publication) as semaine
FROM offre 
INNER JOIN intitule ON intitule.id = offre.intitule
WHERE offre.Date_publication > current_timestamp - interval '7 day'
GROUP BY nom_intitule, semaine
ORDER BY semaine;
************************************************************************3
SELECT intitule.nom as nom_intitule,
COUNT(*) as nb_offre, 
date_trunc('month', offre.date_publication) as mois
FROM offre 
INNER JOIN intitule ON intitule.id = offre.intitule
WHERE offre.Date_publication > current_timestamp - interval '30 day'
GROUP BY nom_intitule, mois
ORDER BY mois;
************************************************************************4
SELECT intitule.nom as nom_intitule,
region.nom as nom_region,
COUNT(*) as nb_offre
FROM offre
INNER JOIN region ON region.code_reg = offre.region
INNER JOIN ville ON ville.code_insee = offre.ville
INNER JOIN intitule ON intitule.id = offre.intitule
GROUP BY nom_intitule, nom_region
ORDER BY nom_region;  
************************************************************************5
SELECT intitule.nom as nom_intitule,
ville.nom as nom_ville,
COUNT(*) as nb_offre,
ville.latitude as lat,
ville.longitude as lng
FROM offre 
INNER JOIN ville ON ville.code_insee = offre.ville
INNER JOIN intitule ON intitule.id = offre.intitule
GROUP BY nom_intitule, nom_ville, lat, lng
ORDER BY nom_ville;
************************************************************************6