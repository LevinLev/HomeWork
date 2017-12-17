SELECT Country.Name, COUNT(ALL Country.Name) AS Megalopolises
FROM Country
LEFT JOIN City ON Country.Code = City.CountryCode
WHERE City.Population >= 1000000
GROUP BY Country.Name
ORDER BY Megalopolises desc;
