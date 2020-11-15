#%%
import pandas
import numpy as np

gas =  pandas.DataFrame.from_dict({
    'x': [1, 2, 3, 3, 4, 5],
    'y': [1, 2, 3, 3, 4, 5]
})

plants =  pandas.DataFrame.from_dict({
    'x': [1, 3, 4, 5, 6],
    'y': [1, 3, 4, 5, 6]
})

gas['xy'] = gas.x.astype('string') + ',' + gas.y.astype('string')
plants['xy'] = plants.x.astype('string') + ',' + plants.y.astype('string')

grouped_by_xy = gas.groupby(['xy']).count()
is_plant_present = plants['xy'].isin(grouped_by_xy.index)
only_present_plant_xys = plants['xy'].loc[is_plant_present]
counts = grouped_by_xy.loc[only_present_plant_xys.array]

