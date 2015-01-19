#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Comms Signal Viewer
# Generated: Sun Jan 18 22:59:24 2015
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import osmosdr
import sip
import sys
import time

from distutils.version import StrictVersion
class SignalViewer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Comms Signal Viewer")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Comms Signal Viewer")
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

        self.settings = Qt.QSettings("GNU Radio", "SignalViewer")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.recordBool = recordBool = True
        self.fskDemodBool = fskDemodBool = True
        self.freq = freq = 101.7e6
        self.fmDemodBool = fmDemodBool = True

        ##################################################
        # Blocks
        ##################################################
        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel("Sample Rate"+": "))
        self._samp_rate_line_edit = Qt.QLineEdit(str(self.samp_rate))
        self._samp_rate_tool_bar.addWidget(self._samp_rate_line_edit)
        self._samp_rate_line_edit.returnPressed.connect(
        	lambda: self.set_samp_rate(eng_notation.str_to_num(self._samp_rate_line_edit.text().toAscii())))
        self.top_grid_layout.addWidget(self._samp_rate_tool_bar, 4,1,1,2)
        _recordBool_check_box = Qt.QCheckBox("Don't Record IQ")
        self._recordBool_choices = {True: True, False: False}
        self._recordBool_choices_inv = dict((v,k) for k,v in self._recordBool_choices.iteritems())
        self._recordBool_callback = lambda i: Qt.QMetaObject.invokeMethod(_recordBool_check_box, "setChecked", Qt.Q_ARG("bool", self._recordBool_choices_inv[i]))
        self._recordBool_callback(self.recordBool)
        _recordBool_check_box.stateChanged.connect(lambda i: self.set_recordBool(self._recordBool_choices[bool(i)]))
        self.top_grid_layout.addWidget(_recordBool_check_box, 6,4,1,1)
        self.main_tab = Qt.QTabWidget()
        self.main_tab_widget_0 = Qt.QWidget()
        self.main_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_0)
        self.main_tab_grid_layout_0 = Qt.QGridLayout()
        self.main_tab_layout_0.addLayout(self.main_tab_grid_layout_0)
        self.main_tab.addTab(self.main_tab_widget_0, "PSD")
        self.main_tab_widget_1 = Qt.QWidget()
        self.main_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.main_tab_widget_1)
        self.main_tab_grid_layout_1 = Qt.QGridLayout()
        self.main_tab_layout_1.addLayout(self.main_tab_grid_layout_1)
        self.main_tab.addTab(self.main_tab_widget_1, "Waterfall")
        self.top_grid_layout.addWidget(self.main_tab, 1,1,3,5)
        self._freq_layout = Qt.QHBoxLayout()
        self._freq_layout.addWidget(Qt.QLabel("Frequency"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._freq_counter = qwt_counter_pyslot()
        self._freq_counter.setRange(24e6, 1.7e9, 0.5e6)
        self._freq_counter.setNumButtons(2)
        self._freq_counter.setMinimumWidth(200)
        self._freq_counter.setValue(self.freq)
        self._freq_layout.addWidget(self._freq_counter)
        self._freq_counter.valueChanged.connect(self.set_freq)
        self.top_grid_layout.addLayout(self._freq_layout, 4,3,1,3)
        self.volumeBlock = blocks.multiply_const_vff((100, ))
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
          
        self.recordIQ = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(recordBool))
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_rate, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        
        if complex == type(float()):
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [5, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.main_tab_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
                gr.sizeof_char,
                0,
                qtgui.NUM_GRAPH_HORIZ,
        	1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        units = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])
        
        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 7,1,1,5)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        
        if complex == type(float()):
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.main_tab_layout_0.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))
        _fskDemodBool_check_box = Qt.QCheckBox("Don't FSK Demod")
        self._fskDemodBool_choices = {True: True, False: False}
        self._fskDemodBool_choices_inv = dict((v,k) for k,v in self._fskDemodBool_choices.iteritems())
        self._fskDemodBool_callback = lambda i: Qt.QMetaObject.invokeMethod(_fskDemodBool_check_box, "setChecked", Qt.Q_ARG("bool", self._fskDemodBool_choices_inv[i]))
        self._fskDemodBool_callback(self.fskDemodBool)
        _fskDemodBool_check_box.stateChanged.connect(lambda i: self.set_fskDemodBool(self._fskDemodBool_choices[bool(i)]))
        self.top_grid_layout.addWidget(_fskDemodBool_check_box, 6,3, 1,1)
        self.fskDemod = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(fskDemodBool))
        self.fskData = blocks.file_sink(gr.sizeof_char*1, "/Users/ryanlagoy/Documents/Repositories/comms/GNURadio_SDR/fskData.bin", False)
        self.fskData.set_unbuffered(True)
        _fmDemodBool_check_box = Qt.QCheckBox("Don't FM Demod")
        self._fmDemodBool_choices = {True: True, False: False}
        self._fmDemodBool_choices_inv = dict((v,k) for k,v in self._fmDemodBool_choices.iteritems())
        self._fmDemodBool_callback = lambda i: Qt.QMetaObject.invokeMethod(_fmDemodBool_check_box, "setChecked", Qt.Q_ARG("bool", self._fmDemodBool_choices_inv[i]))
        self._fmDemodBool_callback(self.fmDemodBool)
        _fmDemodBool_check_box.stateChanged.connect(lambda i: self.set_fmDemodBool(self._fmDemodBool_choices[bool(i)]))
        self.top_grid_layout.addWidget(_fmDemodBool_check_box, 6,2,1,1)
        self.fmDemod = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(fmDemodBool))
        self.digital_gfsk_demod_0 = digital.gfsk_demod(
        	samples_per_symbol=2,
        	sensitivity=1.0,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=500e3,
        	audio_decimation=10,
        )
        self.IQData = blocks.file_sink(gr.sizeof_gr_complex*1, "/Users/ryanlagoy/Documents/Repositories/comms/GNURadio_SDR/IQData.bin", False)
        self.IQData.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0_0_0, 0))    
        self.connect((self.digital_gfsk_demod_0, 0), (self.fskData, 0))    
        self.connect((self.digital_gfsk_demod_0, 0), (self.qtgui_number_sink_0, 0))    
        self.connect((self.fmDemod, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.fskDemod, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.digital_gfsk_demod_0, 0))    
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.volumeBlock, 0))    
        self.connect((self.recordIQ, 0), (self.IQData, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.fmDemod, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.fskDemod, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.recordIQ, 0))    
        self.connect((self.volumeBlock, 0), (self.audio_sink_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SignalViewer")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        Qt.QMetaObject.invokeMethod(self._samp_rate_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.samp_rate)))

    def get_recordBool(self):
        return self.recordBool

    def set_recordBool(self, recordBool):
        self.recordBool = recordBool
        self.recordIQ.set_open(bool(self.recordBool))
        self._recordBool_callback(self.recordBool)

    def get_fskDemodBool(self):
        return self.fskDemodBool

    def set_fskDemodBool(self, fskDemodBool):
        self.fskDemodBool = fskDemodBool
        self.fskDemod.set_open(bool(self.fskDemodBool))
        self._fskDemodBool_callback(self.fskDemodBool)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)
        Qt.QMetaObject.invokeMethod(self._freq_counter, "setValue", Qt.Q_ARG("double", self.freq))

    def get_fmDemodBool(self):
        return self.fmDemodBool

    def set_fmDemodBool(self, fmDemodBool):
        self.fmDemodBool = fmDemodBool
        self.fmDemod.set_open(bool(self.fmDemodBool))
        self._fmDemodBool_callback(self.fmDemodBool)

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
    tb = SignalViewer()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
