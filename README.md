# US Open Census Agent

This project uses Wren AI to model and query the Snowflake database
`US_OPEN_CENSUS_DATA_NEIGHBORHOOD_INSIGHTS_FREE_DATASET`.

## Connection setup

Copy the values for the Snowflake account, user, password, and schema into `.env`.
This project's connection profile uses password authentication and Snowflake's
default warehouse.
The `.env` file is ignored by Git; `.env _template` is the safe shareable template.

Once the values are in place, create and bind the Wren profile using the included
secret-free `wren-snowflake-connection.yml`:

```bash
uv sync
uv run wren profile add us-open-census --from-file wren-snowflake-connection.yml
uv run wren context init --empty
uv run wren context set-profile us-open-census
```

Then generate Wren MDL models from the selected Snowflake tables before querying.


`models/` contains the generated and validated Wren MDL semantic layer. It is committed intentionally to make the agent's data model reviewable and reproducible.

