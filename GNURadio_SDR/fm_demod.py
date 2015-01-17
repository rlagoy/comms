#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Fm Demod
# Generated: Sat Jan 17 16:28:59 2015
##################################################

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import sys
import time

from distutils.version import StrictVersion
class fm_demod(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Fm Demod")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fm Demod")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fm_demod")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 5
        self.samp_rate = samp_rate = 2e6
        self.freq = freq = 101.7e6

        ##################################################
        # Blocks
        ##################################################
        self._volume_tool_bar = Qt.QToolBar(self)
        self._volume_tool_bar.addWidget(Qt.QLabel("volume"+": "))
        self._volume_line_edit = Qt.QLineEdit(str(self.volume))
        self._volume_tool_bar.addWidget(self._volume_line_edit)
        self._volume_line_edit.returnPressed.connect(
        	lambda: self.set_volume(int(self._volume_line_edit.text().toAscii())))
        self.top_layout.addWidget(self._volume_tool_bar)
        self.volumeBlock = blocks.multiply_const_vff((volume, ))
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_clock_source("external", 0)
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=500e3,
        	audio_decimation=10,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.volumeBlock, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.volumeBlock, 0), (self.audio_sink_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fm_demod")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        Qt.QMetaObject.invokeMethod(self._volume_line_edit, "setText", Qt.Q_ARG("QString", str(self.volume)))
        self.volumeBlock.set_k((self.volume, ))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = fm_demod()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
