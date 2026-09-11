---
nl: Compare public-transit commuting rates between San Francisco County, California
  and Los Angeles County, California.
sql: SELECT f.COUNTY, SUM(c.B08301e1) AS total_workers_age_16_plus, SUM(c.B08301e10)
  AS workers_commuting_by_public_transportation, 100.0 * SUM(c.B08301e10) / NULLIF(SUM(c.B08301e1),
  0) AS public_transit_commute_pct FROM census_2019_commuting AS c JOIN census_2019_county_fips
  AS f ON SUBSTRING(c.CENSUS_BLOCK_GROUP, 1, 2) = f.STATE_FIPS AND SUBSTRING(c.CENSUS_BLOCK_GROUP,
  3, 3) = f.COUNTY_FIPS WHERE f.STATE = 'CA' AND f.COUNTY IN ('San Francisco County',
  'Los Angeles County') GROUP BY f.COUNTY ORDER BY f.COUNTY
source: user
---
