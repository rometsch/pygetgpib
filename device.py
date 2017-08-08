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
	gpib_lib_name = "HP8591B";
	gpib_address = 18;

	def __init__(self):
		# Try to find the gpib device.
		self.dev = gpib.find(self.gpib_lib_name);
		# Reset dev
		self.reset();

	def reset(self):
		# Reset device with "IP"
		gpib.write(self.dev, "IP");
