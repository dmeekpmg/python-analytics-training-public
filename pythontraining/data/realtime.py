import os
import requests
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
from typing import List
import pandas as pd
from datetime import datetime
from data.model import Location
from data.data import engine


load_dotenv()
BASE_URL = "https://api.transport.nsw.gov.au"
BUS_POSITION_URI = f"{BASE_URL}/v1/gtfs/vehiclepos/buses"


app_name = os.getenv("APP_NAME")
api_key = os.getenv("API_KEY")


headers = {
    "Authorization": f"apikey {api_key}"
}
request_details = dict(
    headers=headers,
    stream=True
)
if cert:=os.getenv("CERT", None):
    request_details['verify'] = cert


def flatten_entity(position:dict) -> dict:
    """
    live data arrives in the following format and needs to be flattened:
    {
        'id': '33553_26249868_2436_600_1',
        'vehicle': {
            'trip': {
                'trip_id': '1954191',
                'start_time': '19:40:00',
                'start_date': '20230911',
                'schedule_relationship': 0,
                'route_id': '2436_600'
            },
            'position': {
                'latitude': -33.71885299682617,
                'longitude': 151.10745239257812,
                'bearing': 44.0,
                'speed': 15.300000190734863
            },
            'timestamp': 1694428312,
            'congestion_level': 1,
            'vehicle': {
                'id': '33553_26249868_2436_600_1'
            },
            'occupancy_status': 1
        }
    }

    Args:
        position (dict): _description_

    Returns:
        dict: _description_
    """
    row = {}
    row["id"] = position["id"]

    trip = position["vehicle"]["trip"]
    row["trip_id"] = trip.get("trip_id","")
    row["route_id"] = trip.get("route_id","")
    row["schedule_relationship"] = trip.get("schedule_relationship","")

    if "position" in position['vehicle']:
        row["lat"] = position["vehicle"]["position"].get("latitude","")
        row["lon"] = position["vehicle"]["position"].get("longitude","")
        row["bearing"] = position["vehicle"]["position"].get("bearing","")
        row["speed"] = position["vehicle"]["position"].get("speed","")
    else:
        # Example for debugging, too few Nones
        row['lat'], row['lon'], row['bearing'], row['speed'] = None, None, None, None
    
    row["timestamp"] = position["vehicle"].get("timestamp","")
    row["congestion_level"] = position["vehicle"].get("congestion_level","")
    row["stop_id"] = position["vehicle"].get("stop_id","")
    row["vehicle_id"] = position["vehicle"]["vehicle"].get("id","")
    row["label"] = position["vehicle"]["vehicle"].get("label","")

    return row


def get_positions_dataframe(positions:List[dict]) -> pd.DataFrame:
    # Example for debugging: Forget to search for ['entity']
    df = pd.DataFrame([flatten_entity(e) for e in positions['entity']])
    df['request_timestamp'] = positions['header']['timestamp']
    return df


def get_latest_positions() -> List[dict]:
    """Return a dictionary of positions

    Returns:
        dict: _description_
    """
    response = requests.get(BUS_POSITION_URI, **request_details)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    positions = protobuf_to_dict(feed)
    return positions


def upload_realtime(df: pd.DataFrame):
    df.to_sql("locations", engine, if_exists="append", index=False)


def fetch_and_upload_positions():
    positions = get_latest_positions()
    df = get_positions_dataframe(positions)
    upload_realtime(df)


if __name__ == "__main__":
    fetch_and_upload_positions()