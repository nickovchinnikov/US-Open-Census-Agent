# Business rules

## County geography must be resolved, never guessed

For every question naming a county and state, first execute a lookup against
`census_2019_county_fips` using the canonical county name and the two-letter
state abbreviation. Use the returned `STATE_FIPS` and `COUNTY_FIPS` values in
the fact query. Do not hand-code, infer, or rely on remembered FIPS values,
even when they seem familiar. A county answer without a successful FIPS lookup
is not sufficiently grounded.

## Bachelor's degree or higher, age 25+

In `census_2019_education` using the `B15003` table, this metric is all four
degree levels: `B15003e22 + B15003e23 + B15003e24 + B15003e25` (bachelor's,
master's, professional, and doctorate). For a county percentage, calculate:

`100.0 * (SUM(B15003e22) + SUM(B15003e23) + SUM(B15003e24) + SUM(B15003e25)) / NULLIF(SUM(B15003e1), 0)`.

`B15003e22` alone means bachelor's degree only; it is not "bachelor's degree
or higher."
