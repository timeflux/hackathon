# -*- coding: utf-8 -*-
"""Workshop utilities
    Created on december 2019
    Module containing utils functions for the workshop
"""

import logging

import numpy as np
import pandas as pd
import yaml

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

logging.getLogger("matplotlib").setLevel(logging.WARNING)


def estimate_rate(data):
    """ Estimate nominal sampling rate of a DataFrame.
    This function checks if the index are correct, that is monotonic and regular
    (the jitter should not exceed twice the nominal timespan)
    Notes
    -----
    This function does not take care of jitters in the Index and consider that the rate as the 1/Ts
    where Ts is the average timespan between samples.
    Parameters
    ----------
    data: pd.DataFrame
        DataFrame with index corresponding to timestamp (either DatetimeIndex or floats)
    Returns
    -------
    rate: nominal rate of the DataFrame
    """
    # check that the index is monotonic
    # if not data.index.is_monotonic:
    # raise Exception('Data index should be monotonic')
    if data.shape[0] < 2:
        raise Exception('Sampling rate requires at least 2 points')

    if isinstance(data.index, (pd.TimedeltaIndex, pd.DatetimeIndex)):
        delta = data.index - data.index[0]
        index_diff = np.diff(delta) / np.timedelta64(1, 's')
    elif np.issubdtype(data.index, np.number):
        index_diff = np.diff(data.index)
    else:
        raise Exception('Dataframe index is not numeric')

    average_timespan = np.mean(index_diff)

    return 1 / average_timespan


def load_standalone_graph(path):
    # Load a graph for offline usage
    with open(path, 'r') as stream:
        try:
            graph = yaml.safe_load(stream)['graphs'][0]
        except yaml.YAMLError as exc:
            print(exc)
    graph_standalone = graph.copy()
    # Get rid of online specific nodes and edges (zmq, lsl, safeguards)
    graph_standalone['nodes'] = [node for node in graph['nodes'] if
                                 node['module'] not in ['timeflux.nodes.lsl', 'timeflux.nodes.zmq']]
    nodes_id = [node['id'] for node in graph_standalone['nodes']]

    def keep_edge(edge):
        return (edge['source'].split(':')[0] in nodes_id) and (edge['target'].split(':')[0] in nodes_id)

    graph_standalone['edges'] = [edge for edge in graph_standalone['edges'] if keep_edge(edge)]
    return graph_standalone
