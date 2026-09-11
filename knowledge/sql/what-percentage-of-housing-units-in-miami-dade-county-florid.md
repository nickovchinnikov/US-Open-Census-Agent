---
nl: What percentage of housing units in Miami-Dade County, Florida are vacant?
sql: SELECT SUM(h.B25002e1) AS total_housing_units, SUM(h.B25002e3) AS vacant_housing_units,
  100.0 * SUM(h.B25002e3) / NULLIF(SUM(h.B25002e1), 0) AS vacant_housing_units_pct
  FROM census_2019_housing AS h JOIN census_2019_county_fips AS f ON SUBSTRING(h.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(h.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'FL' AND f.COUNTY = 'Miami-Dade County'
source: user
---
