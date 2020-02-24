# -*- coding: utf-8 -*-
"""Workshop utilities
    Created on december 2019
    Module containing utils functions for the workshop
"""

import logging

import mne
import numpy as np

from .tutorial_utils import estimate_rate

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

logging.getLogger("matplotlib").setLevel(logging.WARNING)


def pandas_to_mne(data, events=None, montage_kind='standard_1005', unit_factor=1e-6, bad_ch=[]):
    ''' Convert a pandas Dataframe into mne raw object 
    Parameters
    ----------
    data: Dataframe with index=timestamps, columns=eeg channels
    events: array, shape = (n_events, 3) with labels on the third axis. 
    unit_factor: unit factor to apply to get Voltage
    bad_ch: list of channels to reject 

    Returns
    -------
    raw: raw object
    '''
    n_chan = len(data.columns)

    X = data.copy().values
    times = data.index

    ch_names = list(data.columns)
    ch_types = ['eeg'] * n_chan
    montage = mne.channels.read_montage(montage_kind) if montage_kind is not None else None
    sfreq = estimate_rate(data)
    X *= unit_factor

    if events is not None:
        events_onsets = events.index
        events_labels = events.label.values
        event_id = {mk: (ii + 1) for ii, mk in enumerate(np.unique(events_labels))}
        ch_names += ['stim']
        ch_types += ['stim']

        trig = np.zeros((len(X), 1))
        for ii, m in enumerate(events_onsets):
            ix_tr = np.argmin(np.abs(times - m))
            trig[ix_tr] = event_id[events_labels[ii]]

        X = np.c_[X, trig]

    info = mne.create_info(ch_names=ch_names, ch_types=ch_types, sfreq=sfreq, montage=montage)
    info["bads"] = bad_ch
    raw = mne.io.RawArray(data=X.T, info=info, verbose=False)
    return raw
