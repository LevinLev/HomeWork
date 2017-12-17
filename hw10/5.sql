SELECT GovernmentForm, SUM(SurfaceArea) AS Surface
FROM Country
GROUP BY GovernmentForm
ORDER BY Surface DESC
limit 1;
