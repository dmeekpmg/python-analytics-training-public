from typing import List

import pandas as pd
import polars as pl


def is_bunched(df: pd.DataFrame) -> List[bool]:
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
            "and abs(lat1 - lat2) < 0.002 "
            "and abs(lon1 - lon2) < 0.002"
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


def is_bunched_pl(df: pl.DataFrame) -> pl.DataFrame:
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
            & ((pl.col("lat") - pl.col("lat_right")).abs() < 0.002)
            & ((pl.col("lon") - pl.col("lon_right")).abs() < 0.002)
        )
        .select("lat", "lon", "request_timestamp", "direction_id", "short_name")
        .unique()
        .with_columns(pl.lit(True).alias("bunched"))
    )

    df = df.join(bunches, how="left", on=join_on + ["lat", "lon"]).with_columns(
        pl.col("bunched").fill_null(False).alias("bunched")
    )
    return df


def is_bunched_pl_lazy(df: pl.LazyFrame) -> pl.DataFrame:
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
            & ((pl.col("lat") - pl.col("lat_right")).abs() < 0.002)
            & ((pl.col("lon") - pl.col("lon_right")).abs() < 0.002)
        )
        .select("lat", "lon", "request_timestamp", "direction_id", "short_name")
        .unique()
        .with_columns(pl.lit(True).alias("bunched"))
    )

    df = df.join(bunches, how="left", on=join_on + ["lat", "lon"]).with_columns(
        pl.col("bunched").fill_null(False).alias("bunched")
    )
    return df.collect()
