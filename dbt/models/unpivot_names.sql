{{ config(
    materialized = 'table',
    alias = 'names_data'
) }}

{% set source_table = source('main', 'data_raw_names') %}

{% set all_columns = adapter.get_columns_in_relation(source_table) %}

{% set tokens = [] %}
{% for col in all_columns %}
    {% if col.column | lower not in ['date', 'load_ts'] %}
        {% do tokens.append(col.column) %}
    {% endif %}
{% endfor %}

WITH source AS (
    SELECT * FROM {{ source_table }}
)

SELECT
    date,
    token AS instrument,
    value,
    load_ts AS ts
FROM (
    {% for token in tokens %}
    SELECT
        date,
        '{{ token }}' AS token,
        "{{ token }}" AS value,
        load_ts
    FROM source
    {% if not loop.last %}
    UNION ALL
    {% endif %}
    {% endfor %}
);
