"""timeflux_omind.nodes.math: simple mathematic nodes"""

from timeflux.core.node import Node


class Fillna(Node):
    def __init__(self, **kwargs):
        ''' Fill NA/NaN values using the specified method
        Attributes:
            i (Port): Default input, expects DataFrame.
            o (Port): Default output, provides DataFrame and meta.

        '''
        super().__init__()
        self._kwargs = kwargs
        self._kwargs['inplace'] = True

    def update(self):
        if self.i.ready():
            self.o = self.i
            self.o.data.fillna(**self._kwargs)


class SumColumns(Node):
    def __init__(self, name='A'):
        ''' Sum columns of a Dataframe
        Attributes:
            i (Port): Default input, expects DataFrame.
            o (Port): Default output, provides DataFrame and meta.

        Args:
            name (str): Name of output columns
        '''
        super().__init__()
        self._name = name

    def update(self):
        if self.i.ready():
            self.o.meta = self.i.meta
            self.o.data = self.i.data.sum(axis=1).to_frame(self._name)
