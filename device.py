#-----------------------------------------------------------
#	
#	Wrapper class to provide an abstract representation
#	of an HP8591E Spectrum Analyzer
#
#	Author	:	Thomas Rometsch
#	Date	:	Aug. 8, 2017
#	
#-----------------------------------------------------------
import gpib

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


	def write(self, scpi):
		# write a Standard Commands for Programmable Instruments (SCPI) to the device
		gpib.write(self.dev, scpi);
	
	def reset_flags(self):
		self.peak_searched = False;

	def reset(self):
		# Reset device with "IP"
		self.write("IP");

	def set_center_frequency(self, freq):
		# freq: center frequency in MHz
		self.write("CF {:.2f}MZ".format(freq));

	def set_span(self, span):
		# span: span in MHz
		self.write("SP {:.2f}MZ".format(span));

	def set_singlesweep(self):
		self.write("SNGLS");
		self.reset_flags();

	def sweep(self):
		# take one sweep
		self.write("TS");

	def find_peak(self):
		# Use the build in function of the spectrum analyzer to set the data marker
		# to the frequency with the highest amplitude.
		self.write("MKPH HI");

	def get_peak_amplitude(self):
		# Return amplitude of peak in dbm.
		if not self.peak_searched:
			self.find_peak();
		self.write("MKA?");
		ans = gpib.read(self.dev, 10);
		return ans.decode("UTF-8");
