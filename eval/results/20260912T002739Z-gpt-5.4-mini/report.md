# Census eval

Model: `gpt-5.4-mini`  
Cases: 28/30 passed  
Execution: 100%  
Result accuracy: 93%  
Average latency: 14.70s

## Failures

- `how-many-occupied-housing-units-are-there-in-suffolk-county`: DataFrame.iloc[:, 0] (column name="occupied_housing_units") are different

DataFrame.iloc[:, 0] (column name="occupied_housing_units") values are different (100.0 %)
[index]: [0]
[left]:  [309844]
[right]: [3713]
At positional index 0, first diff: 309844 != 3713
- `what-percentage-of-adults-age-25-or-older-in-suffolk-county`: DataFrame.iloc[:, 0] (column name="bachelors_or_higher_pct_age_25_plus") are different

DataFrame.iloc[:, 0] (column name="bachelors_or_higher_pct_age_25_plus") values are different (100.0 %)
[index]: [0]
[left]:  [46.062865]
[right]: [25.341823]
At positional index 0, first diff: 46.062865 != 25.341823
