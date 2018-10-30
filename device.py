#-----------------------------------------------------------
#
#	Wrapper class to provide an abstract representation
#	of an HP8591E Spectrum Analyzer
#
#	Author	:	Thomas Rometsch
#	Date	:	Aug. 8, 2017
#
#-----------------------------------------------------------
#	Note that you must call sweep before calling
#	commands like get_peak or get_trace to take a sweep
#	which means refreshing the spectrum on the analyzer.
#-----------------------------------------------------------
import gpib
import numpy as np
import time

class SpectrumAnalyzer:
	# Name and address of the gpib instrument as set in /etc/gpib.conf
	gpib_lib_name = "HP8591E";
	gpib_address = 18;

	def __init__(self):
		# Flag for peak search
		self.peak_searched = False;

		# Try to find the gpib device.
		self.dev = gpib.find(self.gpib_lib_name);
		# Reset dev
		self.reset();
		# Set to single sweep mode
		self.set_singlesweep();

	def read(self, length):
		# Read a number of bytes from the bus and return
		# a decoded string with the results
		ans = gpib.read(self.dev, length)
		return ans.decode("ASCII").strip()

	def write(self, scpi):
		# write a Standard Commands for Programmable Instruments (SCPI) to the device
		gpib.write(self.dev, scpi);

	def reset_flags(self):
		self.peak_searched = False;

	def reset(self):
		# Reset device with "IP"
		self.write("IP");
		time.sleep(3)

	def set_center_frequency(self, freq):
		# freq: center frequency in MHz
		self.write("CF {:.2f}MZ".format(freq));

	def set_span(self, span):
		# span: span in MHz
		self.write("SP {:.2f}MZ".format(span));

	def set_singlesweep(self):
		self.write("SNGLS");

	def sweep(self):
		# take one sweep
		self.write("TS");
		self.reset_flags();

	def find_peak(self):
		# Use the build in function of the spectrum analyzer to set the data marker
		# to the frequency with the highest amplitude.
		self.write("MKPK HI");
		self.peak_searched = True;

	def get_peak_amplitude(self):
		# Return amplitude of peak in dbm.
		if not self.peak_searched:
			self.find_peak();
		self.write("MKA?");
		ans = self.read(20);
		return float(ans)

	def get_peak_frequency(self):
		# Return frequency where the peak is located in MHz.
		if not self.peak_searched:
			self.find_peak();
		self.write("MKF?");
		ans = self.read(20);
		return float(ans);

	def get_peak(self):
		# Return a list with (frequency [MHz], amplitude [dBm]) of the peak
		rv = [self.get_peak_frequency(), self.get_peak_amplitude()];
        self.pead_searched = False:
        return rv

	def get_trace(self):
		# Return the data from the display as numpy array.
		self.write("TRA?");
		ans = self.read(10000); #TODO: find the correct number, this is probably too large
		vals = ans.split(",");
		return np.array(vals, dtype=float);
