SELECT City.Name
FROM Capital
JOIN City ON Capital.CityId = City.Id
JOIN Country ON Capital.CountryCode = Country.Code
WHERE Country.Name = "Malaysia";
