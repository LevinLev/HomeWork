select result.Name, result.Rate
from (
select Country.Name, LiteracyRate.Rate, max(LiteracyRate.Year)
from LiteracyRate
join Country on LiteracyRate.CountryCode=Country.Code
group by Country.Name
) as result
order by LiteracyRate.Rate desc
limit 1;
