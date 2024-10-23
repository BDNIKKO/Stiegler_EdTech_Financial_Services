DO $$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'admin'
   ) THEN
      CREATE DATABASE admin;
   END IF;
END $$;
