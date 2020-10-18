##############################################################################################
#                           linear-filter-banks implementation
##############################################################################################
import numpy as np
from ..cutils.cythonfuncs import cymel_and_lin_helper
from ..utils.exceptions import ParameterError, ErrorMsgs


def linear_filter_banks(nfilts=20,
                        nfft=512,
                        fs=16000,
                        low_freq=None,
                        high_freq=None,
                        scale="constant"):
    """
    Compute linear-filterbanks. The filters are stored in the rows, the columns
    correspond to fft bins.

    Args:
        nfilts    (int) : the number of filters in the filterbank.
                          (Default 20)
        nfft      (int) : the FFT size.
                          (Default is 512)
        fs        (int) : sample rate/ sampling frequency of the signal.
                          (Default 16000 Hz)
        low_freq  (int) : lowest band edge of mel filters.
                          (Default 0 Hz)
        high_freq (int) : highest band edge of mel filters.
                          (Default samplerate/2)
        scale    (str)  : choose if max bins amplitudes ascend, descend or are constant (=1).
                          Default is "constant"

    Returns:
        (numpy array) array of size nfilts * (nfft/2 + 1) containing filterbank.
        Each row holds 1 filter.
    """
    # init freqs
    high_freq = high_freq or fs / 2
    low_freq = low_freq or 0

    # run checks
    if low_freq < 0:
        raise ParameterError(ErrorMsgs["low_freq"])
    if high_freq > (fs / 2):
        raise ParameterError(ErrorMsgs["high_freq"])

    # compute points evenly spaced in mels (points are in Hz)
    mel_points = np.linspace(low_freq, high_freq, nfilts + 2)

    # we use fft bins, so we have to convert from Hz to fft bin number
    bins = np.floor((nfft + 1) * mel_points / fs)

    # compute amps of fbanks
    fbank = cymel_and_lin_helper(scale, nfilts, nfft, bins)
    return np.abs(fbank)
