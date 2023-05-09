import os

import logic.config as config
import logic.sql_database as db
import logic.fingerprint as fingerprint


# create fingerprints of known songs and add to database

# get files and names of songs
def get_files(address_to_files_folder: str):
    """
    A function that accesses the local folder containing the .wav files and save their path and names
    :param address_to_files_folder: local directory containing wav files
    :return: a dictionary with key values as song_address names and values as path to the files
    """
    songs = {}
    with os.scandir(address_to_files_folder) as folder:
        for file in folder:
            songs[file.name[:-4]] = file.path.replace("\\", "/")
    return songs


def add_song_to_app(name: str, song_address: str):
    """
    A function to update the song_address info and related fingerprints(after their creation) to the Engine Database.
    Any DUPLICATE songs will not be added to database
    :param name: name of the song, this will be stored in the song table of the database
    :param song_address: the local path to the .wav file fo the song_address
    :return:
    """
    database_cnxn = db.SQLConnection()
    song_id = database_cnxn.insert_song(name)
    num_duplicates = 0
    if song_id != -1:  # not a DUPLICATE

        f = fingerprint.Fingerprint(song_address, song_id)
        fingerprints = f.get_fingerprint(plot=False, verbose=True)
        num_fingerprints = len(fingerprints)

        for fprint in fingerprints:
            num_duplicates += database_cnxn.insert_fingerprint(fprint)

        dup_perc = (num_fingerprints - num_duplicates) / num_fingerprints
        database_cnxn.change_fingerprinted_flag(song_id, True)
        print("Unique Fingerprints for {0}, id {1} inserted: {2}.\n Originally {3}% duplicates \n\n".
              format(name, song_id, num_fingerprints, dup_perc))
    else:
        print("Song already present in database")
    database_cnxn.close_cnx()


def build_app(first_build: bool = False, schema_to_use: str = None):
    if first_build:
        # building the database for the first time.
        first_conn = db.SQLConnection(build_schema=schema_to_use)
        first_conn.close_cnx()
    else:  # a build call after the primary database has already been built 
        if config.are_you_sure:
            pass # the already present database will be deleted.
        else:
            raise ValueError("This action will delete the existing database. Please make necessary checks before re-running.")
        
        db_conn = db.SQLConnection()
        db_conn.delete_database(schema_to_use)
        db_conn.create_database(schema_to_use)
        db_conn.close_cnx()
        

    new_conn = db.SQLConnection()
    new_conn.create_tables()

    song_info_dict = get_files(config.files_folder)

    for key in list(song_info_dict.keys())[:1]:
        print(key, song_info_dict[key])

        add_song_to_app(key, song_info_dict[key])
        
    new_conn.close_cnx()          
