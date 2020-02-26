from timeflux.core.node import Node
import numpy as np
import pandas as pd
from scipy.stats import linregress


def _zero_crossing_rate(x):
    return len(np.where(np.diff(np.sign(x)))[0]) / len(x)


class TemporalFeatures(Node):

    def update(self):
        outputs = {}
        for _, suffix, port in self.iterate('i*'):
            if port.ready():
                index = port.data.index.values[-1]
                list_features = []
                data = port.data
                list_features.append(data.std().add_suffix('_std'))
                list_features.append(data.max().add_suffix('_max'))
                list_features.append(data.apply(_zero_crossing_rate).add_suffix('_zcr'))
                list_features.append(data.abs().std().add_suffix('_astd'))
                print(port.meta)
                outputs['o' + suffix] = {'meta': port.meta,
                                         'data': pd.concat(list_features).to_frame(index).T}
        for port_name, port_data in outputs.items():
            o = getattr(self, port_name)
            o.data = port_data['data']
            o.meta = port_data['meta']


class TKEO(Node):
    """

    Notes:
    ------
    """

    def __init__(self):
        self._previous = None
        self._columns = None

    def update(self):
        if not self.i.ready():
            return

        if self._columns is None:
            self._columns = self.i.data.columns
        else:
            self.i.data = self._previous.append(self.i.data)
        x = self.i.data.values
        tkeo = np.power(x[1:-1], 2) - np.multiply(x[2:], x[:-2])
        self._previous = self.i.data
        self.o.data = pd.DataFrame(tkeo, columns=self._columns, index=self.i.data.index[1:-1])


class DetectBurst(Node):
    """
    Notes:
    ------
    """

    def __init__(self, intensity):
        self._intensity = intensity

        self._signal_sum = None
        self._signal_samples = 0
        self._energy_max = None
        self._last_burst = pd.DataFrame()
        self._labels = {-1: 'burst_ends', 1: 'burst_begins'}
        self._previous = pd.DataFrame()
        self._threshold = None
        self._signal_ready = self._energy_ready = False
        self._above_thres = []

    def update(self):
        self._update_threshold()

        if self.i_energy.ready() and self._threshold is not None:
            # if we want a boolean activation
            # burst = (self._previous.append(self.i_energy.data) > self._threshold).astype(float)
            self._above_thres.append(self.i_energy.data[self.i_energy.data > self._threshold])

            _tmp = pd.concat(self._above_thres).dropna()
            _max = _tmp.mean() + _tmp.std()  # todo; until convergence!
            # if we want scaled activation between 0 and 1
            burst = self._previous.append(self.i_energy.data)

            burst = burst / _max

            # events = pd.DataFrame()
            # for time, rows in burst.diff().replace(0., np.NaN).dropna(how='all').iterrows():
            #     for column in rows.dropna().index:
            #         events = events.append(pd.DataFrame(np.array([self._labels[rows[column]],
            #                                                       {'column': column}]).reshape(1, -1),
            #                                             index=[time],
            #                                             columns=['label', 'data']))
            self.o.data = burst
            self._previous = self.i_energy.data.iloc[[-1], :]
            # if not events.empty:
            #     self.o_events.data = events

    def _update_threshold(self):
        if self.i_signal.ready():
            self._signal_samples += len(self.i_signal.data)
            if not self._signal_ready:
                self._signal_sum = self.i_signal.data.sum()
                self._signal_mean = self._signal_sum / self._signal_samples
                self._signal_sumsq = ((self.i_signal.data - self._signal_mean) ** 2).sum()
                self._signal_std = self._signal_sumsq / self._signal_samples
                self._signal_ready = True
            else:
                self._signal_sum += self.i_signal.data.sum()
                self._signal_mean = self._signal_sum / self._signal_samples
                self._signal_std = np.sqrt((self._signal_sumsq / self._signal_samples))
        if self.i_energy.ready():
            if not self._energy_ready:
                self._energy_max = self.i_energy.data.max()
                self._energy_ready = True
            else:
                self._energy_max = np.maximum(self._energy_max, self.i_energy.data.max())

        if self._signal_ready and self._energy_ready:
            self._threshold_0_perc_level = (- self._signal_mean) / self._signal_std
            self._threshold_100_perc_level = (self._energy_max - self._signal_mean) / self._signal_std
            self._threshold = pd.concat([self._threshold_0_perc_level, self._threshold_100_perc_level], axis=1).apply(
                self._estimate_threshold, axis=1)

    def _estimate_threshold(self, x):
        """
        Regression function that with a percent input gives an absolute value of the threshold
        level (used in the muscular activation detection algorithm).
        Converts a relative threshold level to an absolute value.
        """
        self._slope, self._intercept = linregress([0, 100], x.values)[:2]
        return self._slope * self._intensity + self._intercept
