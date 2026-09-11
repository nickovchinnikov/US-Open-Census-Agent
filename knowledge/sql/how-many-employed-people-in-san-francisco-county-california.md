---
nl: How many employed people in San Francisco County, California commute to work by
  public transportation?
sql: SELECT SUM(c.B08301e10) AS estimated_workers_commuting_by_public_transportation
  FROM census_2019_commuting AS c JOIN census_2019_county_fips AS f ON SUBSTRING(c.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(c.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'CA' AND f.COUNTY = 'San Francisco County'
source: user
---
