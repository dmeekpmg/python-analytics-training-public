import os
from pathlib import Path
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv


load_dotenv()
FILENAME_SCHEDULE = 'gtfs.zip'

path = Path(os.getenv("DATA_PATH"))
zip_path = Path(path / FILENAME_SCHEDULE)

con_str = os.getenv("SQLDRIVER")
engine = create_engine(con_str)
Session = sessionmaker(engine)

