---
nl: Among census block groups in King County, Washington, which five have the highest
  percentage of residents aged 25 to 34?
sql: SELECT a.CENSUS_BLOCK_GROUP, a.B01001e1 AS total_population, a.B01001e11 + a.B01001e12
  + a.B01001e35 + a.B01001e36 AS residents_age_25_to_34, 100.0 * (a.B01001e11 + a.B01001e12
  + a.B01001e35 + a.B01001e36) / NULLIF(a.B01001e1, 0) AS residents_age_25_to_34_pct
  FROM census_2019_age_sex AS a JOIN census_2019_county_fips AS f ON SUBSTRING(a.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(a.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'WA' AND f.COUNTY = 'King County' AND a.B01001e1 > 0 ORDER BY residents_age_25_to_34_pct
  DESC, a.CENSUS_BLOCK_GROUP LIMIT 5
source: user
---
