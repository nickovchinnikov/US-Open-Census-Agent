---
nl: How many people age 25 or older in Cook County, Illinois have a bachelor's degree
  or higher?
sql: SELECT SUM(e.B15003e22) + SUM(e.B15003e23) + SUM(e.B15003e24) + SUM(e.B15003e25)
  AS estimated_people_age_25_plus_bachelors_or_higher FROM census_2019_education AS
  e JOIN census_2019_county_fips AS f ON SUBSTRING(e.CENSUS_BLOCK_GROUP, 1, 2) = f.STATE_FIPS
  AND SUBSTRING(e.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE = 'IL' AND
  f.COUNTY = 'Cook County'
source: user
tags:
- source:verified-census-query
---
