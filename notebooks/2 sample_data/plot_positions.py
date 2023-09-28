#%%[markdown]
# # Simple plot positions script

# In VSCode, this script works similar to a notebook.
# You can either run start to end using the terminal, or you
# can run in interactive mode

#%%
import pandas as pd

from data import data, shapes
from visualisations import maps as vis_maps

#%%
df_shapes = pd.read_csv(data.path / "shapes.txt")\
    .pipe(shapes.restructure)\
    .pipe(shapes.add_end_lat_lon)

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
fig = vis_maps.routemap(df_sample)
fig.show()
