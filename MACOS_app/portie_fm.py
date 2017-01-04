#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Portie - FM Radio
# Generated: Mon Apr  4 08:43:22 2016
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import math
import osmosdr
import sys
import time
import sqlite3

class portie_fm(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "portie_fm")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2400000
        self.bb_decim = bb_decim = 4
        self.freq_offset = freq_offset = 250000
        self.freq = freq = 105.3
        self.baseband_rate = baseband_rate = samp_rate/bb_decim
        self.audio_decim = audio_decim = 5
        self.xlate_bandwidth = xlate_bandwidth = 100000
        self.volume = volume = 0
        self.stations = stations = 0
        self.select = select = 0
        self.save = save = 0
        self.remove = remove = 0
        self.freq_tune = freq_tune = freq*1000000- freq_offset
        self.audio_rate = audio_rate = 48000
        self.audio_decim_rate = audio_decim_rate = baseband_rate/audio_decim
        self.connection = sqlite3.connect('stations.db')
        self.user = 0
        self.c = self.connection.cursor()
        self.s = 0
        self.r = 0

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(-20, 10, 1, 0, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, "Volume", "counter_slider", float)
        self.top_layout.addWidget(self._volume_win)

        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes.low_pass(1, samp_rate, xlate_bandwidth, 100000)), freq_offset, samp_rate)
        self._freq_range = Range(88.1, 107.9, 0.1, 105.3, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "Frequency", "counter_slider", float)
        self.top_layout.addWidget(self._freq_win)

        self._stations_options = (0, 1, 2, )
        self._stations_labels = (str(self._stations_options[0]), str(self._stations_options[1]), str(self._stations_options[2]), )
        self._stations_tool_bar = Qt.QToolBar(self)
        self._stations_tool_bar.addWidget(Qt.QLabel("Stations"+": "))
        self._stations_combo_box = Qt.QComboBox()
        self._stations_tool_bar.addWidget(self._stations_combo_box)
        
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

        _select_push_button = Qt.QPushButton("Select")
        self._select_choices = {'Pressed': 1, 'Released': 0}
        _select_push_button.pressed.connect(lambda: self.set_select(self._select_choices['Pressed']))
        _select_push_button.released.connect(lambda: self.select_pressed())
        self.top_layout.addWidget(_select_push_button)

        _save_push_button = Qt.QPushButton("Save")
        self._save_choices = {'Pressed': 1, 'Released': 0}
        _save_push_button.pressed.connect(lambda: self.set_save(self._save_choices['Pressed']))
        _save_push_button.released.connect(lambda: self.save_pressed())
        self.top_layout.addWidget(_save_push_button)

        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq_tune, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(1, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(20, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        _remove_push_button = Qt.QPushButton("Remove")
        self._remove_choices = {'Pressed': 1, 'Released': 0}
        _remove_push_button.pressed.connect(lambda: self.set_remove(self._remove_choices['Pressed']))
        _remove_push_button.released.connect(lambda: self.remove_pressed())
        self.top_layout.addWidget(_remove_push_button)

        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=audio_rate,
                decimation=audio_decim_rate,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=audio_rate,
                decimation=audio_decim_rate,
                taps=None,
                fractional_bw=None,
        )

        self.fir_filter_xxx_5 = filter.fir_filter_fff(audio_decim, (firdes.low_pass(1.0,baseband_rate,20e3,40e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_5.declare_sample_delay(0)
        self.fir_filter_xxx_3 = filter.fir_filter_fff(1, (firdes.band_pass(1.0,baseband_rate,38e3-13e3,38e3+13e3,3e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_3.declare_sample_delay(0)
        self.fir_filter_xxx_2 = filter.fir_filter_fcc(1, (firdes.complex_band_pass(1.0,baseband_rate,19e3-500,19e3+500,1e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_2.declare_sample_delay(0)
        self.fir_filter_xxx_1 = filter.fir_filter_fff(audio_decim, (firdes.low_pass(1.0,baseband_rate,13e3,3e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_1.declare_sample_delay(0)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((10**(1.*(volume+15)/10), ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((10**(1.*(volume+15)/10), ))
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0 = audio.sink(audio_rate, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=bb_decim,
        )
        self.analog_pll_refout_cc_0 = analog.pll_refout_cc(0.001, 2 * math.pi * (19000+200) / baseband_rate, 2 * math.pi * (19000-200) / baseband_rate)
        self.analog_fm_deemph_0_0_0 = analog.fm_deemph(fs=audio_decim_rate, tau=75e-6)
        self.analog_fm_deemph_0_0 = analog.fm_deemph(fs=audio_decim_rate, tau=75e-6)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_deemph_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.analog_fm_deemph_0_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_1, 0))    
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_1, 1))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.fir_filter_xxx_1, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.fir_filter_xxx_2, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.fir_filter_xxx_3, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.analog_fm_deemph_0_0_0, 0))    
        self.connect((self.blocks_complex_to_imag_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.fir_filter_xxx_5, 0))    
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_imag_0, 0))    
        self.connect((self.blocks_sub_xx_0, 0), (self.analog_fm_deemph_0_0, 0))    
        self.connect((self.fir_filter_xxx_1, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.fir_filter_xxx_1, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.fir_filter_xxx_2, 0), (self.analog_pll_refout_cc_0, 0))    
        self.connect((self.fir_filter_xxx_3, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.fir_filter_xxx_5, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.fir_filter_xxx_5, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.audio_sink_0, 1))    
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "portie_fm")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_baseband_rate(self.samp_rate/self.bb_decim)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.xlate_bandwidth, 100000)))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_bb_decim(self):
        return self.bb_decim

    def set_bb_decim(self, bb_decim):
        self.bb_decim = bb_decim
        self.set_baseband_rate(self.samp_rate/self.bb_decim)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.set_freq_tune(self.freq*1000000- self.freq_offset)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freq_offset)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_tune(self.freq*1000000- self.freq_offset)

    def get_baseband_rate(self):
        return self.baseband_rate

    def set_baseband_rate(self, baseband_rate):
        self.baseband_rate = baseband_rate
        self.set_audio_decim_rate(self.baseband_rate/self.audio_decim)
        self.analog_pll_refout_cc_0.set_max_freq(2 * math.pi * (19000+200) / self.baseband_rate)
        self.analog_pll_refout_cc_0.set_min_freq(2 * math.pi * (19000-200) / self.baseband_rate)
        self.fir_filter_xxx_1.set_taps((firdes.low_pass(1.0,self.baseband_rate,13e3,3e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_2.set_taps((firdes.complex_band_pass(1.0,self.baseband_rate,19e3-500,19e3+500,1e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_3.set_taps((firdes.band_pass(1.0,self.baseband_rate,38e3-13e3,38e3+13e3,3e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_5.set_taps((firdes.low_pass(1.0,self.baseband_rate,20e3,40e3,firdes.WIN_HAMMING)))

    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        self.audio_decim = audio_decim
        self.set_audio_decim_rate(self.baseband_rate/self.audio_decim)

    def get_xlate_bandwidth(self):
        return self.xlate_bandwidth

    def set_xlate_bandwidth(self, xlate_bandwidth):
        self.xlate_bandwidth = xlate_bandwidth
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.xlate_bandwidth, 100000)))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k((10**(1.*(self.volume+15)/10), ))
        self.blocks_multiply_const_vxx_0_0.set_k((10**(1.*(self.volume+15)/10), ))

    def get_stations(self):
        return self.stations

    def set_stations(self, stations):
        self.stations = stations
        self._stations_callback(self.stations)

    def get_select(self):
        return self.select

    def set_select(self, select):
        self.select = select

    def get_save(self):
        return self.save

    def set_save(self, save):
        self.save = save

    def get_remove(self):
        return self.remove

    def set_remove(self, remove):
        self.remove = remove

    def get_freq_tune(self):
        return self.freq_tune

    def set_freq_tune(self, freq_tune):
        self.freq_tune = freq_tune
        self.rtlsdr_source_0.set_center_freq(self.freq_tune, 0)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate

    def get_audio_decim_rate(self):
        return self.audio_decim_rate

    def set_audio_decim_rate(self, audio_decim_rate):
        self.audio_decim_rate = audio_decim_rate

    def save_pressed(self):
        try:
            self.c.execute("INSERT INTO stations VALUES("+ str(self.user) + ",'"+ str(self.freq) + "')")
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("\nStation is already saved.")
        else:
            self._stations_combo_box.addItem(str(self.freq))

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


def main(top_block_cls=portie_fm, options=None):

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
