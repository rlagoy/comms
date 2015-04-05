#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Comms Signal TXer
# Generated: Fri Apr  3 08:29:41 2015
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import osmosdr
import sys
import time

from distutils.version import StrictVersion
class SignalTX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Comms Signal TXer")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Comms Signal TXer")
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

        self.settings = Qt.QSettings("GNU Radio", "SignalTX")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20e6
        self.recordBool = recordBool = True
        self.fskDemodBool = fskDemodBool = True
        self.freq = freq = 100e6
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
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "hackrf=0" )
        self.osmosdr_sink_0.set_sample_rate(915e6*4)
        self.osmosdr_sink_0.set_center_freq(915e6, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(0, 0)
        self.osmosdr_sink_0.set_if_gain(0, 0)
        self.osmosdr_sink_0.set_bb_gain(0, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        _fskDemodBool_check_box = Qt.QCheckBox("Don't FSK Demod")
        self._fskDemodBool_choices = {True: True, False: False}
        self._fskDemodBool_choices_inv = dict((v,k) for k,v in self._fskDemodBool_choices.iteritems())
        self._fskDemodBool_callback = lambda i: Qt.QMetaObject.invokeMethod(_fskDemodBool_check_box, "setChecked", Qt.Q_ARG("bool", self._fskDemodBool_choices_inv[i]))
        self._fskDemodBool_callback(self.fskDemodBool)
        _fskDemodBool_check_box.stateChanged.connect(lambda i: self.set_fskDemodBool(self._fskDemodBool_choices[bool(i)]))
        self.top_grid_layout.addWidget(_fskDemodBool_check_box, 6,3, 1,1)
        self._freq_layout = Qt.QHBoxLayout()
        self._freq_layout.addWidget(Qt.QLabel("Frequency"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._freq_counter = qwt_counter_pyslot()
        self._freq_counter.setRange(10e6, 6e9, 0.5e6)
        self._freq_counter.setNumButtons(2)
        self._freq_counter.setMinimumWidth(200)
        self._freq_counter.setValue(self.freq)
        self._freq_layout.addWidget(self._freq_counter)
        self._freq_counter.valueChanged.connect(self.set_freq)
        self.top_grid_layout.addLayout(self._freq_layout, 4,3,1,3)
        _fmDemodBool_check_box = Qt.QCheckBox("Don't FM Demod")
        self._fmDemodBool_choices = {True: True, False: False}
        self._fmDemodBool_choices_inv = dict((v,k) for k,v in self._fmDemodBool_choices.iteritems())
        self._fmDemodBool_callback = lambda i: Qt.QMetaObject.invokeMethod(_fmDemodBool_check_box, "setChecked", Qt.Q_ARG("bool", self._fmDemodBool_choices_inv[i]))
        self._fmDemodBool_callback(self.fmDemodBool)
        _fmDemodBool_check_box.stateChanged.connect(lambda i: self.set_fmDemodBool(self._fmDemodBool_choices[bool(i)]))
        self.top_grid_layout.addWidget(_fmDemodBool_check_box, 6,2,1,1)
        self.analog_sig_source_x_0 = analog.sig_source_c(915e6*4, analog.GR_COS_WAVE, 915e6, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.osmosdr_sink_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SignalTX")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        Qt.QMetaObject.invokeMethod(self._samp_rate_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.samp_rate)))

    def get_recordBool(self):
        return self.recordBool

    def set_recordBool(self, recordBool):
        self.recordBool = recordBool
        self._recordBool_callback(self.recordBool)

    def get_fskDemodBool(self):
        return self.fskDemodBool

    def set_fskDemodBool(self, fskDemodBool):
        self.fskDemodBool = fskDemodBool
        self._fskDemodBool_callback(self.fskDemodBool)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        Qt.QMetaObject.invokeMethod(self._freq_counter, "setValue", Qt.Q_ARG("double", self.freq))

    def get_fmDemodBool(self):
        return self.fmDemodBool

    def set_fmDemodBool(self, fmDemodBool):
        self.fmDemodBool = fmDemodBool
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
    tb = SignalTX()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
