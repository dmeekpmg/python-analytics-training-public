"""
We are trying to find buses on the same route that are close to each
other.

If the rows could be sorted so that the next closest bus is in the next
row, then we could have a very fast search. However, buses could have
non-linear routes where sorting on one field leaves the nearest buses in
non-consecutive rows. Instead, we will do a cartesian product within
each route and request_timestamp.
"""


from typing import List

import pandas as pd
import polars as pl

LAT_ALLOWANCE = 0.002
LON_ALLOWANCE = 0.002


def is_bunched(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get a list of lat / lon that are bunches.
    Only compares lat and lon for each route and timestamp. Some routes may
    loop back on themselves and will incorrectly appear to have bunching
    """
    join_on = ["request_timestamp", "short_name", "direction_id"]
    bunched = (
        df.join(
            df.set_index(join_on), how="inner", on=join_on, lsuffix="1", rsuffix="2"
        )
        .query(
            "((lat1 != lat2) or (lon1 != lon2)) "
            f"and abs(lat1 - lat2) < {LAT_ALLOWANCE} "
            f"and abs(lon1 - lon2) < {LON_ALLOWANCE}"
        )[["request_timestamp", "short_name", "direction_id", "lat1", "lon1"]]
        .drop_duplicates()
        .rename(columns={"lat1": "lat", "lon1": "lon"})
        .assign(bunched=True)
    )
    df = df.join(
        bunched.set_index(join_on + ["lat", "lon"]),
        how="left",
        on=join_on + ["lat", "lon"],
    )
    df["bunched"] = df["bunched"].fillna(False)

    return df


def is_bunched_pl(df: [pl.DataFrame|pl.LazyFrame]) -> pl.DataFrame:
    """
    Get a list of lat / lon that are bunches.
    Only compares lat and lon for each route and timestamp. Some routes may
    loop back on themselves and will incorrectly appear to have bunching
    """
    join_on = ["request_timestamp", "short_name", "direction_id"]
    bunches = (
        df.join(df, how="inner", on=join_on)
        .filter(
            (
                (pl.col("lat") != pl.col("lat_right"))
                | (pl.col("lon") != pl.col("lon_right"))
            )
            & ((pl.col("lat") - pl.col("lat_right")).abs() < LAT_ALLOWANCE)
            & ((pl.col("lon") - pl.col("lon_right")).abs() < LON_ALLOWANCE)
        )
        .select("lat", "lon", "request_timestamp", "direction_id", "short_name")
        .unique()
        .with_columns(pl.lit(True).alias("bunched"))
    )

    df = df.join(bunches, how="left", on=join_on + ["lat", "lon"]).with_columns(
        pl.col("bunched").fill_null(False).alias("bunched")
    )
    try:
        return df.collect()
    except AttributeError:
        return df
