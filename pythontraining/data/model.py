from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass


def _simple_repr(cls, attrs):
        return (
            cls.__class__.__name__ + "(" + 
            ", ".join(f"{attr}={getattr(cls, attr)!r}" for attr in attrs) + ")"
        )

_gtfs_table_registry_ = []


def register_gtfs(cls):
    _gtfs_table_registry_.append(cls)
    return cls


@register_gtfs
class Agency(Base):
    __tablename__ = "agencies"
    _gtfs_fields_ = ('agency_id', 'agency_name', 'agency_url', 'agency_timezone',
                     'agency_lang', 'agency_phone')
    _gtfs_file_ = 'agency'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    url: Mapped[str] = mapped_column(String(50))
    timezone: Mapped[str] = mapped_column(String(20))
    lang: Mapped[str] = mapped_column(String(2))
    phone: Mapped[int] = mapped_column(nullable=True)


    def __repr__(self) -> str:
        return _simple_repr(self, ['id', 'name', 'url'])


@register_gtfs
class Calendar(Base):
    __tablename__ = "calendar"
    _gtfs_fields_ = ('service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 
                     'friday', 'saturday', 'sunday', 'start_date', 'end_date')
    _gtfs_file_ = 'calendar'

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
        attrs = ['service_id', 'start_date', 'end_date']
        return _simple_repr(self, attrs)
    


@register_gtfs
class Route(Base):
    __tablename__ = "routes"
    _gtfs_fields_ = ('route_id', 'agency_id', 'route_short_name', 'route_long_name',
                    'route_desc', 'route_type', 'route_color', 'route_text_color')
    _gtfs_file_ = 'routes'

    id: Mapped[str] = mapped_column(primary_key=True)
    agency_id: Mapped[str]
    short_name: Mapped[str]
    long_name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(200))
    type: Mapped[int]
    color: Mapped[str] = mapped_column(String(6))
    text_color: Mapped[str] = mapped_column(String(6))

    trips: Mapped[List["Trip"]] = relationship(back_populates="route")

    def __repr__(self) -> str:
        attrs = ['id', 'agency_id', 'short_name', 'long_name', 'description']
        return _simple_repr(self, attrs)


@register_gtfs
class Shape(Base):
    __tablename__ = "shapes"
    _gtfs_fields_ = ('shape_id', 'shape_pt_sequence', 'shape_pt_lat', 'shape_pt_lon', 
                     'shape_dist_traveled')
    _gtfs_file_ = 'shapes'

    id: Mapped[str] = mapped_column(primary_key=True)
    sequence: Mapped[int] = mapped_column(primary_key=True)
    lat: Mapped[float]
    lon: Mapped[float]
    dist_traveled: Mapped[float]

    def __repr__(self) -> str:
        attrs = ['id', 'lat', 'lon', 'sequence', 'dist_traveled']
        return _simple_repr(self, attrs)
    

@register_gtfs
class Stop(Base):
    __tablename__ = "stops"
    _gtfs_fields_ = ('stop_id', 'stop_name', 'stop_lat', 'stop_lon', 
                     'wheelchair_boarding')
    _gtfs_file_ = 'stops'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    lat: Mapped[float]
    lon: Mapped[float]
    wheelchair_boarding: Mapped[int]
    
    def __repr__(self) -> str:
        attrs = ['id', 'lat', 'lon', 'code', 'name']
        return _simple_repr(self, attrs)


@register_gtfs
class StopTime(Base):
    __tablename__ = "stop_times"
    _gtfs_fields_ = ('trip_id', 'stop_sequence', 'arrival_time', 'departure_time', 'stop_id', 
                     'stop_headsign', 'pickup_type', 'drop_off_type',
                     'shape_dist_traveled', 'timepoint', 'stop_note')
    _gtfs_file_ = 'stop_times'

    trip_id: Mapped[str] = mapped_column(primary_key=True)
    stop_sequence: Mapped[int] = mapped_column(primary_key=True)
    arrival_time: Mapped[str]
    departure_time: Mapped[str]
    stop_id: Mapped[str]
    stop_headsign: Mapped[str] = mapped_column(nullable=True)
    pickup_type: Mapped[int]
    drop_off_type: Mapped[int]
    shape_dist_traveled: Mapped[float]
    timepoint: Mapped[int]
    stop_note: Mapped[str] = mapped_column(nullable=True)
    
    def __repr__(self) -> str:
        attrs = ['trip_id', 'stop_id', 'arrival_time', 'departure_time', 'sequence']
        return _simple_repr(self, attrs)


@register_gtfs
class Trip(Base):
    __tablename__ = "trips"
    _gtfs_fields_ = ('route_id', 'trip_id', 'service_id', 'shape_id', 'trip_headsign',
                     'direction_id', 'wheelchair_accessible', 'route_direction')
    _gtfs_file_ = 'trips'

    route_id: Mapped[str] = mapped_column(
        ForeignKey("routes.id"), 
        primary_key=True
    )
    trip_id: Mapped[str] = mapped_column(primary_key=True)
    service_id: Mapped[str]
    shape_id: Mapped[str] = mapped_column(ForeignKey("shapes.id"))
    trip_headsign: Mapped[str] = mapped_column(nullable=True)
    direction_id: Mapped[int]
    wheelchair_accessible: Mapped[int]
    route_direction: Mapped[str]

    route: Mapped[List["Route"]] = relationship(back_populates="trips")

    shape: Mapped[List["Shape"]] = relationship(
        order_by="asc(Shape.sequence)",
        primaryjoin="Trip.shape_id == Shape.id",
    )

    def __repr__(self) -> str:
        attrs = ['route_id', 'service_id', 'trip_id', 'trip_headsign']
        return _simple_repr(self, attrs)
    

class Location(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(primary_key=True)
    trip_id: Mapped[str]
    route_id: Mapped[str]
    schedule_relationship: Mapped[int]
    lat: Mapped[float]
    lon: Mapped[float]
    bearing: Mapped[float]
    speed: Mapped[float]
    timestamp: Mapped[int]
    congestion_level: Mapped[int]
    stop_id: Mapped[str]
    vehicle_id: Mapped[str]
    label: Mapped[str]


    def __repr__(self) -> str:
        attrs = ['id', 'trip_id', 'route_id', 'latitute', 'longitude', 'bearing',
                 'speed', 'timestamp', 'congestion_level', 'stop_id', 'vehicle_id']
        return _simple_repr(self, attrs)