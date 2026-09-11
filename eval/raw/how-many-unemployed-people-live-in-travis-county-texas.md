---
nl: How many unemployed people live in Travis County, Texas?
sql: SELECT SUM(e.B23025e5) AS estimated_unemployed_people FROM census_2019_employment
  AS e JOIN census_2019_county_fips AS f ON SUBSTRING(e.CENSUS_BLOCK_GROUP, 1, 2)
  = f.STATE_FIPS AND SUBSTRING(e.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE
  = 'TX' AND f.COUNTY = 'Travis County'
source: user
---
