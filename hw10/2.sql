select Country.Name
from City
join Country on City.CountryCode=Country.Code
group by Country.Name
having sum(City.Population)<Country.Population
order by Country.Name;
