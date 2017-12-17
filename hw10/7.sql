SELECT Country.Name
FROM Country
LEFT JOIN City ON Country.Code = City.CountryCode
GROUP BY Country.Name
HAVING (2 * SUM(City.Population) < Country.Population) OR (SUM(City.Population) IS NULL) AND Country.Population > 0
ORDER BY Country.Name;
