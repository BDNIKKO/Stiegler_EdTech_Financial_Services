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
    password VARCHAR(100) NOT NULL
);

-- Loan table definition
CREATE TABLE IF NOT EXISTS loan (
    id SERIAL PRIMARY KEY,
    income FLOAT NOT NULL,
    loan_amount FLOAT NOT NULL,
    loan_term INTEGER NOT NULL,
    employment_length FLOAT NOT NULL,
    decision VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert a pre-authenticated admin user (hashed password: 'admin123')
INSERT INTO "user" (username, password)
VALUES ('admin', '$2b$12$KwB6TdxuyxLJpkD8K3OEOukdhPN1k5vGcZTGFeIu1K9KOKLVtvKaG')
ON CONFLICT (username) DO NOTHING;
