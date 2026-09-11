---
nl: How many males aged 22 to 24 lived in Wabash County, Indiana in 2019?
sql: SELECT SUM(age.B01001e10) AS estimated_males_age_22_to_24 FROM census_2019_age_sex
  AS age WHERE SUBSTRING(age.CENSUS_BLOCK_GROUP, 1, 2) = '18' AND SUBSTRING(age.CENSUS_BLOCK_GROUP,
  3, 3) = '169'
source: user
tags:
- source:verified-census-query
---
