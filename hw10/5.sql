select GovernmentForm, sum(SurfaceArea) as "TotalSurfaseArea"
from Country
group by GovernmentForm
order by "totalSurfaseArea" desc
limit 1;
