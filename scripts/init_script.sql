/*
=============================================================
Create Database and Schemas
=============================================================
Script Purpose:
    This script creates a new database named 'DataWarehouse' after checking if it already exists. 
    If the database exists, it is dropped and recreated. Additionally, the script sets up three schemas 
    within the database: 'bronze', 'silver', and 'gold'.
	
WARNING:
    Running this script will drop the entire 'DataWarehouse' database if it exists. 
    All data in the database will be permanently deleted. Proceed with caution 
    and ensure you have proper backups before running this script.
*/

-- Connect to the default database
\c postgres;

-- Drop and recreate the 'DataWarehouse' database
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'DataWarehouse') THEN
        PERFORM pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'DataWarehouse';
        EXECUTE 'DROP DATABASE DataWarehouse';
    END IF;
END $$;

-- Create the 'DataWarehouse' database
CREATE DATABASE "DataWarehouse";

-- Connect to the 'DataWarehouse' database
\c DataWarehouse;

-- Create Schemas
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
