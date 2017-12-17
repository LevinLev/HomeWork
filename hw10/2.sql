select Country.Name, LiteracyRate.Rate
from LiteracyRate
join Country on LiteracyRate.CountryCode=Country.Code
group by Country.Name
having max(LiteracyRate.Year)
order by LiteracyRate.Rate desc
limit 1;
