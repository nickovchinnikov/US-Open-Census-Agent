---
nl: Which census block group in Miami-Dade County, Florida has the highest unemployment
  rate?
sql: WITH miami_dade AS (SELECT e.CENSUS_BLOCK_GROUP, e.B23025e3 AS civilian_labor_force,
  e.B23025e5 AS unemployed_people, 100.0 * e.B23025e5 / NULLIF(e.B23025e3, 0) AS unemployment_rate_pct
  FROM census_2019_employment AS e JOIN census_2019_county_fips AS f ON SUBSTRING(e.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(e.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'FL' AND f.COUNTY = 'Miami-Dade County' AND e.B23025e3 > 0), highest AS
  (SELECT MAX(unemployment_rate_pct) AS highest_unemployment_rate_pct FROM miami_dade)
  SELECT m.CENSUS_BLOCK_GROUP, m.civilian_labor_force, m.unemployed_people, m.unemployment_rate_pct
  FROM miami_dade AS m CROSS JOIN highest AS h WHERE m.unemployment_rate_pct = h.highest_unemployment_rate_pct
  ORDER BY m.CENSUS_BLOCK_GROUP
source: user
---
