CREATE TABLE IF NOT EXISTS dim_token (
    id INT PRIMARY KEY,
    token VARCHAR(255) UNIQUE,
    token_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dim_token_info (
    token_id INT NOT NULL,
    description TEXT,
    website VARCHAR(255),
    technical_doc VARCHAR(255),
    twitter VARCHAR(255),
    reddit VARCHAR(255),
    logo VARCHAR(255),
    CONSTRAINT fk_dim_token_info_token_id FOREIGN KEY (token_id) REFERENCES dim_token(id)
);

CREATE TABLE IF NOT EXISTS fact_token_prices (
    token_id INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    open DECIMAL(18, 8),
    high DECIMAL(18, 8),
    low DECIMAL(18, 8),
    close DECIMAL(18, 8),
    volume DECIMAL(18, 2),
    price_difference DECIMAL(18, 8),
    price_percentage_change DECIMAL(18, 8),
    mid_price DECIMAL(18, 8),
    vwap DECIMAL(18, 8),
    CONSTRAINT pk_fact_token_prices PRIMARY KEY (token_id, timestamp),
    CONSTRAINT fk_fact_token_prices_token_id FOREIGN KEY (token_id) REFERENCES dim_token(id)
);
