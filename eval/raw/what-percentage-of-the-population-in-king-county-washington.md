---
nl: What percentage of the population in King County, Washington is female?
sql: SELECT 100.0 * SUM(a.B01001e26) / NULLIF(SUM(a.B01001e1), 0) AS female_population_pct
  FROM census_2019_age_sex AS a JOIN census_2019_county_fips AS f ON SUBSTRING(a.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(a.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'WA' AND f.COUNTY = 'King County'
source: user
tags:
- source:verified-census-query
---
