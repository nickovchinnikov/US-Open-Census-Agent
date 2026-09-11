---
nl: Which census block groups in San Francisco County, California have a median household
  income above ,000 and more than 30% of adults age 25 or older with a bachelor's
  degree or higher?
sql: SELECT i.CENSUS_BLOCK_GROUP, i.B19013e1 AS median_household_income_2019_usd,
  100.0 * (e.B15003e22 + e.B15003e23 + e.B15003e24 + e.B15003e25) / NULLIF(e.B15003e1,
  0) AS bachelors_or_higher_pct_age_25_plus FROM census_2019_income AS i JOIN census_2019_education
  AS e ON i.CENSUS_BLOCK_GROUP = e.CENSUS_BLOCK_GROUP JOIN census_2019_county_fips
  AS f ON SUBSTRING(i.CENSUS_BLOCK_GROUP, 1, 2) = f.STATE_FIPS AND SUBSTRING(i.CENSUS_BLOCK_GROUP,
  3, 3) = f.COUNTY_FIPS WHERE f.STATE = 'CA' AND f.COUNTY = 'San Francisco County'
  AND i.B19013e1 > 100000 AND e.B15003e1 > 0 AND 100.0 * (e.B15003e22 + e.B15003e23
  + e.B15003e24 + e.B15003e25) / NULLIF(e.B15003e1, 0) > 30 ORDER BY i.CENSUS_BLOCK_GROUP
source: user
---
