# Census eval

Model: `gpt-5.4-mini`  
Cases: 35/37 passed  
Execution: 100%  
Result accuracy: 95%  
Average latency: 13.02s

## Failures

- `which-census-block-group-in-los-angeles-county-has-the-large`: DataFrame.iloc[:, 0] (column name="census_block_group") are different

DataFrame.iloc[:, 0] (column name="census_block_group") values are different (100.0 %)
[index]: [0]
[left]:  [060372756021]
[right]: [481576729001]
At positional index 0, first diff: 060372756021 != 481576729001
- `which-census-block-group-in-miami-dade-county-florida-has-th`: DataFrame.iloc[:, 0] (column name="census_block_group") are different

DataFrame.iloc[:, 0] (column name="census_block_group") values are different (100.0 %)
[index]: [0]
[left]:  [120869807001]
[right]: [120860038011]
At positional index 0, first diff: 120869807001 != 120860038011
