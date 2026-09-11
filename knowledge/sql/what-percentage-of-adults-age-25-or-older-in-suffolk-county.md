---
nl: What percentage of adults age 25 or older in Suffolk County, Massachusetts have
  a bachelor's degree or higher?
sql: SELECT 100.0 * (SUM(e.B15003e22) + SUM(e.B15003e23) + SUM(e.B15003e24) + SUM(e.B15003e25))
  / NULLIF(SUM(e.B15003e1), 0) AS bachelors_or_higher_pct_age_25_plus FROM census_2019_education
  AS e JOIN census_2019_county_fips AS f ON SUBSTRING(e.CENSUS_BLOCK_GROUP, 1, 2)
  = f.STATE_FIPS AND SUBSTRING(e.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE
  = 'MA' AND f.COUNTY = 'Suffolk County'
source: user
tags:
- source:verified-census-query
---
