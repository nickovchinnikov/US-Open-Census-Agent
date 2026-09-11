---
nl: How many households in Travis County, Texas earn less than $25,000 per year?
sql: SELECT SUM(i.B19001e2) + SUM(i.B19001e3) + SUM(i.B19001e4) + SUM(i.B19001e5)
  AS estimated_households_income_under_25k FROM census_2019_income AS i JOIN census_2019_county_fips
  AS f ON SUBSTRING(i.CENSUS_BLOCK_GROUP, 1, 2) = f.STATE_FIPS AND SUBSTRING(i.CENSUS_BLOCK_GROUP,
  3, 3) = f.COUNTY_FIPS WHERE f.STATE = 'TX' AND f.COUNTY = 'Travis County'
source: user
tags:
- source:verified-census-query
---
