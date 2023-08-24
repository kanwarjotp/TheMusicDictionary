# The Music Dictionary

A Music Recognition Website, which works by utilizing Audio Fingerprinting. The website, “The Music Dictionary” presents an interactive environment for the user to submit record songs as queries and explore prediction generated based on Audiofingerprinting.
During this project, I designed and developed a Music Recognition Application that operates as a web-based platform. The application offers real-time predictions by dynamically analyzing user-submitted recordings of music pieces captured through their microphones. The primary challenge of this project was to create a robust classification methodology capable of uniquely identifying specific audio files. This involved a comprehensive exploration of acoustics principles, including frequencies, amplitudes, and other essential properties of music signals.

Project Highlights:

The project's scope extended into the realm of music information retrieval, necessitating an in-depth understanding of how a machine digitally interprets music signals. This involved quantifiable values like note frequencies, durations, loudness, and amplitudes. This approach distilled music classification to the fundamental building blocks of acoustics. The project aimed to extract unique features from a music piece, addressing the question: "What distinguishes this music?"

The Music Recognition Engine followed a multi-step process:

Fingerprint Generation: The engine creates unique fingerprints of the recorded audio files.

Fingerprint Matching: These fingerprints are matched against known song fingerprints stored in a database.

Audio Processing: The process involves various audio processing steps, including specific fingerprint selection and prediction generation.

User Interface: The results are conveyed to the end-user through a website interface.

The project was entirely written in Python 3.10.10 and employed a diverse range of industry-standard packages and cutting-edge modules. The logic for the music dictionary executed the entire process, showcasing the power of Python in implementing complex audio processing workflows.

Music Representation:

The foundation of the project rested on gathering information from music, which can be represented in physical, symbolic, and audio forms. Physical representation involves traditional musical scores with notations. Symbolic representation digitizes musical notes, often using formats like MIDI. More advanced forms like Spectrograms and Waveforms are also used for symbolic representation, allowing retrieval of specific properties. Audio representation refers to file formats like WAV, FLAC, and MP3. WAV files, used in this project due to their uncompressed nature, provided ample data and detailed information about audio files.

In conclusion, the Music Recognition Application project delved into the intricacies of acoustics and music processing, combining Python programming, audio processing techniques, and web development to create a powerful and user-friendly platform for music recognition and classification.

## The Whats, Hows, and Whys?

This is a Dynamic Website that records audio snippets of songs at the user's machine and returns the title of the song. 

The Website, which serves as the front-end is fundamentally a Flask Whisky Server, with certain add-ons and personalisations to make it more, mainstream. These additions are :

1. Password Encryption, using Bcrypt
2. Client Side Validation
3. Server Side Validation
4. Tweaks to Flask Session Time Lines
5. Interactive Forms, ansd so on...

The Music Recognition Engine, which forms the brains of the whole operations is a Python Package, which is imported to the Server. I installed the package to my local machine, however this might not be possible for everyone so, I have kept it as a number of modules in the TMDEngine Folder. It's sailient development features are :

1. wavfile, of SciPy (reading audio into app)
2. matplotlib, for visualising the spectrogram
3. scikit-image, for peak finding
4. hashlib, numpy and others for various features
5. the databases are manipulated using mysql-connectors

To make it easier to start-up from scratch, I have addes some shell scripts, they will take up the bulk of the work and are described in details, below. Beware they look more tedious than they are.

## Installation on a Local Machine

To install and run the project on a local machine you must fullfil the following requirements:

1. Python 3
2. A MySQL Server

Once you are sure that the above requirements are statisfied, it's time to install all the required packages. To do so run the following cmds in bash. This is required only for the first time.

```sh
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
```

You may run the commands or just add them to start.sh and run that file. That's all, once you run the commands above it's time to create the configuration files.

### Configs

To maintain a secure development environment, no config files are committed to the Version Control, this means you would need to set some parameters of your own. However this can be done quite easily in just 2 steps.

#### server.py Config

