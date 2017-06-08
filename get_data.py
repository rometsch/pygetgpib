import visa;
import numpy as np;

# Open resource manager
rm = visa.ResourceManager();

# Specify resource here
my_resource = "GPIB::11"
inst = rm.open_resource(my_resource);

# Set Instrument Preset on the analyzer with "IP" command
# The programming manual requires that
inst.write("IP");
# Set analyzer output format to real number
# data is transfered as ASCII (see programming manual p.3-20)
inst.write("TDF P");
# Set analyzer to single sweep mode
inst.write("SNGLS");
# Set center frequency
inst.write("CF 300MZ");
# Set span
inst.write("SP 200MZ");
# Sweep once
inst.write("TS");
# Request trace A from the analyzer via "TRA?"
values_ASCII = inst.query_ascii_values('TRA?', converter='E');
print(values_ASCII);

# Set analyzer output to binary (faster).
# Data is given in measurement units in the range from 0...8000
# Each datapoint is 2 bytes = 16 bit long
# thus use the "short" datatype indicated by "h" (https://docs.python.org/2/library/struct.html#format-characters)
values_bin = inst.query_binary_values('TRA?', datatype='h', is_big_endian=True, container=np.array);
# Get the reference level to display values in volts
ref_level = inst.query('RL?');
values_volts = values_bin*ref_level*1./8000;
print(values_bin);
