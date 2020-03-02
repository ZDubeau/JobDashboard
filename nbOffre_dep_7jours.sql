SELECT ville.code_dep as dep_code,
count(*) as nb_offre
FROM offre
INNER JOIN ville ON ville.code_insee = offre.ville 
INNER JOIN region ON region.code_reg = offre.region
WHERE offre.Date_publication > current_timestamp - interval '7 day'
GROUP BY dep_code
ORDER BY nb_offre DESC;