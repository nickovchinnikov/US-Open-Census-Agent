---
nl: Which census block group in King County, Washington has the highest percentage
  of workers who work from home?
sql: WITH king_county AS (SELECT c.CENSUS_BLOCK_GROUP, c.B08301e1 AS total_workers_age_16_plus,
  c.B08301e21 AS workers_working_from_home, 100.0 * c.B08301e21 / NULLIF(c.B08301e1,
  0) AS work_from_home_pct FROM census_2019_commuting AS c JOIN census_2019_county_fips
  AS f ON SUBSTRING(c.CENSUS_BLOCK_GROUP, 1, 2) = f.STATE_FIPS AND SUBSTRING(c.CENSUS_BLOCK_GROUP,
  3, 3) = f.COUNTY_FIPS WHERE f.STATE = 'WA' AND f.COUNTY = 'King County' AND c.B08301e1
  > 0), highest AS (SELECT MAX(work_from_home_pct) AS highest_work_from_home_pct FROM
  king_county) SELECT k.CENSUS_BLOCK_GROUP, k.total_workers_age_16_plus, k.workers_working_from_home,
  k.work_from_home_pct FROM king_county AS k CROSS JOIN highest AS h WHERE k.work_from_home_pct
  = h.highest_work_from_home_pct ORDER BY k.CENSUS_BLOCK_GROUP
source: user
---
