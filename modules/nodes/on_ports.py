from timeflux.core.node import Node
import pandas as pd


class Divide(Node):
    def update(self):
        if not (self.i_num.ready() & self.i_den.ready()):
            return
        # check shapes 
        if not self.i_num.data.index.equals(self.i_den.data.index):
            self.logger.warning('Cannot divide data with different index')
        else:
            self.o.data = pd.DataFrame(self.i_num.data.values / self.i_den.data.values,
                                       columns=self.i_num.data.columns, index=self.i_num.data.index)
