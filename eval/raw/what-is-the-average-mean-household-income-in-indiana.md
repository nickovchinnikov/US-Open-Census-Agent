---
nl: What is the average (mean) household income in Indiana?
sql: SELECT SUM(i.B19025e1) / NULLIF(SUM(i.B19001e1), 0) AS mean_household_income_2019_usd
  FROM census_2019_income AS i WHERE SUBSTRING(i.CENSUS_BLOCK_GROUP, 1, 2) = '18'
source: user
tags:
- source:verified-census-query
---
