from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


_gtfs_table_registry_: List[Table] = []


class Base(DeclarativeBase):
    pass


def _simple_repr(cls, attrs):
    return (
        cls.__class__.__name__
        + "("
        + ", ".join(f"{attr}={getattr(cls, attr)!r}" for attr in attrs)
        + ")"
    )


def register_gtfs(cls: Table):
    """Function decorator to make it easy to keep track of which classes
    need to be filled with GTFS data. Once the register is filled, we
    can just call each of these classes in turn to fill the data with
    the listed GTFS table and selected fields

    Returns:
        SQLAlchemy Table: This table will be added to the registry of
        GTFS tables. Each table should appear in the GTFS zip file
    """
    _gtfs_table_registry_.append(cls)
    return cls


@register_gtfs
class Agency(Base):
    __tablename__ = "agencies"
    _gtfs_fields_ = (
        "agency_id",
        "agency_name",
        "agency_url",
        "agency_timezone",
        "agency_lang",
        "agency_phone",
    )
    _gtfs_file_ = "agency"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    url: Mapped[str] = mapped_column(String(50))
    timezone: Mapped[str] = mapped_column(String(20))
    lang: Mapped[str] = mapped_column(String(2))
    phone: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return _simple_repr(self, ["id", "name", "url"])


@register_gtfs
class Calendar(Base):
    __tablename__ = "calendar"
    _gtfs_fields_ = (
        "service_id",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "start_date",
        "end_date",
    )
    _gtfs_file_ = "calendar"

    service_id: Mapped[int] = mapped_column(primary_key=True)
    monday: Mapped[int]
    tuesday: Mapped[int]
    wednesday: Mapped[int]
    thursday: Mapped[int]
    friday: Mapped[int]
    saturday: Mapped[int]
    sunday: Mapped[int]
    start_date: Mapped[int]
    end_date: Mapped[int]

    def __repr__(self) -> str:
        attrs = ["service_id", "start_date", "end_date"]
        return _simple_repr(self, attrs)


@register_gtfs
class Route(Base):
    __tablename__ = "routes"
    _gtfs_fields_ = (
        "route_id",
        "agency_id",
        "route_short_name",
        "route_long_name",
        "route_desc",
        "route_type",
        "route_color",
        "route_text_color",
    )
    _gtfs_file_ = "routes"

    id: Mapped[str] = mapped_column(primary_key=True)
    agency_id: Mapped[str]
    short_name: Mapped[str]
    long_name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(200))
    type: Mapped[int]
    color: Mapped[str] = mapped_column(String(6))
    text_color: Mapped[str] = mapped_column(String(6))

    trips: Mapped[List["Trip"]] = relationship(back_populates="route")
    locations: Mapped[List["Location"]] = relationship(
        back_populates="route"
    )

    def __repr__(self) -> str:
        attrs = ["id", "agency_id", "short_name", "long_name", "description"]
        return _simple_repr(self, attrs)


@register_gtfs
class Shape(Base):
    __tablename__ = "shapes"
    _gtfs_fields_ = (
        "shape_id",
        "shape_pt_sequence",
        "shape_pt_lat",
        "shape_pt_lon",
        "shape_dist_traveled",
    )
    _gtfs_file_ = "shapes"

    id: Mapped[str] = mapped_column(primary_key=True)
    sequence: Mapped[int] = mapped_column(primary_key=True)
    lat: Mapped[float]
    lon: Mapped[float]
    dist_traveled: Mapped[float]

    trips: Mapped[List["Trip"]] = relationship(back_populates="shape")

    def __repr__(self) -> str:
        attrs = ["id", "lat", "lon", "sequence", "dist_traveled"]
        return _simple_repr(self, attrs)


@register_gtfs
class Stop(Base):
    __tablename__ = "stops"
    _gtfs_fields_ = (
        "stop_id",
        "stop_name",
        "stop_lat",
        "stop_lon",
        "wheelchair_boarding",
    )
    _gtfs_file_ = "stops"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    lat: Mapped[float]
    lon: Mapped[float]
    wheelchair_boarding: Mapped[int]

    stop_times: Mapped[List["StopTime"]] = relationship(back_populates="stop")

    def __repr__(self) -> str:
        attrs = ["id", "lat", "lon", "name"]
        return _simple_repr(self, attrs)


