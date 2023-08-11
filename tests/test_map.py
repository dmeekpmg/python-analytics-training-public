import pandas as pd
from plotly.graph_objects import Figure

from pythontraining.visualisations import maps


def test_map():
    # Test that a plot is produced
    df = pd.DataFrame({
        "shape_id":["2-CCN-sj2-31.41.H","2-CCN-sj2-31.41.H","2-CCN-sj2-31.41.H","2-CCN-sj2-31.41.H","2-CCN-sj2-31.41.H"],
        "lat":[-33.883672,-33.884792,-33.885092,-33.8853,-33.885368],
        "lon":[151.20648,151.2056,151.205312,151.20504,151.204912],
        "shape_pt_sequence":[1,2,3,4,5],
        "shape_dist_traveled":[0.0,1424.3595051812,1840.2248680091,2182.6398209536,2327.5811884096],
        "end_lat":[-33.884792,-33.885092,-33.8853,-33.885368,-33.885584],
        "end_lon":[151.2056,151.205312,151.20504,151.204912,151.20456]
    }, index=["487515", "487516", "487517", "487518", "487519"]
    )
    fig = maps.routemap(df)
    assert(isinstance(fig, Figure))