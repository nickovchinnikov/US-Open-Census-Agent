---
nl: Which Indiana counties had the highest unemployment rate in 2019?
sql: SELECT f.COUNTY, 100.0 * SUM(e.B23025e5) / NULLIF(SUM(e.B23025e3), 0) AS unemployment_rate_pct
  FROM census_2019_employment AS e JOIN census_2019_county_fips AS f ON SUBSTRING(e.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(e.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'IN' GROUP BY f.COUNTY ORDER BY unemployment_rate_pct DESC LIMIT 10
source: user
tags:
- source:verified-census-query
---
