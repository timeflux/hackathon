import numpy as np
import pandas as pd
from timeflux.nodes.window import Window


class MovingAverage(Window):
    """ TODO
    XXX TODO
    Attributes:
        i (Port): Default input, expects DataFrame.
        o (Port): Default output, provides DataFrame and meta.

    Args:
       length (float): The length of the window, in seconds.
        closed (str):
    """

    def __init__(self, length, step, closed='right'):

        super(self.__class__, self).__init__(length=length, step=step)
        self._closed = closed
        self._columns = None

    def update(self):

        if not self.i.ready():
            return
        if self._columns is None:
            self._columns = self.i.data.columns

        # At this point, we are sure that we have some data to process
        super(self.__class__, self).update()

        # if the window output is ready, fit the scaler with its values
        if self.o.ready():
            if self._closed == 'right':
                closed_index = -1
            elif self._closed =='left':
                closed_index = 0
            else: # center
                closed_index = len(self.i.data)//2
            time = self.i.data.index[closed_index]
            self.o.data = pd.DataFrame(np.mean(self.o.data.values, axis=0).reshape(1, -1),
                                        index=[time],
                                        columns=self._columns )
