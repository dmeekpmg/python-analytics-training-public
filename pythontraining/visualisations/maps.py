import pandas as pd
import plotly.graph_objects as go


def add_positions(fig:go.Figure, lat_lon:pd.DataFrame) -> go.Figure:
    fig.add_trace(
        go.Scattermapbox(
            mode = "markers",
            lon=lat_lon['lon'],
            lat=lat_lon['lat']
        )
    )

    return fig

def add_routes(fig:go.Figure, route_shapes:pd.DataFrame) -> go.Figure:
    for id, df_id in route_shapes.groupby("shape_id"):
        fig.add_trace(
            go.Scattermapbox(
                mode = "lines",
                lon = df_id['lon'],
                lat = df_id['lat'],
                name = id
            )
        )
    
    return fig


def get_base_map(title=None) -> go.Figure:
    fig = go.Figure()

    fig.update_layout(
        title_text = title,
        margin = {'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': 151.206, 'lat': -33.88357},
            'style': "carto-positron",
            'zoom': 6
        },
        geo = dict(
            scope = 'asia',
            projection_type = 'azimuthal equal area',
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        ),
    )

    return fig


def routemap(route_shapes:pd.DataFrame) -> go.Figure:
    fig = get_base_map("Example bus routes")
    add_routes(fig, route_shapes)
    return fig


def position_map(lat_lon) -> go.Figure:
    fig = get_base_map("Example bus routes")
    add_positions(fig, lat_lon)
    return fig
