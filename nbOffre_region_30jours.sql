SELECT region.nom as nom_region,
region.code_reg as reg_code,
count(*) as nb_offre
FROM offre
INNER JOIN ville ON ville.code_insee = offre.ville 
INNER JOIN region ON region.code_reg = offre.region
WHERE offre.Date_publication > current_timestamp - interval '30 day'
GROUP BY nom_region, reg_code
ORDER BY nb_offre DESC;