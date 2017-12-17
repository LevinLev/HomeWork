select City.Name, City.Population as "CityPopulation", Country.Population as "CountryPopulation"
from City
join Country on City.CountryCode=Country.Code
order by City.Population/Country.Population desc, City.Name desc
limit 20;
