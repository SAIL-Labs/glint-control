import bmc

dm = bmc.BmcDm()

old_serial = 'MultiUSB000'
serial = '32AW038#027'

err_code = dm.open_dm(serial)
if err_code:
    raise Exception(dm.error_string(err_code))

mapping = list(dm.default_mapping())

data = bmc.DoubleVector()
data.assign(dm.num_actuators(), 0.0)
dm.send_data(data)

monotonic_map = range(0, dm.num_actuators())
dm.send_data_custom_mapping(data, monotonic_map)

print('BMC error status:', dm.error_string(dm.get_status()))

dm.close_dm()
