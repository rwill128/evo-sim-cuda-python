#%%
import pandas
import numpy as np
from pandas import DataFrame

num_gas = 200000
x_values = np.random.randint(0, 1000 + 1, num_gas)
y_values = np.random.randint(0, 1000 + 1, num_gas)
gas: DataFrame = pandas.DataFrame({'x': x_values, 'y': y_values}, dtype=int)
num_plants = 10000
plant_x_values = np.random.randint(0, 1000 + 1, num_plants)
plant_y_values = np.random.randint(0, 1000 + 1, num_plants)
plant_energy_values = np.zeros(shape=num_plants, dtype=int)
plants: DataFrame = pandas.DataFrame.from_dict({'x': plant_x_values, 'y': plant_y_values, 'energy': plant_energy_values},
                                    dtype=int)


def count_energy_for_plants():
    gas['xy'] = gas.x.astype('string') + ',' + gas.y.astype('string')
    plants['xy'] = plants.x.astype('string') + ',' + plants.y.astype('string')
    grouped_by_xy: pandas.DataFrame = gas.groupby(['xy']).count()
    is_plant_present: pandas.Series = plants['xy'].isin(grouped_by_xy.index)
    only_present_plant_xys: pandas.Series = plants['xy'].loc[is_plant_present]
    counts: pandas.DataFrame = grouped_by_xy.loc[only_present_plant_xys.array]
    counts['energy'] = counts['x']
    counts.drop(['x', 'y'], axis='columns', inplace=True)
    energy_counted_plants = plants.set_index('xy')
    counts.sort_index(inplace=True)
    energy_counted_plants.sort_index(inplace=True)
    energy_counted_plants.drop_duplicates(inplace=True)
    energy_counted_plants['energy'] += counts['energy'].astype('int')
    energy_counted_plants.reset_index(inplace=True)


count_energy_for_plants()