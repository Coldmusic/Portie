#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Portie - FM Radio
# Generated: Fri Apr  1 15:23:30 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import osmosdr
import sys
import time
import sqlite3

class fm_receiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Portie - FM Radio")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Portie - FM Radio")
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

        self.settings = Qt.QSettings("GNU Radio", "fm_receiver")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.stations = stations = 0
        self.samp_rate = samp_rate = 2048000
        self.freq = freq = 105.3
        self.Save = Save = 0
        self.Remove = Remove = 0
        self.connection = sqlite3.connect('stations.db')
        self.user = 0
        self.c = self.connection.cursor()

        ##################################################
        # Blocks
        ##################################################
        self._freq_range = Range(88.0, 108.0, 0.1, 105.3, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "Frequency", "counter_slider", float)
        self.top_layout.addWidget(self._freq_win)

        self._stations_options = (0, 1, 2, )
        self._stations_labels = (str(self._stations_options[0]), str(self._stations_options[1]), str(self._stations_options[2]), )
        self._stations_tool_bar = Qt.QToolBar(self)
        self._stations_tool_bar.addWidget(Qt.QLabel("Stations"+": "))
        self._stations_combo_box = Qt.QComboBox()
        self._stations_tool_bar.addWidget(self._stations_combo_box)

        #for label in self._stations_labels: 
        #    self._stations_combo_box.addItem(label)
        self._stations_combo_box.addItem("Select Station")
        self.c.execute("SELECT station FROM stations where user_id = " + str(self.user) + "")
        stats = self.c.fetchall() 
        for els in stats:
            self._stations_combo_box.addItem(els[0])       

        self._stations_callback = lambda i: Qt.QMetaObject.invokeMethod(self._stations_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._stations_options.index(i)))

        self._stations_callback(self.stations)
        self._stations_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_stations(self._stations_options[i]))
        self.top_layout.addWidget(self._stations_tool_bar)

	#RTL-SDR source
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq * 1e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=500,
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
        	1, samp_rate, 100000, 1000000, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=500000,
        	audio_decimation=1,
        )
        _Save_push_button = Qt.QPushButton("Save")
        self._Save_choices = {'Pressed': 1, 'Released': 0}
        _Save_push_button.pressed.connect(lambda: self.set_Save(self._Save_choices['Pressed']))
        _Save_push_button.released.connect(lambda: self.save_pressed())
        self.top_layout.addWidget(_Save_push_button)

        _Remove_push_button = Qt.QPushButton("Remove")
        self._Remove_choices = {'Pressed': 1, 'Released': 0}
        _Remove_push_button.pressed.connect(lambda: self.set_Remove(self._Remove_choices['Pressed']))
        _Remove_push_button.released.connect(lambda: self.remove_pressed())
        self.top_layout.addWidget(_Remove_push_button)
        
        _Select_push_button = Qt.QPushButton("Select")
        self._Select_choices = {'Pressed':1, 'Released':0}
        _Select_push_button.released.connect(lambda: self.select_pressed())
        self.top_layout.addWidget(_Select_push_button)

        
        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.audio_sink_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fm_receiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_stations(self):
        return self.stations

    def set_stations(self, stations):
        self.stations = stations
        self._stations_callback(self.stations)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100000, 1000000, firdes.WIN_HAMMING, 6.76))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.rtlsdr_source_0.set_center_freq(self.freq * 1e6, 0)

    def get_Save(self):
        return self.Save

    def set_Save(self, Save):
        self.Save = Save
  
    def save_pressed(self):
        print(self.freq)
        self._stations_combo_box.addItem(str(self.freq))
        self.c.execute("INSERT INTO stations VALUES("+ str(self.user) + ",'"+ str(self.freq) + "')")
        self.connection.commit()

    def remove_pressed(self):
        ind = self._stations_combo_box.currentIndex()
        txt = self._stations_combo_box.currentText()
        self._stations_combo_box.removeItem(ind)
        if(txt != "Select Station"):
            self.c.execute("DELETE FROM stations where station = '" + str(txt) +"'")
            self.connection.commit()

    def select_pressed(self):
        print("Select pressed")
        txt = self._stations_combo_box.currentText()
        if(txt != "Select Station"):
            self.set_freq(float(txt))
            #self._freq_win.Counter.setValue(float(txt))

    def get_Remove(self):
        return self.Remove

    def set_Remove(self, Remove):
        self.Remove = Remove


def main(top_block_cls=fm_receiver, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
