#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
import sip



class tone_transmit(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "tone_transmit")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = int(5e6)
        self.width = width = 0.5e6
        self.tone_mag = tone_mag = 5
        self.noise_mag = noise_mag = 2
        self.generation_rate = generation_rate = samp_rate
        self.gain = gain = 0
        self.frequency_adjust = frequency_adjust = 0
        self.amplitude = amplitude = 1

        ##################################################
        # Blocks
        ##################################################

        self._width_range = qtgui.Range(0, 2e6, 100, 0.5e6, 200)
        self._width_win = qtgui.RangeWidget(self._width_range, self.set_width, "'width'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._width_win)
        self._tone_mag_range = qtgui.Range(0, 5, 0.01, 5, 200)
        self._tone_mag_win = qtgui.RangeWidget(self._tone_mag_range, self.set_tone_mag, "'tone_mag'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tone_mag_win)
        self._noise_mag_range = qtgui.Range(0, 5, 0.01, 2, 200)
        self._noise_mag_win = qtgui.RangeWidget(self._noise_mag_range, self.set_noise_mag, "'noise_mag'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_mag_win)
        self._gain_range = qtgui.Range(0, 10, 1, 0, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self._frequency_adjust_range = qtgui.Range(-1e6, +2e6, 0.1e6, 0, 200)
        self._frequency_adjust_win = qtgui.RangeWidget(self._frequency_adjust_range, self.set_frequency_adjust, "'frequency_adjust'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._frequency_adjust_win)
        self._amplitude_range = qtgui.Range(0, 5, 0.1, 1, 200)
        self._amplitude_win = qtgui.RangeWidget(self._amplitude_range, self.set_amplitude, "'amplitude'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._amplitude_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (866e6 + frequency_adjust), #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                generation_rate,
                (width / 2),
                (width / 15),
                window.WIN_HAMMING,
                6.76))
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32("ip:192.168.2.1" if "ip:192.168.2.1" else iio.get_pluto_uri(), [True, True], samp_rate, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(int(samp_rate))
        self.iio_pluto_sink_0.set_frequency((int(866e6 + frequency_adjust)))
        self.iio_pluto_sink_0.set_samplerate(samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, gain)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(10 ** -(tone_mag- 1) if (5 - tone_mag > 0.1) else 0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(10 ** -(noise_mag - 1) if (5 - noise_mag > 0.1) else 0)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1e3, amplitude, 0, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, amplitude, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tone_transmit")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_generation_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0.set_bandwidth(int(self.samp_rate))
        self.iio_pluto_sink_0.set_samplerate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range((866e6 + self.frequency_adjust), self.samp_rate)

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.generation_rate, (self.width / 2), (self.width / 15), window.WIN_HAMMING, 6.76))

    def get_tone_mag(self):
        return self.tone_mag

    def set_tone_mag(self, tone_mag):
        self.tone_mag = tone_mag
        self.blocks_multiply_const_vxx_1.set_k(10 ** -(self.tone_mag- 1) if (5 - self.tone_mag > 0.1) else 0)

    def get_noise_mag(self):
        return self.noise_mag

    def set_noise_mag(self, noise_mag):
        self.noise_mag = noise_mag
        self.blocks_multiply_const_vxx_0.set_k(10 ** -(self.noise_mag - 1) if (5 - self.noise_mag > 0.1) else 0)

    def get_generation_rate(self):
        return self.generation_rate

    def set_generation_rate(self, generation_rate):
        self.generation_rate = generation_rate
        self.blocks_throttle2_0.set_sample_rate(self.generation_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.generation_rate, (self.width / 2), (self.width / 15), window.WIN_HAMMING, 6.76))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.iio_pluto_sink_0.set_attenuation(0,self.gain)

    def get_frequency_adjust(self):
        return self.frequency_adjust

    def set_frequency_adjust(self, frequency_adjust):
        self.frequency_adjust = frequency_adjust
        self.iio_pluto_sink_0.set_frequency((int(866e6 + self.frequency_adjust)))
        self.qtgui_freq_sink_x_0.set_frequency_range((866e6 + self.frequency_adjust), self.samp_rate)

    def get_amplitude(self):
        return self.amplitude

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude
        self.analog_noise_source_x_0.set_amplitude(self.amplitude)
        self.analog_sig_source_x_0.set_amplitude(self.amplitude)




def main(top_block_cls=tone_transmit, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
