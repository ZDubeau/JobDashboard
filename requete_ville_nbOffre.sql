SELECT ville.nom as nom_ville, COUNT(*) as nb_offre, 
    offre.date_publication as date_pub, 
    ville.latitude as lat, ville.longitude as lng 
FROM offre 
INNER JOIN ville ON ville.code_insee = offre.ville 
GROUP BY nom_ville, date_pub, lat, lng;