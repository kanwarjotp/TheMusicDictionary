import TMDEngine.sql_database as db


def look_for_matches(fingerprints_of_sample=None):
    """
    A function that looks for matches of hash values of the sample's fingerprint in the database for each fingerprint
    in the list fingerprints_os_sample. A dictionary is constructed and returned. SEE README.MD Development Notes:
    Pt.3.
    :param fingerprints_of_sample: a list (length N) of sample's fingerprints
    :return: a dictionary,with keys equal to the fingerprints of the sample and values as list of matching fingerprints in database
    """
    if fingerprints_of_sample is None:
        fingerprints_of_sample = []
    if not fingerprints_of_sample:
        # recording not viable
        raise ValueError("No Fingerprints Supplied for Sample")
    else:
        matching_fingerprints = {}
        db_cnxn = db.SQLConnection()
        for fingerprints in fingerprints_of_sample:
            # a list of fingerprints with hashes matching the sample's hash
            fingerprint_in_db = db_cnxn.find_fingerprint(fingerprints[0])
            # adding fingerprints found
            matching_fingerprints[fingerprints] = fingerprint_in_db

        return matching_fingerprints


def align_matches(fingerprint_of_sample: tuple, list_of_matched_fingerprints: list):
    # all the hashes with same distance apart are the ones that are real matches
    # therefore the offset difference with the highest number of hashes

    aligned_matches = []
    for each_match_fprint in list_of_matched_fingerprints:
        # time offset from matched_fprint - time_offset from each_s_fprint
        difference = each_match_fprint[2] - fingerprint_of_sample[1][1]
        song_id_of_match = each_match_fprint[1]

        aligned_matches.append((song_id_of_match, difference))

    return aligned_matches


def find_final_song_id(pairs):
    counts_tds = dict()

    for i in pairs:
        tds = i[1]  # the time differences
        counts_tds[tds] = counts_tds.get(tds, 0) + 1

    max_tds_count = max(counts_tds, key=counts_tds.get)

    songs_max_tds = {}
    for i in pairs:
        if i[1] == max_tds_count:
            sid = i[0]
            songs_max_tds[sid] = songs_max_tds.get(sid, 0) + 1

    return max(songs_max_tds, key=songs_max_tds.get), songs_max_tds
