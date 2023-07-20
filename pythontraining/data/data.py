import pandas as pd
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
path = Path(os.getenv("DATA_PATH"))

