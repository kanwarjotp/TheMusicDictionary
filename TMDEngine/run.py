# final run script for using the recognition application
import TMDEngine.fingerprint as fingerprint
import TMDEngine.recognize as recognize
import TMDEngine.config as conf
import TMDEngine.sql_database as db

user_sample = conf.test_rec  # path to user's recording


def engine() -> str:

    fprinter_for_sample = fingerprint.Fingerprint(user_sample)
    fprints_of_sample = fprinter_for_sample.generate_fingerprint(verbose=True)  # the fingerprints for sample


    testing_ = fprints_of_sample
    # lookup the fingerprints using hash matching
    matching_fingerprints_in_db = recognize.look_for_matches(testing_)  # trying at first on a2 fingerprints

    not_matched_at_all = 0
    for i in matching_fingerprints_in_db.keys():
        if not matching_fingerprints_in_db[i]:
            not_matched_at_all += 1


    all_pairs = []
    for f in matching_fingerprints_in_db.keys():
        if matching_fingerprints_in_db[f]:
            all_pairs += matching_fingerprints_in_db[f]


    song_id, dict_songs = recognize.find_final_song_id(all_pairs)

    obj_to_save_song_name = db.SQLConnection()
    

    return (obj_to_save_song_name.find_song(song_id))[0][1] # returns the name of the song as in the database
