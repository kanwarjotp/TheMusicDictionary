import hashlib

import matplotlib.mlab as mlab
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.mlab import specgram
from scipy.io import wavfile
from skimage.feature import peak_local_max


class Fingerprint:
    NFFT_VALUE = 4096
    OVERLAP_VALUE = 2048
    MIN_DISTANCE_PEAKS = 25  # decreasing minimum distance, increases the number of peaks found
    MIN_INTENSITY_OF_PEAKS = 30  # the more this value, less the noise errors
    MAX_SEGMENT_TO_FINGERPRINT = 15  # these number of peaks will be matched with a single peak
    TIME_INTERVAL_PRECISION = 3
    MIN_TIME_DIFF = 0  # min time diff between peak frequencies

    def __init__(
        self,
        song_address: str,
        song_id: int = 0,
        force_one_chnl: bool = True
        ):  # when song_id = 0, indicates a user's recording
        """

        :param song_address:  String representing the local address of the file\n
        :param song_id: A Unique Value, identifying the songs in the database \n\n
        :return: Fingerprint Object: exposes the get_fingerprint() method which returns a hash value, representing the fingerprint
        """
        self._song_id = song_id
        self._song = song_address
        self._wav_info = {}
        self._mono = force_one_chnl
        self._spectrum = {}
        self._coordinates = []
        self._peaks = []
        self._hashes = []

    def get_fingerprint(self, plot: bool = False, verbose: bool = False):
        """

        :param plot: Boolean, set True if the plots of spectrograms and peaks are desired, defaults to False
        :param verbose: Boolean, set True if detailed decriptions are desired, defaults to False

        :return: list containing hash values, representing the fingerprint for the song_address
        """
        self._convert_to_wav()
        if verbose: print("wav file generated")
        hashes_total = []
        num_hashes_gen = 0

        if len(self._wav_info['song_data'].shape) != 1 and not self._mono:
            channels = self._wav_info['song_data'].shape[1]
        else:
            # in case of a Single channel:
            channels = 1
            self._mono = True

        for channel in range(channels):  # iterating over the functions for each channel
            self._generate_spectrum(plot=plot, channel=channel)
            if verbose: print("spectrum generated for channel ", channel)

            self._find_peaks()
            if verbose: print("peaks generated in channel {0}: {1}".format(channel, len(self._peaks)))
            if plot: self._plot_spectrum()  # plot if requested

            self._generate_hash()
            if verbose: print("hash generated in channel {0}: {1}".format(channel, len(self._hashes)))
            num_hashes_gen += len(self._hashes)
            hashes_total += self._hashes

        if verbose: print("Total Hashes across {0} channel(s): {1}".format(channels, num_hashes_gen))

        return hashes_total

    def _convert_to_wav(self):
        sample_rate, song_data = wavfile.read(self._song)

        data_dict = {
            'sample_rate': sample_rate,
            'song_data': song_data
        }

        self._wav_info = data_dict

    def _generate_spectrum(self, plot: bool, channel: int):
        if not self._mono:
            song_channel = self._wav_info['song_data'][:, channel]
        else:
            song_channel = self._wav_info['song_data']
        # TODO: store the fingerprint with the offsets and song_id in the sql;ite3 database

        spectrum, freq, times = specgram(
            x=song_channel,
            Fs=self._wav_info['sample_rate'],
            NFFT=Fingerprint.NFFT_VALUE,
            noverlap=Fingerprint.OVERLAP_VALUE,
            window=mlab.window_hanning  # hanning to make the signal periodic
        )

        spectrum[spectrum == 0] = 1e-6  # changing 0 values to 1e-6
        Z = 10.0 * np.log10(spectrum)  # apply log transform since specgram() returns linear array
        Z = np.flipud(Z)  # inverting y-axis of spectrum

        self._spectrum = {
            'spectrum': Z,
            'times': times,
            'freq': freq
        }

        if plot: self._plot_spectrum()

    def _find_peaks(self):
        # finding peaks using scipy
        self._coordinates = peak_local_max(
            self._spectrum['spectrum'],
            min_distance=Fingerprint.MIN_DISTANCE_PEAKS,
            threshold_abs=Fingerprint.MIN_INTENSITY_OF_PEAKS
        )

        peaks = []  # list to store peaks for the songs

        ht_of_spec = self._spectrum['spectrum'].shape[0]
        wdt_of_spec = self._spectrum['spectrum'].shape[1]

        length_of_song = round(np.amax(self._spectrum['times']), Fingerprint.TIME_INTERVAL_PRECISION)
        max_freq_of_song = self._spectrum['freq'][-1]

        single_unit_time = round((length_of_song / wdt_of_spec), Fingerprint.TIME_INTERVAL_PRECISION)
        single_unit_freq = round((max_freq_of_song / ht_of_spec))

        for i in self._coordinates:
            # converting x coordinates to time in seconds
            time_coordinate = int(single_unit_time * i[1])

            # converting y coordinates to frequency in Hz
            freq_coordinates = round(single_unit_freq * (ht_of_spec - i[0]))

            # storing the pair in peaks
            peaks.append((time_coordinate, freq_coordinates))
            pass

        self._peaks = peaks

    def _generate_hash(self):
        # hashes are stored as (hash_vale, (song_id, time_offset))
        hashed = set()  # preventing redundant hashes

        hashes = []
        peaks = self._peaks

        for i in range(len(peaks)):
            for j in range(Fingerprint.MAX_SEGMENT_TO_FINGERPRINT):
                if i + j < len(peaks) and not (i, i + j) in hashed:
                    f1 = peaks[i][1]
                    f2 = peaks[i + j][1]
                    t1 = peaks[i][0]
                    t2 = peaks[i + j][0]
                    t_diff = t2 - t1

                    if t_diff >= Fingerprint.MIN_TIME_DIFF:
                        # hash this value
                        h = hashlib.sha1(("{0}{1}{2}".format(str(f1), str(f2), str(t_diff))).encode('utf-8'))
                        hashes.append((h.hexdigest()[0:20], (self._song_id, t1)))
                        # converting the string hash to a hexadecimal notation and truncating it to first 20 chars

                    hashed.add((i, i + j))

        self._hashes = hashes

    def _plot_spectrum(self):
        plt.figure(figsize=(20, 8), facecolor='white')

        if len(self._coordinates) != 0:  # draw peaks
            extent = 0, len(self._spectrum['times']), len(self._spectrum['freq']), 0
            plt.imshow(self._spectrum['spectrum'], cmap='viridis')
            plt.scatter(self._coordinates[:, 1], self._coordinates[:, 0])
            plt.xlabel('Spectrogram Width Units')
            plt.ylabel('Spectrogram Height Units')
            plt.title("Peaks: " + self._song_id, fontsize=18)
        else:
            extent = 0, np.amax(self._spectrum['times']), self._spectrum['freq'][0], self._spectrum['freq'][-1]
            plt.imshow(self._spectrum['spectrum'], cmap='viridis', extent=extent)
            plt.xlabel('Time bin')
            plt.ylabel('Frequency [Hz]')
            plt.title("Spectrum" + self._song_id)

        plt.axis('auto')
        ax = plt.gca()
        ax.set_xlim([extent[0], extent[1]])
        ax.set_ylim([extent[2], extent[3]])
        plt.show()
