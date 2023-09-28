"Test simple data processing"
import pandas as pd

from src.data import shapes


def test_restructure():
    "Rename columns"
    df = pd.DataFrame({
        'shape_pt_lat': [1, 2, 3],
        'shape_pt_lon': [5, 6, 7]
    }).pipe(shapes.restructure)
    assert(list(df.columns) == ['lat', 'lon'])


def test_add_end_lat_lon():
    "Add starting and ending lat and lon to a shape"
    df_in = pd.DataFrame({
        'shape_id': [1, 1, 1, 2, 2, 2],
        'shape_pt_sequence': [1, 3, 2, 7, 5, 6],
        'lat': [1, 2, 3, 4, 5, 6],
        'lon': [5, 6, 7, 8, 9, 10.2]
    })
    df_out = pd.DataFrame({
        'shape_id': [1, 1, 1, 2, 2, 2],
        'shape_pt_sequence': [1, 2, 3, 5, 6, 7],
        'lat': [1, 3, 2, 5, 6, 4,],
        'lon': [5, 7, 6, 9, 10.2, 8],
        'end_lat': [3, 2, None, 6, 4, None],
        'end_lon': [7, 6, None, 10.2, 8, None]
    }).reset_index(drop=True)
    df = shapes.add_end_lat_lon(df_in).reset_index(drop=True)
    assert(df.equals(df_out))