import os
import glob
import psycopg2
import pandas as pd
import numpy as np
import datetime as datetime
from sql_queries import *
from psycopg2.extensions import register_adapter, AsIs

# Function defined so that psycopg2 package can identify numpy float types
def addapt_numpy_float64(numpy_float64):
    """Object converted to floating type that is understood by psycopg2"""
    return AsIs(numpy_float64)

# Function defined so that psycopg2 package can identify numpy integer types
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)

def process_song_file(cur, filepath):
    """
    Processes the songs json file and inserts records in the songs and artists table
    
    Parameters:
    cur: The cursor connection created to work with the database
    filepath: The location of the file to process
    
    Returns: nothing
    """
    # open song file
    df = pd.read_json(filepath, lines=True)                                        
    df['artist_latitude'].fillna(0, inplace=True)                                   # Default unknown latitude values to 0
    df['artist_location'].fillna('null', inplace=True)                              # Set unknown location values to null
    df['artist_longitude'].fillna(0, inplace=True)                                  # Default unknown longitue values to 0

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].iloc[0].values.tolist()         # Select the first record and convert to a list prior to insertion 
    cur.execute(song_table_insert, song_data)                                                         # Insert records into the song table
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].iloc[0].values.tolist()  # Select the first record and convert to a list prior to insertion
    cur.execute(artist_table_insert, artist_data)                                # Insert records into the artist table


def process_log_file(cur, filepath):
    """
    Processes the logs json file, filters records and inserts records in the time, users and songplays table
    
    Parameters:
    cur: The cursor connection created to work with the database
    filepath: The location of the file to process
    
    Returns: nothing
    """
    # open log file
    df = pd.read_json(filepath, lines=True)
    
    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'].astype(int), unit='ms').reset_index(drop=True)
    
    # insert time data records
    time_data = [t.astype('str').tolist(), t.dt.hour.tolist() , t.dt.day.tolist(), t.dt.weekofyear.tolist(), t.dt.month.tolist(), t.dt.year.tolist(), t.dt.weekday_name.tolist()]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame({column_labels[0]:time_data[0],column_labels[1]:time_data[1],column_labels[2]:time_data[2],column_labels[3]:time_data[3],column_labels[4]:time_data[4],column_labels[5]:time_data[5],column_labels[6]:time_data[6]})                     # Create the DataFrame from the dictionary using column_labels as keys and the pandas Series (convered to list) as values

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))         # Insert records into the time table

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]               

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)               # Insert records into the users table

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)              # Insert records into the songplays table


def process_data(cur, conn, filepath, func):
    """Function is used to create paths for all the json files under a directory
    
    Parameters:
    cur: The cursor connection created to work with the database
    conn: The connection used to connect to the Sparkify database
    filepath: The directory to search and process the files from
    func: Identifies which function needs to be called to process the correct file type
    
    Returns: nothing
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()