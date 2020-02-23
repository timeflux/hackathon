import json

import pandas as pd
from timeflux.core.node import Node


class SerializeColumn(Node):

    def __init__(self, column_name='data'):
        super().__init__()
        self.column_name = column_name

    def update(self):
        if not self.i.ready():
            return
        self.o = self.i
        self.o.data[self.column_name] = self.o.data[self.column_name].apply(lambda d: json.dumps(d))


class ToSignal(Node):
    """ Extract meta from event and  convert in a signal
    Example:
    -------
    >>> events = tm.makeTimeDataFrame(5, freq='L').rename(columns={'A': 'label', 'B': 'data'})
    >>> labels = ['foo', 'bar', 'zaz', 'rer', 'foo']
    >>> data = [{'a': 1, 'b': 10}, {'a': 2, 'b': 20}, {}, {}, {'a': 1, 'c': 2},]
    >>> events.label = labels
    >>> events.data = data
    >>> events
                                label               data
        2000-01-01 00:00:00.000   foo  {'a': 1, 'b': 10}
        2000-01-01 00:00:00.001   bar  {'a': 2, 'b': 20}
        2000-01-01 00:00:00.002   zaz                 {}
        2000-01-01 00:00:00.003   rer                 {}
        2000-01-01 00:00:00.004   foo   {'a': 1, 'c': 2}
    >>> node = ToSignal(labels=['bar', 'foo'], meta_keys=['a', 'b'])
    >>> node.update()
    >>> node.o.data
                                label  a     b
        2000-01-01 00:00:00.001   bar  2  20.0
        2000-01-01 00:00:00.000   foo  1  10.0
        2000-01-01 00:00:00.004   foo  1   NaN


    """

    def __init__(self, meta_keys, labels=None, label_column='label', meta_column='data', drop_label=True):
        super().__init__()
        if isinstance(labels, str):
            labels = [labels]
        self._labels = labels
        if isinstance(meta_keys, str):
            meta_keys = [meta_keys]
        self._meta_keys = meta_keys
        self._label_column = label_column
        self._meta_column = meta_column
        self._drop_label = drop_label

    def update(self):
        if not self.i.ready():
            return

        self.o = self.i
        if self._labels is not None:
            idx = self.i.data[self._label_column].isin(self._labels)
            self.i.data = self.i.data.loc[idx]

        selected_meta = pd.DataFrame(index=self.i.data.index, columns=self._meta_keys)

        for meta_key in self._meta_keys:
            selected_meta[meta_key] = [a[meta_key] for a in self.i.data[self._meta_column].values]

        self.o.data = selected_meta

        if not self._drop_label:
            self.o.data = pd.concat([self.i.data[[self._label_column]], self.o.data], axis=1)
