"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, n_bins=256, n_repeats=32, sample_rate=2.4e6):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[(np.complex64, n_bins * n_repeats)],
            out_sig=[(np.float32, n_bins)]
        )
        self.n_bins = n_bins
        self.n_repeats = n_repeats
        self.sample_rate = sample_rate

    def work(self, input_items, output_items):
        s = input_items[0][0]
        #s = s - s.mean()
        s.shape = (self.n_repeats, self.n_bins)
        s *= np.hamming(self.n_bins)
        psd = np.mean(np.abs(np.fft.fft(s)) ** 2, axis=0) /\
            (self.n_bins * self.sample_rate)
        psd_log = 10 * np.log10(psd)
        psd_shifted = np.fft.fftshift(psd_log)

        output_items[0][0] = psd_shifted
        return len(output_items[0])
