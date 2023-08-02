import pandas as pd
import plotly.graph_objects as go

def routemap(route_shapes:pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    for id, df_id in route_shapes.groupby("shape_id"):
        fig.add_trace(
            go.Scattermapbox(
                mode = "lines",
                lon = df_id['lon'],
                lat = df_id['lat'],
                name=id
            )
        )

    fig.update_layout(
        title_text = 'Example bus routes',
        margin ={'l':0,'t':0,'b':0,'r':0},
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
