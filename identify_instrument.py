import visa

# Open resource manager
rm = visa.ResourceManager();

# Specify resource here
my_resource = "GPIB::11"
my_instrument = rm.open_resource(my_resource);

print(my_instrument.query('*IDN?'))
