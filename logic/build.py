import os
import config
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


def build_app():
    # deleting pre-existing database
    if config.are_you_sure:
        pass
    else:
        raise ValueError("This action will delete the existing database. Please make necessary check before re "
                         "running.")
    db_conn = db.SQLConnection()
    db_conn.delete_database(config.test_schema)
    db_conn.create_database(config.test_schema)

    new_con = db.SQLConnection()
    new_con.create_tables()

    song_info_dict = get_files(config.files_folder)

    for key in list(song_info_dict.keys())[:2]:
        print(key, song_info_dict[key])

        add_song_to_app(key, song_info_dict[key])


