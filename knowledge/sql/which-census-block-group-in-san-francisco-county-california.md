---
nl: Which census block group in San Francisco County, California has the highest number
  of residents age 25 or older with a bachelor's degree or higher?
sql: WITH san_francisco_county AS (SELECT e.CENSUS_BLOCK_GROUP, e.B15003e22 + e.B15003e23
  + e.B15003e24 + e.B15003e25 AS estimated_people_age_25_plus_bachelors_or_higher
  FROM census_2019_education AS e JOIN census_2019_county_fips AS f ON SUBSTRING(e.CENSUS_BLOCK_GROUP,
  1, 2) = f.STATE_FIPS AND SUBSTRING(e.CENSUS_BLOCK_GROUP, 3, 3) = f.COUNTY_FIPS WHERE
  f.STATE = 'CA' AND f.COUNTY = 'San Francisco County'), highest AS (SELECT MAX(estimated_people_age_25_plus_bachelors_or_higher)
  AS highest_count FROM san_francisco_county) SELECT s.CENSUS_BLOCK_GROUP, s.estimated_people_age_25_plus_bachelors_or_higher
  FROM san_francisco_county AS s CROSS JOIN highest AS h WHERE s.estimated_people_age_25_plus_bachelors_or_higher
  = h.highest_count ORDER BY s.CENSUS_BLOCK_GROUP
source: user
tags:
- source:verified-census-query
---
