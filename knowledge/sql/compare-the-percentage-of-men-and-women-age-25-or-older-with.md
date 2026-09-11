---
nl: Compare the percentage of men and women age 25 or older with a bachelor's degree
  or higher in King County, Washington.
sql: SELECT SUM(e.B15002e2) AS men_age_25_plus, SUM(e.B15002e15) + SUM(e.B15002e16)
  + SUM(e.B15002e17) + SUM(e.B15002e18) AS men_bachelors_or_higher, 100.0 * (SUM(e.B15002e15)
  + SUM(e.B15002e16) + SUM(e.B15002e17) + SUM(e.B15002e18)) / NULLIF(SUM(e.B15002e2),
  0) AS men_bachelors_or_higher_pct, SUM(e.B15002e19) AS women_age_25_plus, SUM(e.B15002e32)
  + SUM(e.B15002e33) + SUM(e.B15002e34) + SUM(e.B15002e35) AS women_bachelors_or_higher,
  100.0 * (SUM(e.B15002e32) + SUM(e.B15002e33) + SUM(e.B15002e34) + SUM(e.B15002e35))
  / NULLIF(SUM(e.B15002e19), 0) AS women_bachelors_or_higher_pct FROM census_2019_education
  AS e JOIN census_2019_county_fips AS f ON SUBSTRING(e.CENSUS_BLOCK_GROUP, 1, 2)
  = f.STATE_FIPS AND SUBSTRING(e.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE f.STATE
  = 'WA' AND f.COUNTY = 'King County'
source: user
---
