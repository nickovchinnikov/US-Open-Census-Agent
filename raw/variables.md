# Curated 2019 variable dictionary

This is a high-confidence starting vocabulary for the agent. Every mapping below
was read from `notebooks/catalog_2019.json`; it is not inferred from a variable
name. For other concepts, search the full catalog before choosing a field.

## Population and age

| Business concept | Variable | Physical source | Universe / exact meaning |
| --- | --- | --- | --- |
| Total population | `B01001e1` | `2019_CBG_B01` | Total population |
| Total male population | `B01001e2` | `2019_CBG_B01` | Total population; male |
| Males aged 22–24 | `B01001e10` | `2019_CBG_B01` | Total population; male; 22 to 24 years |
| Females aged 22–24 | `B01001e34` | `2019_CBG_B01` | Total population; female; 22 to 24 years |

`B01001e10` is a count, so it can be summed over an explicitly selected set of
CBGs. Its uncertainty companion is `B01001m10`; do not return it as a count.

## Income and poverty

| Business concept | Variable | Physical source | Universe / exact meaning |
| --- | --- | --- | --- |
| Median household income | `B19013e1` | `2019_CBG_B19` | Households; median household income in the past 12 months, in 2019 inflation-adjusted dollars |
| MOE of median household income | `B19013m1` | `2019_CBG_B19` | MOE for `B19013e1` |
| People below poverty level | `B17021e2` | `2019_CBG_B17` | Population for whom poverty status is determined; income in past 12 months below poverty level |
| Population with poverty status determined | `B17021e1` | `2019_CBG_B17` | Population for whom poverty status is determined; total |
| Aggregate income deficit of families below poverty level | `B17011e1` | `2019_CBG_B17` | Families below poverty level; aggregate income deficit in past 12 months |

Use `B17021e2 / B17021e1` for the share of the population (among people whose
poverty status is determined) below poverty level. This is an individual-level
poverty measure. It is not interchangeable with `B17010` (families) or `B17017`
(households). `B17011e1` measures dollars of deficit for families below poverty,
not a number of people or families.

## Employment, education, and commuting

| Business concept | Variable(s) | Physical source | Universe / exact meaning |
| --- | --- | --- | --- |
| Civilian labour force | `B23025e3` | `2019_CBG_B23` | Population 16+; in labour force; civilian labour force |
| Unemployed civilian labour force | `B23025e5` | `2019_CBG_B23` | Population 16+; civilian labour force; unemployed |
| Bachelor’s degree only | `B15003e22` | `2019_CBG_B15` | Population 25+; bachelor's degree |
| Master’s degree | `B15003e23` | `2019_CBG_B15` | Population 25+; master's degree |
| Professional school degree | `B15003e24` | `2019_CBG_B15` | Population 25+; professional school degree |
| Doctorate degree | `B15003e25` | `2019_CBG_B15` | Population 25+; doctorate degree |
| Workers who drove alone | `B08301e3` | `2019_CBG_B08` | Workers 16+; car, truck, or van; drove alone |
| Public-transit workers | `B08301e10` | `2019_CBG_B08` | Workers 16+; public transportation excluding taxicab |
| Worked-from-home workers | `B08301e21` | `2019_CBG_B08` | Workers 16+; worked from home |
| All workers in commute table | `B08301e1` | `2019_CBG_B08` | Workers 16+; total |

The correct unemployment rate is
`SUM(B23025e5) / SUM(B23025e3)`. “Bachelor’s or higher” is
`B15003e22 + B15003e23 + B15003e24 + B15003e25`; `B15003e22` alone means
bachelor’s degree **only**.

## Housing

| Business concept | Variable | Physical source | Universe / exact meaning |
| --- | --- | --- | --- |
| Housing units | `B25001e1` | `2019_CBG_B25` | Housing units; total |
| Occupied housing units | `B25002e2` | `2019_CBG_B25` | Housing units; occupied |
| Vacant housing units | `B25002e3` | `2019_CBG_B25` | Housing units; vacant |
| Occupied units / tenure total | `B25003e1` | `2019_CBG_B25` | Occupied housing units; total |
| Owner-occupied units | `B25003e2` | `2019_CBG_B25` | Occupied housing units; owner occupied |
| Renter-occupied units | `B25003e3` | `2019_CBG_B25` | Occupied housing units; renter occupied |
| Median gross rent | `B25064e1` | `2019_CBG_B25` | Renter-occupied units paying cash rent; median gross rent in dollars |
| Median property value | `B25077e1` | `2019_CBG_B25` | Owner-occupied housing units; median value in dollars |

Vacancy rate is `SUM(B25002e3) / SUM(B25002e1)`. Owner-occupancy rate is
`SUM(B25003e2) / SUM(B25003e1)`. Do not aggregate `B25064e1` or `B25077e1` by
summing or averaging the CBG medians.

## Safe selection notes

- Select the `e` estimate counterpart unless the user explicitly asks for MOE.
- Use a variable only with the stated universe. A rate must retain the universe
  of both numerator and denominator in its explanation.
- The IDs and physical locations above are verified for **2019 only**. Resolve
  2020 variables from 2020 metadata rather than copying these IDs blindly.
