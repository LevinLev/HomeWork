select Country.Name, Country.Population
from Country
left join City on Country.Code=City.CountryCode
group by Country.Name
having sum(City.Population) < (Country.Population - sum(City.Population)) or (City.Population is null) and Country.Population > 0
order by Country.Name;
