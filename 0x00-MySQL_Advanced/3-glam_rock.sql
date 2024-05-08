-- List glam rock bands ranked by longevity
SELECT band_name, 
       IF(LOCATE('-', formed) > 0 AND LOCATE('-', split) > 0, 
          SUBSTRING_INDEX(split, '-', 1) - SUBSTRING_INDEX(formed, '-', 1),
          2022 - CAST(formed AS UNSIGNED)) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
