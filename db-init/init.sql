DO $$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'admin'
   ) THEN
      CREATE DATABASE admin;
   END IF;
END $$;

\connect admin;

-- User table definition
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT
);

-- Loan table definition
CREATE TABLE IF NOT EXISTS loan (
    id SERIAL PRIMARY KEY,
    income FLOAT NOT NULL,
    loan_amount FLOAT NOT NULL,
    loan_term INTEGER NOT NULL,
    employment_length FLOAT NOT NULL,
    decision VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS loan_analytics (
    id SERIAL PRIMARY KEY,
    total_applications INT,
    approved_count INT,
    denied_count INT,
    approval_rate FLOAT,
    avg_loan_amount FLOAT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Insert a pre-authenticated admin user (hashed password: 'admin123')
INSERT INTO "user" (username, password)
VALUES ('admin', '$2b$12$KwB6TdxuyxLJpkD8K3OEOukdhPN1k5vGcZTGFeIu1K9KOKLVtvKaG')
ON CONFLICT (username) DO NOTHING;
