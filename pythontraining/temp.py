import pandas as pd
from sqlalchemy import select
from typing import List

from data.data import Session, engine
from data.model import Trip, Route, Location
from visualisations import maps

pd.read_sql(select(Location.lat, Location.lon. Route.))