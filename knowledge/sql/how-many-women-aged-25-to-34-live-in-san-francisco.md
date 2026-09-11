---
nl: How many women aged 25 to 34 live in San Francisco?
sql: SELECT SUM(a.B01001e35 + a.B01001e36) AS estimated_women_age_25_to_34 FROM census_2019_age_sex
  AS a JOIN census_2019_county_fips AS f ON SUBSTRING(a.CENSUS_BLOCK_GROUP, 1, 2)
  = f.STATE_FIPS AND SUBSTRING(a.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE
  = 'CA' AND f.COUNTY = 'San Francisco County'
source: user
tags:
- source:verified-census-query
---
