"Fetch locations"
from sqlalchemy import select
import pandas as pd

from data.model import Location, Route, Trip
from data.data import engine


def get_locations() -> pd.DataFrame:
    stmt = (
        select(
            Location.lat,
            Location.lon,
            Location.bearing,
            Location.speed,
            Location.request_timestamp,
            Trip.direction_id,
            Trip.route_direction,
            Route.short_name,
        )
        .select_from(Location)
        .join(Route, Location.route_id == Route.id)
        .join(Trip, Location.trip_id == Trip.id)
    )

    locations = pd.read_sql(stmt, engine)
    return locations