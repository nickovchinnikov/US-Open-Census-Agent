# Census eval

Model: `gpt-5.4-mini`  
Cases: 3/5 passed  
Execution: 100%  
Result accuracy: 60%  
Average latency: 11.75s

## Failures

- `unavailable-king-county-median-income-2024`: agent ran SQL for an unavailable request
- `unavailable-seattle-city-women-age-25-to-34`: agent ran SQL for an unavailable request
