---
nl: What percentage of workers in New York County, New York commute by car, truck,
  or van?
sql: SELECT SUM(c.B08301e1) AS total_workers_age_16_plus, SUM(c.B08301e2) AS workers_commuting_by_car_truck_or_van,
  100.0 * SUM(c.B08301e2) / NULLIF(SUM(c.B08301e1), 0) AS car_truck_or_van_commute_pct
  FROM census_2019_commuting AS c JOIN census_2019_county_fips AS f ON SUBSTRING(c.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(c.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'NY' AND f.COUNTY = 'New York County'
source: user
---
