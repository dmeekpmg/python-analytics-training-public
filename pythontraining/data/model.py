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
            cls.__name__ + 
            ", ".join(f"{attr}={cls.getattr(attr)!r}" for attr in attrs) + ")"
        )


class Agency(Base):
    __tablename__ = "agencies"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    url: Mapped[str] = mapped_column(String(50))
    timezone: Mapped[str] = mapped_column(String(20))
    lang: Mapped[str] = mapped_column(String(2))
    phone: Mapped[int]


    def __repr__(self) -> str:
        return _simple_repr(self, ['id', 'name', 'url'])


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[str] = mapped_column(primary_key=True)
    agency_id: Mapped[str]
    short_name: Mapped[str]
    long_name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(200))
    type: Mapped[int]
    color: Mapped[str] = mapped_column(String(6))
    text_color: Mapped[str] = mapped_column(String(6))
    exact_times: Mapped[str]

    def __repr__(self) -> str:
        attrs = ['id', 'agency_id', 'short_name', 'long_name', 'description']
        return _simple_repr(self, attrs)


class Shape(Base):
    __tablename__ = "shapes"

    id: Mapped[str] = mapped_column(primary_key=True)
    lat: Mapped[float]
    lon: Mapped[float]
    sequence: Mapped[int]
    dist_traveled: Mapped[float]

    def __repr__(self) -> str:
        attrs = ['id', 'lat', 'lon', 'sequence', 'dist_traveled']
        return _simple_repr(self, attrs)
    

class Stop(Base):
    __tablename__ = "stops"

    id: Mapped[str] = mapped_column(primary_key=True)
    code: Mapped[int]
    name: Mapped[str]
    lat: Mapped[float]
    lon: Mapped[float]
    wheelchair_boarding: Mapped[int]
    
    def __repr__(self) -> str:
        attrs = ['id', 'lat', 'lon', 'code', 'name']
        return _simple_repr(self, attrs)


class StopTime(Base):
    __tablename__ = "stop_times"

    trip_id: Mapped[str]
    arrival_time: Mapped[str]
    departure_time: Mapped[str]
    stop_id: Mapped[str] = mapped_column(primary_key=True)
    sequence: Mapped[int]
    stop_headsign: Mapped[str]
    pickup_type: Mapped[int]
    drop_off_type: Mapped[int]
    shape_dist_traveled: Mapped[float]
    timepoint: Mapped[int]
    stop_note: Mapped[str]
    
    def __repr__(self) -> str:
        attrs = ['trip_id', 'stop_id', 'arrival_time', 'departure_time', 'sequence']
        return _simple_repr(self, attrs)


class Trip(Base):
    __tablename__ = "trips"

    route_id: Mapped[str] = mapped_column(primary_key=True)
    service_id: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True)
    headsign: Mapped[str]
    direction_id: Mapped[int]
    wheelchair_accessible: Mapped[int]
    route_direction: Mapped[str]

    def __repr__(self) -> str:
        attrs = ['route_id', 'service_id', 'id', 'headsign']
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