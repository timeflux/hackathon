"""Basic sliding window."""

from timeflux.core.node import Node
import pandas as pd


class FixedWindow(Node):

    def __init__(self, length, step=None):
        """
        Initialize the buffer.

        Args:
            length (int): The length of the window, in samples.
            step (int): The sliding step, in samples.
                If None (the default), the step will be set to the window duration.
                If 0, the data will be sent as soon as it is available.
        """

        if step is None: step = length
        self._length = length
        self._step = step
        self._buffer = None

    def update(self):
        if not self.i.ready():
            return

        # Append new data
        if self._buffer is None:
            self._buffer = self.i.data
        else:
            self._buffer = self._buffer.append(self.i.data)

        # Make sure we have enough data
        if len(self._buffer) >= self._length:
            self.o.data = self._buffer[-self._length:]
            # Step
            self._buffer = self.o.data[self._step:]


