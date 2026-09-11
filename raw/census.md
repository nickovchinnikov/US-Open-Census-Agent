# US Open Census — context for the data agent

## What this project contains

This project models the Snowflake database
`US_OPEN_CENSUS_DATA_NEIGHBORHOOD_INSIGHTS_FREE_DATASET`. It contains US Census
measures arranged in subject tables and is intended for neighbourhood analysis.
The physical observation grain is one **Census Block Group (CBG)** per row, not
one row per state, county, or Census tract.

Two parallel releases were found: **2019** and **2020**. Keep releases separate
unless the user explicitly asks for a year-over-year comparison. The supplied
variable catalog, `notebooks/catalog_2019.json`, is the verified dictionary for
the 2019 release: it has 8,120 variable records — 4,060 estimates and 4,060
margins of error. Do not assume that an identically named 2020 column is
available until its metadata and physical schema have been checked.

The main subject tables follow this pattern:

```text
2019_CBG_B01   # age and sex measures
2019_CBG_B19   # household-income measures
2019_CBG_B25   # housing measures
```

Every such table has `CENSUS_BLOCK_GROUP` plus Census variables such as
`B01001e10`. The compact variable name has no safe business meaning on its own:
use the catalog's `semantic_path`, `title`, and `universe` to resolve it.

## Geography

CBG is the base grain. State and county results are created by filtering or
grouping CBG rows; they are not separate fact grains in this source.

The geography lookup is verified for 2019:

```text
CENSUS_BLOCK_GROUP = 12-digit identifier
first 2 digits     -> state FIPS
next 3 digits      -> county FIPS
(state FIPS, county FIPS) -> 2019_METADATA_CBG_FIPS_CODES -> state and county name
```

For example, observed CBG `181691022001` resolves to FIPS `18` / `169`, or
**IN, Wabash County**. Use the FIPS lookup for a human-readable filter or label;
do not match places by a substring of the CBG identifier. Latitude, longitude,
land area, and water area are available in `2019_METADATA_CBG_GEOGRAPHIC_DATA`.

Never compare, join, or average records that represent different geographic
grains without an explicit aggregation plan. A county total is the sum of its
CBGs; a CBG value must not be repeated after a many-to-one geography join.

## How to interpret Census variables

Each catalog record identifies:

| Field | Meaning |
| --- | --- |
| `table_id` | Census variable, for example `B01001e10` |
| `physical_table` / `physical_column` | verified 2019 source location |
| `measure_type` | `estimate` or `marginoferror` |
| `title`, `topics`, `universe` | definition and eligible population/unit |
| `semantic_path` | hierarchy that distinguishes a total from a subgroup |

An `e` variable is an **estimate** and should be the normal default. The paired
`m` variable is a **margin of error (MOE)**, not another count and not a value to
sum into the estimate. Include or explain MOE only when the user asks about
uncertainty or it is needed to qualify a result.

Example of a fully resolved field:

```text
B01001e10
2019_CBG_B01.B01001e10
Estimate > Sex by Age > Total population > Total > Male > 22 to 24 years
```

It is the estimated **number of males aged 22–24 in one CBG**. `B01001m10` is
the margin of error for that same estimate. A raw lexical match for `male` is
unsafe because it can also match `female`; use the full semantic path and
whole-token matching.

## Metric and aggregation rules

- **Counts:** aggregate compatible CBG estimates with `SUM`. State the
  population/universe and the geography in the answer.
- **Percentages/rates:** calculate `SUM(numerator) / SUM(denominator)`, then
  multiply by 100. Do not average CBG percentages, because that gives every CBG
  equal weight.
- **Medians:** never sum or simple-average CBG medians. `B19013e1` is a median
  household income *for one CBG*, and `B25064e1` is a median rent *for one CBG*.
  A county/state median cannot be derived exactly from those CBG medians alone.
- **Income:** “average income” is not “median household income.” Ask for the
  intended statistic or report that only the named median measure is being used.
  Dollar values in the named 2019 income and housing measures are in **2019
  inflation-adjusted US dollars**.
- **Universe matters:** people, households, families, housing units, workers,
  and the civilian labour force are different denominators. Do not silently
  substitute one for another.
- **Year matters:** label each result as 2019 or 2020. Do not combine releases
  in a single aggregation.

## Agent behaviour

1. Identify the requested year, geography, statistic, population, and whether
   the user asks for a count, share, median, or uncertainty.
2. Retrieve candidate variables from the catalog using title, universe, and all
   levels of `semantic_path`; prefer `measure_type = estimate` by default.
3. Resolve state/county labels through the verified FIPS rule before filtering or
   displaying them.
4. Aggregate only measures for which the operation is valid. If a request is
   ambiguous (for example, “poverty” could mean people, families, or households),
   ask a focused clarification instead of selecting a nearby variable.
5. Answer with the selected measure's human definition, universe, year,
   geography, and calculation, so the result is traceable.

See `raw/variables.md` for a curated set of verified variables and
`raw/user_examples.md` for intended natural-language questions and calculations.
