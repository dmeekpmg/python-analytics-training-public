"""
Test the bunching algorithm across different datasets and libraries

For this exercise, both Polars and Pandas are expected to give the same
results. This function is able to test all variations and differnt 
datasets.
"""
import pandas as pd
import polars as pl
from polars import testing # pylint:disable=W0611
import pytest

from analysis import bunching


TEST_LIBRARIES = [
    (pd, "DataFrame", bunching.is_bunched),
    (pl, "DataFrame", bunching.is_bunched_pl),
    (pl, "LazyFrame", bunching.is_bunched_pl),
]

DATASETS = {
    "best_case": {
        "input_data": {
            'request_timestamp': [1, 1, 1],
            'short_name': ['a', 'a', 'a'],
            'direction_id': [0, 0, 0],
            'lat': [-33.1, -33.101, -33.2],
            'lon': [105, 105, 105],
        },
        'bunched': {'bunched': [True, True, False]}
    },
    "different_timestamps": {
        'input_data': {
            'request_timestamp': [1,  2],
            'short_name': ['a', 'a'],
            'direction_id': [0, 0],
            'lat': [-33.1, -33.1],
            'lon': [105, 105],
        },
        'bunched': {'bunched': [False, False]}
    }
}

testdata = [(*l, k) for l in TEST_LIBRARIES for k in DATASETS.keys()] #pylint:disable=C0201


@pytest.mark.parametrize("lib,frame_type,bunching_func,dataset_name", testdata)
def test_bunches_are_found(lib, frame_type, bunching_func, dataset_name):
    "Test bunching on multiple libraries and functions"
    df_factory = getattr(lib, frame_type)
    data = DATASETS[dataset_name]

    df = df_factory(data['input_data'])
    actual_df = bunching_func(df)
    
    expected_df = df_factory(data['input_data'] | data['bunched'])
    if frame_type == 'LazyFrame':
        expected_df = expected_df.collect()

    lib.testing.assert_frame_equal(expected_df, actual_df)
