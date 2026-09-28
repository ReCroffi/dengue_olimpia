-- 1. Casos por ano
SELECT SE // 100  AS ano , SUM(casos) AS casos_por_ano FROM dengue_olimpia
GROUP BY ano 
ORDER BY ano DESC;