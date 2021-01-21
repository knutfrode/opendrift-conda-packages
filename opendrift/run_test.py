import opendrift

print("Trying to run a simulation..")
from datetime import timedelta
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.leeway import Leeway

lw = Leeway(loglevel=20)  # Set loglevel to 0 for debug information

# Atmospheric model for wind
#reader_arome = reader_netCDF_CF_generic.Reader('https://thredds.met.no/thredds/dodsC/mepslatest/meps_lagged_6_h_latest_2_5km_latest.nc')
reader_arome = reader_netCDF_CF_generic.Reader(lw.test_data_folder() +
    '16Nov2015_NorKyst_z_surface/arome_subset_16Nov2015.nc')

# Ocean model for current
#reader_norkyst = reader_netCDF_CF_generic.Reader('https://thredds.met.no/thredds/dodsC/mepslatest/meps_lagged_6_h_latest_2_5km_latest.nc')
reader_norkyst = reader_netCDF_CF_generic.Reader(lw.test_data_folder() +
    '16Nov2015_NorKyst_z_surface/norkyst800_subset_16Nov2015.nc')

#%%
# Adding readers successively, and specifying which variables they
# shall provide. This way, order of adding readers does not matter
lw.add_reader(reader_norkyst,
              variables=['x_sea_water_velocity', 'y_sea_water_velocity'])
lw.add_reader(reader_arome, variables=['x_wind', 'y_wind'])
lw.set_config('environment:fallback:x_sea_water_velocity', 0)
lw.set_config('environment:fallback:y_sea_water_velocity', 0)

#%%
# Seed leeway elements at defined position and time
object_type = 26  # 26 = Life-raft, no ballast
lw.seed_elements(lon=4.5, lat=59.6, radius=100, number=1000,
                 time=reader_arome.start_time, object_type=object_type)

#%%
# Running model
lw.run(duration=timedelta(hours=48), time_step=900, time_step_output=3600)

#%%
# Print and plot results
print(lw)

lw.plot(fast=True, filename = 'test.png')

