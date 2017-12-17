SELECT City.Name, City.Population AS "CityPopulation", Country.Population AS "CountryPopulation"
FROM City
JOIN Country ON City.CountryCode = Country.Code
ORDER BY 100 * City.Population/Country.Population desc, City.Name desc
limit 20;
