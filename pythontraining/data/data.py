import pandas as pd
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
data_path = Path(os.getenv("DATA_PATH"))

