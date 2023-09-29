import pandas as pd


def restructure(df:pd.DataFrame) -> pd.DataFrame:
    """Restructure the shapes dataframe to one that is a little more succinct

    Args:
        shapes (pd.DataFrame): Raw shapes dataframe

    Returns:
        pd.DataFrame: Shapes dataframe with tidied names
    """
    return df.rename(columns={
        'shape_pt_lat': 'lat',
        'shape_pt_lon': 'lon'
    })

def add_end_lat_lon(df:pd.DataFrame) -> pd.DataFrame:
    """Add the end lat and lon. Requires the dataframe to be sorted

    Args:
        shapes (pd.DataFrame): Shapes dataframe

    Returns:
        pd.DataFrame: DataFrame with end_lat and end_lon added
    """
    df = df.sort_values(["shape_id", "shape_pt_sequence"])
    
    df[['end_lat', 'end_lon']] = (df
        .groupby('shape_id')[['lat', 'lon']]
        .transform(lambda df: df.shift(-1))
    )

    return df
