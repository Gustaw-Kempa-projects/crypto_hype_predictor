







    

    
        
    

    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    

    
        
    


WITH source AS (
    SELECT * FROM main."data_raw_names"
)

SELECT
    date,
    token AS instrument,
    value,
    load_ts AS ts
FROM (
    
    SELECT
        date,
        'Bitcoin' AS token,
        "Bitcoin" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Ethereum' AS token,
        "Ethereum" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Solana' AS token,
        "Solana" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Avalanche' AS token,
        "Avalanche" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Arbitrum' AS token,
        "Arbitrum" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Polygon' AS token,
        "Polygon" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Optimism' AS token,
        "Optimism" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Chainlink' AS token,
        "Chainlink" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Cosmos' AS token,
        "Cosmos" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Sui' AS token,
        "Sui" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Aptos' AS token,
        "Aptos" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Injective' AS token,
        "Injective" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Render Network' AS token,
        "Render Network" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Celestia' AS token,
        "Celestia" AS value,
        load_ts
    FROM source
    
    UNION ALL
    
    
    SELECT
        date,
        'Toncoin' AS token,
        "Toncoin" AS value,
        load_ts
    FROM source
    
    
);