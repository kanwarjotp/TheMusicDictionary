# The Music Dictionary

A Music Recoginition Web Application, which works by utilizing Audio Fingerprinting. The web application, “The Musical Dictionary” a web-based client that presents an interactive environment for the user to submit song recordings as queries and explore prediction generated based on Audiofingerprinting. Using the Scientific Python Libraries: SciPy, scikit-image and NumPy, an audio file is converted to an array, representing the waveform of the track, which is then converted to a spectrogram, by use of matplotlib. Using scikit-image, Peaks are identified and paired, along with their time offsets. This information is stores in a hash, SHA5, which forms the fingerprint to be stored in an MySQL Server. This Database is then used by the Backend of the Web Client to recognize songs, recorded by the user. The recording is sent to the backend using AJAX. Flask and Bootstrap 5, JavaScript are used at backend and frontend respectively. *In a continous state of Development*

The Project is still in development and may not work correctly or work unexpectedly, please feel free to raise an Issue or a PR to point out a problem or suggest a fix. All contribution are welcome.


## Installation on a Local Machine
To install and run the project on a local machine you must fullfil the following requirements:

1. Python 3
2. A MySQL Server

Once you are sure that the above requirements are statisfied, it's time to install all the required packages. This is required only for the first time.

```sh
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
```

You may run the commands or just add them to start.sh and run that file. That's all, once you run the commands above it's time to create the configuration files.

### Configs
To maintain a secure development environment, no config files are committed to the Version Control, this means you would need to set some parameters of your own. However this can be done quite easily in just 2 steps.

#### server.py Config
In the folder where the ***server.py*** script is locate create a new file, ***config.py***. Once created, copy the following code and set these variables as you like.

```py
import datetime

SECRET_KEY="" # change this to a long, unique, secret string 

# it is not necessary to change anything here
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=5)
```

Notes about config.py:
1. SECRET_KEY: A variable to store the secret key configuration for the Flask app. This key is required to create a secure Session in the Flask App.
2. PERMANENT_SESSION_LIFETIME: As the name suggests, it sets the maximum age of a permanent Flask Session.

#### logic Module Config {#logic-config}
Navigate to the folder named ***logic*** in the directory. Once you are inside the fodler create a new file, ***config.py***. Copy the following code into that file.

```py
# the directory containing the wavs of the songs to be fingerprinted.
files_folder = "wavs/song_wavs" 

# address to the recording generated by the webpage
test_rec = "TheMusicDictionary/rec_output.wav" 

# the database in which the app data(songs, fingerprints) is stored.
actual_schema = 'tmd_schema'

current_schema = actual_Schema

cnxn_conf = {
    'username': '',  # set your MySQL username for the connection
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
2. test_rec: Set this variable to the path of the *rec_output.wav* in your filesystem.

The config file in logic module is mainly to facilitate easy development and testing, and thus will be useful if you wish to change the behaviour of the logic module at one place. Neverthless, even if you don't intend to *experiement*, so to say it is still a lot easier to have all relevant config information in one place.

### Building the App
The next step is to build the app on your machine so it can recognise songs. The First Step would be decide which songs you would like to fingerprint. Once that has been decided store the songs in wav format in a directory on your computer and replace the address in the [logic config files](#logic-config).

```py
files_folder = "" # your songs directory
```

After you have done so. Its time to build the application. To do so simply run the ***build_database.sh*** file. This will fingeprint all the songs in files_folder and upload them to the database specified in the [logic config files](#logic-config).

Now we are almost done, with the hard part. 

### Running the Web Application.
All that's left is for you to run ***start.sh*** file and go to the link where the website is hosted on your local network. 

If everything worked correctly, *Congratulations you have a music recognition application installed on your machine*. Please reach out if anything fails or doesn't work. 

## Installation on Glitch
Song Recoginition won't work in Glitch ***at present*** because there is no server side database of songs. However, it is still possible to create accounts and record audio. These are completely working. 

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

+ Will Drevo's [Blog](https://willdrevo.com/fingerprinting-and-audio-recognition-with-python/) on Audiofingerprinting and his [Dejavu Repo](https://github.com/worldveil/dejavu) that helped me start this project.
+ Milos Miljkovic and his [instructive video](https://www.youtube.com/watch?v=xDFARS_oIfM&t) on PyLance, without which this project was just not going to work. Also thanks to his [repo](https://github.com/miishke/PyDataNYC2015)
+ Meinard Müller's Book, [Fundamentals of Music Processing](https://link.springer.com/book/10.1007/978-3-319-21945-5)
+ And lastly thanks to every one at Stackoverflow.
