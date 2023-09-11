import pandas as pd
import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv


load_dotenv()
path = Path(os.getenv("DATA_PATH"))

con_str = os.getenv("SQLDRIVER")
engine = create_engine(con_str)
Session = sessionmaker(engine)