@register_gtfs
class StopTime(Base):
    __tablename__ = "stop_times"
    _gtfs_fields_ = (
        "trip_id",
        "stop_sequence",
        "arrival_time",
        "departure_time",
        "stop_id",
        "stop_headsign",
        "pickup_type",
        "drop_off_type",
        "shape_dist_traveled",
        "timepoint",
        "stop_note",
    )
    _gtfs_file_ = "stop_times"

    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"), primary_key=True)
    stop_sequence: Mapped[int] = mapped_column(primary_key=True)
    arrival_time: Mapped[str]
    departure_time: Mapped[str]
    stop_id: Mapped[str] = mapped_column(ForeignKey("stops.id"))
    stop_headsign: Mapped[str] = mapped_column(nullable=True)
    pickup_type: Mapped[int]
    drop_off_type: Mapped[int]
    shape_dist_traveled: Mapped[float]
    timepoint: Mapped[int]
    stop_note: Mapped[str] = mapped_column(nullable=True)

    trips: Mapped[List["Trip"]] = relationship(back_populates="stop_times")
    stop: Mapped["Stop"] = relationship(back_populates="stop_times")

    def __repr__(self) -> str:
        attrs = [
            "trip_id",
            "stop_id",
            "arrival_time",
            "departure_time",
            "stop_sequence",
        ]
        return _simple_repr(self, attrs)


@register_gtfs
class Trip(Base):
    __tablename__ = "trips"
    _gtfs_fields_ = (
        "trip_id",
        "route_id",
        "service_id",
        "shape_id",
        "trip_headsign",
        "direction_id",
        "wheelchair_accessible",
        "route_direction",
    )
    _gtfs_file_ = "trips"

    id: Mapped[str] = mapped_column(primary_key=True)
    route_id: Mapped[str] = mapped_column(ForeignKey("routes.id"))
    service_id: Mapped[str]
    shape_id: Mapped[str] = mapped_column(ForeignKey("shapes.id"))
    trip_headsign: Mapped[str] = mapped_column(nullable=True)
    direction_id: Mapped[int]
    wheelchair_accessible: Mapped[int]
    route_direction: Mapped[str]

    route: Mapped["Route"] = relationship(back_populates="trips")
    shape: Mapped[List["Shape"]] = relationship(back_populates="trips", uselist=True)
    stop_times: Mapped[List["StopTime"]] = relationship(
        back_populates="trips", uselist=True
    )
    locations: Mapped[List["Location"]] = relationship(
        back_populates="trip"
    )

    def __repr__(self) -> str:
        attrs = ["route_id", "service_id", "id", "trip_headsign"]
        return _simple_repr(self, attrs)


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(primary_key=True)
    request_timestamp: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"))
    route_id: Mapped[str] = mapped_column(ForeignKey("routes.id"))
    schedule_relationship: Mapped[int]
    lat: Mapped[float] = mapped_column(nullable=True)
    lon: Mapped[float] = mapped_column(nullable=True)
    bearing: Mapped[float] = mapped_column(nullable=True)
    speed: Mapped[float] = mapped_column(nullable=True)
    timestamp: Mapped[int]
    congestion_level: Mapped[int]
    stop_id: Mapped[str] # Always blank
    vehicle_id: Mapped[str]
    label: Mapped[str]

    route: Mapped["Route"] = relationship(back_populates="locations")
    trip: Mapped["Trip"] = relationship(back_populates="locations")

    def __repr__(self) -> str:
        attrs = [
            "id",
            "trip_id",
            "route_id",
            "lat",
            "lon",
            "bearing",
            "speed",
            "timestamp",
            "congestion_level",
            "stop_id",
            "vehicle_id",
        ]
        return _simple_repr(self, attrs)
