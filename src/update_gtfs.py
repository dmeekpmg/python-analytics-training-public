"""
Run this script from the pythontraining folder
e.g. python -m data.hydrate
"""

import os
from pathlib import Path
from typing import IO
import zipfile
import requests

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import Table, delete

from data.data import zip_path, engine, Session
from data.model import _gtfs_table_registry_


load_dotenv()

FILENAME_SCHEDULE = 'gtfs.zip'
app_name = os.getenv("APP_NAME")
api_key = os.getenv("API_KEY")

BASE_URL = "https://api.transport.nsw.gov.au"
BUS_POSITION_URI = f"{BASE_URL}/v1/gtfs/vehiclepos/buses"
BUS_SCHEDULE_URI = f"{BASE_URL}/v1/gtfs/schedule/buses"
FERRY_POSITION = f"{BASE_URL}/v1/gtfs/historical"

def download_gtfs():
    """Download GTFS data and save to the configured zip folder
    """
    headers = {
        "Authorization": f"apikey {api_key}"
    }
    request_details = {
        "timeout": 50,
        "headers": headers,
        "stream": True
    }
    # On our network, we need to add a certificate or the request will fail
    # Look at the readme for instructions on how to set this up
    if cert:=os.getenv("CERT", None):
        request_details['verify'] = cert

    response = requests.get(BUS_SCHEDULE_URI, **request_details)

    with open(zip_path, "wb") as f:
        f.write(response.content)


def replace_table(table: Table, df: pd.DataFrame):
    """Upload data to a given table and replace any existing data

    Args:
        table (Table): SQLAlchemy table
        df (pd.DataFrame): Pandas dataframe that matches the table schema
    """
    # Clear existing records
    stmt = delete(table).where(1==1)
    with Session() as session:
        session.execute(stmt)
        session.commit()

    # Upload new records
    df.to_sql(table.__tablename__, engine, if_exists="append", index=False, 
              chunksize=20000)


def get_df(table: Table, file: IO) -> pd.DataFrame:
    """Read a CSV from the downloaded GTFS zip file

    Args:
        table (Table): SQLAlchemy table, used to get the fields to expect
        file (IO): Path to a file

    Returns:
        pd.DataFrame: Pandas dataframe of the CSV
    """
    df_raw = pd.read_csv(file)
    cols_to_include = table._gtfs_fields_
    new_cols = [c.name for c in table.__table__.columns]
    col_mapping = dict(zip(cols_to_include, new_cols))

    df_result = df_raw[list(cols_to_include)].rename(columns=col_mapping)
    return df_result


def upload_gtfs_files():
    """Upload all CSV files from the GTFS zip. Uses the SQLAlchemy table
    definitions to figure out which tables are included
    """
    with zipfile.ZipFile(zip_path) as z:
        for table in _gtfs_table_registry_:
            print(table.__tablename__)
            with z.open(f"{table._gtfs_file_}.txt") as f:
                table_data = get_df(table, f)
                replace_table(table, table_data)


if __name__ == "__main__":
    download_gtfs()
    upload_gtfs_files()
