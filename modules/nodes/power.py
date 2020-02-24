from timeflux.core.node import Node
from timeflux.nodes.window import Window
import numpy as np
import pandas as pd
import json


class Power(Window):
    """ Average of squared samples on a moving window
        Attributes:
            i (Port): Default input, expects DataFrame.
            o (Port): Default output, provides DataFrame and meta.

        Args:
            length (float): Window length
            step (float): Step length
            average (mean|median) : Average method
    """

    def __init__(self,
                 length,
                 step,
                 average='median'):

        super(self.__class__, self).__init__(length=length, step=step)
        if average == 'mean':
            self._average_method = np.median
        else:
            self._average_method = np.median

    def update(self):

        super(self.__class__, self).update()

        if not self.o.ready():
            return

        self.o.data = pd.DataFrame((self.o.data ** 2).apply(self._average_method),
                                   columns=[self.i.data.index[-1]]).T
