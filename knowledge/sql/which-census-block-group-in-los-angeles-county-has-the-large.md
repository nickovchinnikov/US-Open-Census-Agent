---
nl: Which census block group in Los Angeles County has the largest population?
sql: SELECT a.CENSUS_BLOCK_GROUP, a.B01001e1 AS total_population FROM census_2019_age_sex
  AS a JOIN census_2019_county_fips AS f ON SUBSTRING(a.CENSUS_BLOCK_GROUP, 1, 2)
  = f.STATE_FIPS AND SUBSTRING(a.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE
  = 'CA' AND f.COUNTY = 'Los Angeles County' AND a.B01001e1 IS NOT NULL ORDER BY total_population
  DESC LIMIT 1
source: user
tags:
- source:verified-census-query
---
