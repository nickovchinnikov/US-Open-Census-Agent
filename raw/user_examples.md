# Real question-to-measure examples

These examples use real 2019 IDs, semantic definitions, and the verified CBG to
county geography rule from the collected project material. They describe the
intended analytical interpretation; numeric results must be calculated from the
connected data rather than invented in the response.

## 1. Demographic count by county

**User question:** “How many males aged 22 to 24 lived in Wabash County, Indiana
in 2019?”

**Correct interpretation**

- Year: 2019.
- Geography: all CBGs whose CBG prefix has state FIPS `18` and county FIPS
  `169`, resolved through `2019_METADATA_CBG_FIPS_CODES` as IN, Wabash County.
- Measure: `B01001e10` in `2019_CBG_B01`.
- Definition: estimated males aged 22–24; universe is total population.
- Calculation: `SUM(B01001e10)` across the selected CBGs.

**Why this is grounded:** observed CBG `181691022001` has exactly that FIPS
prefix and resolves to Wabash County, IN. Do not include `B01001e34`: it is the
equivalent female measure, not a male measure. If uncertainty is requested, use
the paired `B01001m10` and explain how MOE is handled.

## 2. County unemployment rate

**User question:** “Which Indiana counties had the highest unemployment rate in
2019?”

**Correct interpretation**

- Group all 2019 CBGs in Indiana by the county FIPS extracted from their CBG.
- Numerator: `B23025e5`, unemployed people in the civilian labour force.
- Denominator: `B23025e3`, civilian labour force.
- Calculation per county:
  `100 * SUM(B23025e5) / NULLIF(SUM(B23025e3), 0)`.
- Sort descending by the calculated rate, not by the number of unemployed people.

**Do not:** divide by total population (`B01001e1`), average CBG unemployment
rates, or call the result a rate for every resident. The universe is population
aged 16+ in the civilian labour force.

## 3. Poverty: people, not families

**User question:** “What share of people in Marion County were below the poverty
level in 2019?”

**Correct interpretation**

- Select `B17021e2`: people with income below poverty level.
- Denominator is `B17021e1`: population for whom poverty status is determined.
- Calculation:
  `100 * SUM(B17021e2) / NULLIF(SUM(B17021e1), 0)` over Marion County CBGs.
- Report the denominator wording in the answer; it is not necessarily the total
  population.

**Important distinction:** `B17010` describes **families** and `B17017`
describes **households**. They are valid only if the question names that unit.
`B17011e1` is an aggregate dollar income deficit, so it cannot answer “how many
people are below poverty?”

## 4. Owner-occupancy rate across counties

**User question:** “Compare owner-occupancy rates for the counties in Indiana.”

**Correct interpretation**

- Owner-occupied units: `B25003e2`.
- All occupied units: `B25003e1`.
- Calculation per county:
  `100 * SUM(B25003e2) / NULLIF(SUM(B25003e1), 0)`.
- The denominator is occupied housing units, not all housing units.

It is also possible to report vacancy rate, but it is a different question:
`100 * SUM(B25002e3) / NULLIF(SUM(B25002e1), 0)`.

## 5. Commuting mode share

**User question:** “What percentage of workers in Cook County used public
transportation to get to work in 2019?”

**Correct interpretation**

- Numerator: `B08301e10`, public transportation excluding taxicab.
- Denominator: `B08301e1`, all workers aged 16+ in the transportation-to-work
  table.
- Calculation:
  `100 * SUM(B08301e10) / NULLIF(SUM(B08301e1), 0)`.

The answer should say “public transportation excluding taxicab” because that is
the actual Census category. “Worked from home” would instead use `B08301e21`.

## 6. Educational attainment: “bachelor’s or higher”

**User question:** “Which counties have the largest share of residents age 25+
with a bachelor’s degree or higher?”

**Correct interpretation**

- Numerator per CBG:
  `B15003e22 + B15003e23 + B15003e24 + B15003e25`.
- Denominator: the total population age 25+ in the `B15003` table (resolve the
  total estimate from the catalog before compiling the query).
- Aggregate numerator and denominator by county first, then divide.

**Do not:** use only `B15003e22`, which is bachelor’s degree only, or add a
rate computed within each CBG.

## 7. Median household income: a required clarification

**User question:** “What is the average household income in Indiana?”

**Correct response before querying:** clarify whether the user means average
(mean) income or median household income. The verified available measure is
`B19013e1`, **median household income in the past 12 months**, in 2019
inflation-adjusted dollars.

If the user confirms that they want the CBG-level median, display it at CBG
grain or use an independently verified higher-geography median. Never produce an
Indiana “median household income” by summing or simple-averaging `B19013e1`
across CBGs. `B19013m1` is the MOE, not an alternative income figure.

## Expected answer provenance

For every result, state: the 2019 release, chosen variable(s) and plain-English
definition, universe, selected geography, aggregation/formula, and whether MOE
was included. This lets a user verify why a seemingly similar Census field was
not selected.
