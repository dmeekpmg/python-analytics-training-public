"""
Run this script from the pythontraining folder
e.g. python -m data.hydrate
"""

import pandas as pd
import zipfile
from typing import List, IO
from sqlalchemy import Table, delete

from data.data import zip_path, engine, Session
from data.model import Agency, Route, Shape, Stop, StopTime, Trip, Location, \
    _gtfs_table_registry_


def replace_table(table: Table, df: pd.DataFrame):
    # Clear existing records
    stmt = delete(table).where(1==1)
    with Session() as session:
        session.execute(stmt)
        session.commit()

    # Upload new records
    df.to_sql(table.__tablename__, engine, if_exists="append", index=False, 
              chunksize=20000)


def get_df(table: Table, f: IO):
    df_raw = pd.read_csv(f)
    cols_to_include = table._gtfs_fields_
    new_cols = [c.name for c in table.__table__.columns]
    col_mapping = dict(zip(cols_to_include, new_cols))

    df_result = df_raw[list(cols_to_include)].rename(columns=col_mapping)
    return df_result


def upload_gtfs_files():
    with zipfile.ZipFile(zip_path) as z:
        for table in _gtfs_table_registry_:
            print(table.__tablename__)
            with z.open(f"{table._gtfs_file_}.txt") as f:
                df = get_df(table, f)
                replace_table(table, df)


if __name__ == "__main__":
    upload_gtfs_files()