---
nl: Compare the number of men and women living in Suffolk County, Massachusetts.
sql: SELECT SUM(a.B01001e2) AS estimated_men, SUM(a.B01001e26) AS estimated_women,
  SUM(a.B01001e26) - SUM(a.B01001e2) AS women_minus_men FROM census_2019_age_sex AS
  a JOIN census_2019_county_fips AS f ON SUBSTRING(a.CENSUS_BLOCK_GROUP, 1, 2) = f.STATE_FIPS
  AND SUBSTRING(a.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE = 'MA' AND
  f.COUNTY = 'Suffolk County'
source: user
tags:
- source:verified-census-query
---
