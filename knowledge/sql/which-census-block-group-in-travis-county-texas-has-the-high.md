---
nl: Which census block group in Travis County, Texas has the highest percentage of
  renter-occupied housing units?
sql: WITH travis_county AS (SELECT h.CENSUS_BLOCK_GROUP, h.B25003e1 AS occupied_housing_units,
  h.B25003e3 AS renter_occupied_housing_units, 100.0 * h.B25003e3 / NULLIF(h.B25003e1,
  0) AS renter_occupied_pct FROM census_2019_housing AS h JOIN census_2019_county_fips
  AS f ON SUBSTRING(h.CENSUS_BLOCK_GROUP, 1, 2) = f.STATE_FIPS AND SUBSTRING(h.CENSUS_BLOCK_GROUP,
  3, 3) = f.COUNTY_FIPS WHERE f.STATE = 'TX' AND f.COUNTY = 'Travis County' AND h.B25003e1
  > 0), highest AS (SELECT MAX(renter_occupied_pct) AS highest_renter_occupied_pct
  FROM travis_county) SELECT t.CENSUS_BLOCK_GROUP, t.occupied_housing_units, t.renter_occupied_housing_units,
  t.renter_occupied_pct FROM travis_county AS t CROSS JOIN highest AS x WHERE t.renter_occupied_pct
  = x.highest_renter_occupied_pct ORDER BY t.CENSUS_BLOCK_GROUP
source: user
---
