/*
=============================================================
Create Database and Schemas
=============================================================
Script Purpose:
    This script creates a new database named 'krishna_dwh_db' after checking if it already exists. 
    If the database exists, it is dropped and recreated. Additionally, the script sets up three schemas 
    within the database: 'bronze', 'silver', and 'gold'.
    
WARNING:
    Running this script will drop the entire 'krishna_dwh_db' database if it exists. 
    All data in the database will be permanently deleted. Proceed with caution 
    and ensure you have proper backups before running this script.
*/

-- Connect to postgres database to run administrative commands
\connect postgres;

-- Drop the database if it exists
-- First, disconnect all users
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'krishna_dwh_db') THEN
        -- Force disconnect all users
        EXECUTE 'SELECT pg_terminate_backend(pg_stat_activity.pid) 
                 FROM pg_stat_activity 
                 WHERE pg_stat_activity.datname = ''krishna_dwh_db'' 
                 AND pid <> pg_backend_pid()';
        
        -- Drop the database
        EXECUTE 'DROP DATABASE krishna_dwh_db';
    END IF;
END
$$;

-- Create the new database
CREATE DATABASE krishna_dwh_db;

-- Connect to the newly created database
\connect krishna_dwh_db;

-- Create Schemas
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;

-- Grant usage permissions (optional based on your needs)
GRANT USAGE ON SCHEMA bronze TO public;
GRANT USAGE ON SCHEMA silver TO public;
GRANT USAGE ON SCHEMA gold TO public;

-- Confirm schemas were created
SELECT schema_name FROM information_schema.schemata 
WHERE schema_name IN ('bronze', 'silver', 'gold');