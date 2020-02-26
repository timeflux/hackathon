from timeflux.core.node import Node
import pandas as pd


class Divide(Node):
    """ Divide data from one port by another
    Attributes:
        i_num (Port): Default input, expects DataFrame.
        i_den (Port): Default input, expects DataFrame.
        o (Port): Default output, provides DataFrame and meta.
    """
    def update(self):
        if not (self.i_num.ready() & self.i_den.ready()):
            return
        # check shapes 
        if not self.i_num.data.index.equals(self.i_den.data.index):
            self.logger.warning('Cannot divide data with different index')
        else:
            # divide
            self.o.data = pd.DataFrame(self.i_num.data.values / self.i_den.data.values,
                                       columns=self.i_num.data.columns, index=self.i_num.data.index)
            # propagate the meta
            self.o.meta = self.i_num.meta
            self.o.meta.update(self.i_den.meta)
