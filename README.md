# Project Title
Data Analysis of a songs streaming organization, Sparkify

# Project Description
This project involves reading in and analyzing songs and logs data collected for the Sparkify organization. Sparkify wants to determine how users are using their streaming service. This involves analyzing which sings are streamed the most, which artists are extremely popular, what time of the day do users listen to the songs, which songs are looped etc.   

# Prerequisites
Python installed (Jupyter notebook, IPython, IDLE)
Python packages (pandas, numpy, psycopg2, pscycop2.extensions)
PostgreSQL database

# Database schema
The tables created form a STAR schema with the songplays as the fact and the user, songs, artists and time as the dimension tables.

    Fact Table:
    ==========
    1) songplays - records in log data associated with song plays i.e. records with page NextSong
    Columns: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

    Dimension Tables:
    ================
    1) users - users in the app
    Columns: user_id, first_name, last_name, gender, level

    2) songs - songs in music database
    Columns: song_id, title, artist_id, year, duration

    3) artists - artists in music database
    Columns: artist_id, name, location, latitude, longitude

    4) time - timestamps of records in songplays broken down into specific units
    Columns: start_time, hour, day, week, month, year, weekday

# Steps to build the project 
1) Create a create_tables.py python file that would be used to create a connection to the database and execute queries from the sql_queries.py file to drop and create tables. This script should be created first.

2) Create a sql_queries.py file that will have the DDL and DML statements for dropping, creating and inserting records into the tables. 

3) The data for this project is broadly classified into 2 types: songs data and logs data. All the data is in JSON format and needs to be parsed accordingly. The songs data contains information about the song like title, duration, year released as well as the artist details like name, location etc. The logs data contains information about the users and how they use the streaming service.

4) Information from the songs data is parsed to create the songs and artists table. Likewise, information from the logs data is used to create the users, time and songplays tables. 

5) Create a python notebook file to parse and create tables as per the defined schema and test it at each stage (after inserting record(s) into a new table). Have a separate file (test.ipynb) to do this testing. Once the scripts are ready, create another python notebook file (run_scripts.ipynb) to run the sql_queries and create_tables python files. 

6) Once the testing has been completed, create the final etl.py file that will do all the processing. Restart the kernel to reset the database and run the run_scripts.ipynb file and execute the sql_queries.py, create_tables.py and etl.py in sequence. Monitor the output from the etl.py file and finally check if all records have been inserted into the correct tables.

7) Once the database is ready, the analytics queries can be run.  

# Running the tests
Always use the test.ipynb to run the tests. Restart the kernel if changes have been made to the files. 

