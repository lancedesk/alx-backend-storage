-- Query to list bands with Glam rock style ranked by longevity	
SELECT
    band_name,
    (IFNULL(split, YEAR(CURDATE()) - 1) - formed) AS lifespan
FROM
    metal_bands
WHERE
    FIND_IN_SET('Glam rock', style) > 0
ORDER BY
    lifespan DESC;
