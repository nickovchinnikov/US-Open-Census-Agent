---
nl: How many occupied housing units are there in Suffolk County, Massachusetts?
sql: SELECT SUM(h.B25002e2) AS occupied_housing_units FROM census_2019_housing AS
  h JOIN census_2019_county_fips AS f ON SUBSTRING(h.CENSUS_BLOCK_GROUP, 1, 2) = f.STATE_FIPS
  AND SUBSTRING(h.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE = 'MA' AND
  f.COUNTY = 'Suffolk County'
source: user
---
