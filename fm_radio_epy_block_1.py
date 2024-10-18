"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import pmt

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, initial_offset=0, neg_const=-120, const=-30, n_bins=256, samp_rate=2.4e6):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[],
            out_sig=[(np.float32, n_bins)]
        )

        self.const = const
        self.neg_const = neg_const
        self.n_bins = n_bins
        self.samp_rate = samp_rate

        self.bin = 0
        self.result = np.full((self.n_bins), self.neg_const)
        self.update_result(initial_offset)

        self.message_name = 'channel_offset'
        self.message_port_register_in(pmt.intern(self.message_name))
        self.set_msg_handler(pmt.intern(self.message_name), self.handle_msg)

    def handle_msg(self, msg):
        val = 0
        if pmt.is_pair(msg):
            # key = pmt.car(msg)
            value = pmt.cdr(msg)
            if pmt.is_number(value):
                val = pmt.to_double(value)

            # print(key, val)

        self.update_result(val)

    def update_result(self, offset):
        self.result[self.bin] = self.neg_const

        self.bin = int(
            (self.samp_rate / 2 + offset)
            / self.samp_rate
            * self.n_bins
        )

        self.result[self.bin] = self.const

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = self.result
        return len(output_items[0])
