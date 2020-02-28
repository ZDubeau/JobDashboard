SELECT region.nom as nom_region,
ville.nom as nom_ville,
count(*) as nb_offre,
offre.Date_publication as date_pub,
ville.latitude as lat,
ville.longitude as lng
FROM offre 
INNER JOIN ville ON ville.code_insee = offre.ville 
INNER JOIN region ON region.code_reg = offre.region
GROUP BY nom_region, nom_ville, date_pub, lat, lng
HAVING offre.Date_publication > current_timestamp - interval '30 day'
ORDER BY nb_offre DESC;