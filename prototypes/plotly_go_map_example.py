#%%
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

import data

df_shapes = pd.read_csv(data.data.path / "shapes.txt")\
    .pipe(data.shapes.restructure)\
    .pipe(data.shapes.add_end_lat_lon)

df_shapes.sample(20)

#%%
# Get random sample of 5 ids

sample_ids = df_shapes.shape_id.sample(5)
nice_ids = [
    '2-CCN-sj2-31.49.R',
    '24-S12-4-sj2-1.1.R',
    '20-604-7-sj2-1.1.R',
    '2-CCN-sj2-31.87.H',
    '22-981-8-sj2-1.1.H',
    '2-CCN-sj2-31.41.H',
    '76-540-sj2-1.1.R',
    '76-224-sj2-1.3.R',
    '28-739-N-sj2-1.2.H'
]
sample_ids = nice_ids

print(list(sample_ids))
#%%

df_sample = df_shapes[df_shapes.shape_id.isin(nice_ids)]
fig = go.Figure()

for id, df_id in df_sample.groupby("shape_id"):
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

fig.show()

# %%
