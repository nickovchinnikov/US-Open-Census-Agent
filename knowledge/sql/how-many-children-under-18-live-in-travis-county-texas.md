---
nl: How many children under 18 live in Travis County, Texas?
sql: SELECT SUM(a.B01001e3) + SUM(a.B01001e4) + SUM(a.B01001e5) + SUM(a.B01001e6)
  + SUM(a.B01001e27) + SUM(a.B01001e28) + SUM(a.B01001e29) + SUM(a.B01001e30) AS estimated_children_under_18
  FROM census_2019_age_sex AS a JOIN census_2019_county_fips AS f ON SUBSTRING(a.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(a.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'TX' AND f.COUNTY = 'Travis County'
source: user
tags:
- source:verified-census-query
---
