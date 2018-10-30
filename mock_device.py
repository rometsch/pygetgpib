#-----------------------------------------------------------
#
#   Mock class to develop applications based on the
#   wrapper class in device.py
#
#   Author  :   Thomas Rometsch
#   Date    :   Oct. 30, 2018
#
#-----------------------------------------------------------
#   Note that you must call sweep before calling
#   commands like get_peak or get_trace to take a sweep
#   which means refreshing the spectrum on the analyzer.
#-----------------------------------------------------------
import numpy as np

class SpectrumAnalyzer:
    # Name and address of the gpib instrument as set in /etc/gpib.conf
    gpib_lib_name = "HP8591E";
    gpib_address = 18;

    def __init__(self):
        self.peak_searched = False;
        
        # device config
        self.center_frequency = 0
        self.span_frequency = 200
        self._set_frequencies()
        self.sweep()

    def _set_frequencies(self):
        cf = self.center_frequency
        sp = self.span_frequency
        self.frequencies = np.linspace( cf-sp/2, cf+sp/2)
        
    def reset_flags(self):
        self.peak_searched = False;

    def reset(self):
        # Simulate reset
        time.sleep(3)

    def set_center_frequency(self, freq):
        # freq: center frequency in MHz
        self.center_frequency = freq
        self._set_frequencies()

    def set_span(self, span):
        # span: span in MHz
        self.span_frequency = span
        self._set_frequencies()
        
    def sweep(self):
        # take one sweep, i.e. fill amplitude array with random values
        peak = self.center_frequency + np.random.uniform(-1,1)*self.span_frequency/2
        nu = self.frequencies
        self.amplitudes = -60 + 20*np.exp( - (nu-peak)**2/(0.1*self.span_frequency)**2)
        self.reset_flags();

    def find_peak(self):
        # Use the build in function of the spectrum analyzer to set the data marker
        # to the frequency with the highest amplitude.
        self.peak_searched = True;
        

    def get_peak_amplitude(self):
        # Return amplitude of peak in dbm.
        return np.max(self.amplitudes)

    def get_peak_frequency(self):
        return self.frequencies[np.argmax(self.amplitudes)]

    def get_peak(self):
        # Return a list with (frequency [MHz], amplitude [dBm]) of the peak
        rv = [self.get_peak_frequency(), self.get_peak_amplitude()];
        self.pead_searched = False
        return rv

    def get_trace(self):
        # Return the data from the display as numpy array.
        return self.amplitudes
