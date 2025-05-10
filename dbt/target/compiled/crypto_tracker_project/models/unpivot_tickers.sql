







    

    
        
    

    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    


WITH source AS (
    SELECT * FROM main."data_raw_tickers"
)

SELECT
    date,
    token AS instrument,
    value,
    load_ts AS ts
FROM (
    
    SELECT
        date,
        'BTC' AS token,
        "BTC" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'ETH' AS token,
        "ETH" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'SOL' AS token,
        "SOL" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'AVAX' AS token,
        "AVAX" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'ARB' AS token,
        "ARB" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'MATIC' AS token,
        "MATIC" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'OP' AS token,
        "OP" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'LINK' AS token,
        "LINK" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'ATOM' AS token,
        "ATOM" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'SUI' AS token,
        "SUI" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'APT' AS token,
        "APT" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'INJ' AS token,
        "INJ" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'RNDR' AS token,
        "RNDR" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'TIA' AS token,
        "TIA" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'TON' AS token,
        "TON" AS value,
        load_ts
    FROM source
    
    
);