select Country.Name, count(all Country.Name) as "Megalopolises"
from Country
left join City on Country.Code=City.CountryCode
where City.Population>999999
group by Country.Name
order by Megalopolises desc;
