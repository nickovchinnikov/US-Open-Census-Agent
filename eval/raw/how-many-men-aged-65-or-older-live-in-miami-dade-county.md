---
nl: How many men aged 65 or older live in Miami-Dade County?
sql: SELECT SUM(a.B01001e20) + SUM(a.B01001e21) + SUM(a.B01001e22) + SUM(a.B01001e23)
  + SUM(a.B01001e24) + SUM(a.B01001e25) AS estimated_men_age_65_or_older FROM census_2019_age_sex
  AS a JOIN census_2019_county_fips AS f ON SUBSTRING(a.CENSUS_BLOCK_GROUP, 1, 2)
  = f.STATE_FIPS AND SUBSTRING(a.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE
  = 'FL' AND f.COUNTY = 'Miami-Dade County'
source: user
tags:
- source:verified-census-query
---
