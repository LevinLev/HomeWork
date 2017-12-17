select City.Name
from Capital
join City on Capital.CityId=City.Id
join Country on Capital.CountryCode=Country.Code
where Country.Name="Malaysia";
