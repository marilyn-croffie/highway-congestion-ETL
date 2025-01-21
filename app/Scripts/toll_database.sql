-- Create a database
create database tolldata;

-- Use the database
use tolldata;

-- Create a table
create table livetolldata(timestamp datetime,vehicle_id int,vehicle_type char(15),toll_plaza_id smallint);

-- Disconnect from MySQL server
exit
