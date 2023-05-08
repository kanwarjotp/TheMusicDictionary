test_rec = "F:/The Music Dict/TheMusicDictionary/rec_output.wav"

files_folder = "F:\Audio_Fingerprinting\wav_files"

actual_schema = "tmd_schema"
test_schema = "tmd_test_schema"
test_schema_1 = "s1"  # 25 30 15
test_schema_2 = "s3"

current_schema = test_schema_2

cnxn_conf = {
    'username': "root",
    'password': "sql102000@",
    'host': '127.0.0.2',
    'database': current_schema
}

first_cnxn = {
    'username': "root",
    'password': "sql102000@",
    'host': '127.0.0.2'
}
are_you_sure = False
