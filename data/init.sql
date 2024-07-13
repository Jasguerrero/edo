CREATE TABLE IF NOT EXISTS edos (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    mobileNumber VARCHAR(50),
    email VARCHAR(50),
    contact TEXT,
    physicalAddress TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zipCode VARCHAR(50),
    website TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);
