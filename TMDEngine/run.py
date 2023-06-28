# final run script for using the recognition application
import TMDEngine.fingerprint as fingerprint
import TMDEngine.recognize as recognize
import TMDEngine.config as conf
import TMDEngine.sql_database as db

user_sample = conf.test_rec  # path to user's recording


def engine() -> str:

    fprinter_for_sample = fingerprint.Fingerprint(user_sample)
    fprints_of_sample = fprinter_for_sample.generate_fingerprint(
        verbose=True)  # the fingerprints for sample

    # lookup the fingerprints using hash matching
    matching_fingerprints_in_db = recognize.look_for_matches(
        fprints_of_sample)  # trying at first on a2 fingerprints

    # testing code
    # not_matched_at_all = 0
    # for i in matching_fingerprints_in_db.keys():
    #     if not matching_fingerprints_in_db[i]:
    #         not_matched_at_all += 1

    # aligning matches according to time offsets
    all_aligned_pairs = []
    for each_sample_fprint in matching_fingerprints_in_db.keys():
        sample_fprint = each_sample_fprint
        corres_matches = matching_fingerprints_in_db[each_sample_fprint]
        if not corres_matches:  # in case of empty arrays, i.e. no match for rec hash found in Database
            continue
        aligned_pairs = recognize.align_matches(
            fingerprint_of_sample=sample_fprint, list_of_matched_fingerprints=corres_matches
        )

        all_aligned_pairs += aligned_pairs

    song_id, dict_songs = recognize.find_final_song_id(all_aligned_pairs)
    print("#####################################\n\ndict of songs returned", dict_songs)

    obj_to_save_song_name = db.SQLConnection()

    # returns the name of the song as in the database
    return (obj_to_save_song_name.find_song(song_id))[0][1]