In the folder where the **_server.py_** script is locate create a new file, **_config.py_**. Once created, copy the following code and set these variables as you like.

```py
import datetime

SECRET_KEY="" # change this to a long, unique, secret string

# it is not necessary to change anything here
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=5)
```

Notes about config.py:

1. SECRET_KEY: A variable to store the secret key configuration for the Flask app. This key is required to create a secure Session in the Flask App.
2. PERMANENT_SESSION_LIFETIME: As the name suggests, it sets the maximum age of a permanent Flask Session.

#### TMDEngine Package Config

Navigate to the folder named **_TMDEngine_** in the directory. Once you are inside the fodler create a new file, **_config.py_**. Copy the following code into that file.

```py
# the directory containing the wavs of the songs to be fingerprinted.
files_folder = "wavs/song_wavs"

# address to the recording generated by the webpage
test_rec = "TheMusicDictionary/rec_output.wav"

# the database in which the app data(songs, fingerprints) is stored.
actual_schema = 'tmd_schema'

current_schema = actual_Schema

cnxn_conf = {
    'username': '',  # set the MySQL username for the connection
    'password': '',  # set the MySQL password
    'host': '',  # set the host address
    'database': current_schema
}

# the connection params for building the database for the first time.
first_cnxn = {
    'username': '',
    'password': '',
    'host': ''
}

# always set this to False unless you want to recreate your database.
are_you_sure = False
```

Notes about config.py:

1. files_folder: Add the wav files of all songs you would like to be figerprinted and stored in the database. Note the name of the files will be the names stored in the database and will be the predictions.
2. test_rec: Set this variable to the path of the _rec_output.wav_ in your filesystem.

The config file in logic module is mainly to facilitate easy development and testing, and thus will be useful if you wish to change the behaviour of the logic module at one place. Neverthless, even if you don't intend to _experiement_, so to say it is still a lot easier to have all relevant config information in one place.

### Building the App

The next step is to build the app on your machine so it can recognise songs. The First Step would be decide which songs you would like to fingerprint. Once that has been decided store the songs in wav format in a directory on your computer and replace the address in the [TMDEngine config file](#TMDEngine-package-config).

```py
files_folder = "" # your songs directory
```

After you have done so. Its time to build the application. To do so simply run the **_build_database.sh_** file. This will fingeprint all the songs in files_folder and upload them to the database specified in the [logic config files](#logic-config).

Pat your back, you have dealt with the hard part!!

### Running the Web Application.

All that's left is for you to run **_start.sh_** file and go to the link where the website is hosted on your local network.

If everything worked correctly, _Congratulations you have a music recognition application installed on your machine_. Please reach out if anything fails or doesn't work.

## Installation on Glitch

Song Recoginition won't work in Glitch **_at present_** because there is no server side database of songs. However, it is still possible to create accounts and record audio. These are completely working.

You have to install python3 pip and requirements to use the encrypt functionalties on glitch, need only be done once.

here is how u do it:

```sh
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
python3 server.py
```

Add these to the start.sh file of the Project

## Current Fingerprinting Paramters:

1. Recording Length = 10s<br><br>
2. Minimum Distance b/w Peaks = 25
3. Minimum Intensity = 30
4. Max Segment to Fingerprint = 15
5. <b>Mean Time to Prediction= 39s</b>

## Thanks

- Will Drevo's [Article](https://willdrevo.com/fingerprinting-and-audio-recognition-with-python/) on Audiofingerprinting that helped me start this project and the [Dejavu Repo](https://github.com/worldveil/dejavu).
- Milos Miljkovic and his [instructive video](https://www.youtube.com/watch?v=xDFARS_oIfM&t) on PyData, without which this project wouldn't have reached completion, the [GitHub Repo](https://github.com/miishke/PyDataNYC2015).
- Meinard Müller's Book, [Fundamentals of Music Processing](https://link.springer.com/book/10.1007/978-3-319-21945-5) for explaining all the underlyinc concepts in an understandable and lucid manner.
- And lastly thanks to every one at Stackoverflow.
