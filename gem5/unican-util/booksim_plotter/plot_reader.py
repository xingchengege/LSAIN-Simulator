//
//  Copyright (c) 2015-2020 University of Cantabria
//  All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met: redistributions of source code must retain the above copyright
//  notice, this list of conditions and the following disclaimer;
//  redistributions in binary form must reproduce the above copyright
//  notice, this list of conditions and the following disclaimer in the
//  documentation and/or other materials provided with the distribution;
//  neither the name of the copyright holders nor the names of its
//  contributors may be used to endorse or promote products derived from
//  this software without specific prior written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
//  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
//  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
//  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
//  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
//  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
//  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
//  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
//  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
//  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
//  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//  Authors: Ivan Perez
//

import json
import sys
import pandas as pd
from csv_handler import CSVHandler
import matplotlib.pyplot as plt
from chart import XYLine, XYLineMultiClass, XYMultiLine, HistogramBar,\
        XYLineMultiLineMultisim

class ReaderFactory():
    def get_readers(self,experiment_json):
        with open(experiment_json,'r') as f:
            plot_data = json.load(f)

            readers = []

            for plot in plot_data:
                plot_params = plot_data[plot]
                reader_type = plot_params["reader_type"]
                if reader_type == "booksim":
                    readers.append(BooksimReader(plot, plot_params))
                elif reader_type == "garnet":
                    readers.append(GarnetReader(plot, plot_params))
                elif reader_type == "gem5":
                    readers.append(Gem5Reader(plot, plot_params))
                else:
                    sys.exit("reader_type: " + reader_type + " unknown")

            return readers

class Reader():
    def __init__(self, name, params):
        self.name   = name
        self.params = params


class BooksimReader(Reader):
    def __init__(self, name, params):
        Reader.__init__(self, name, params)
        #TODO: add wildcards to improve usage
        self.simulation_dir = self.params["simulation_dir"]

        self.chart_type = self.params["chart_type"]

    def create_plot(self, output_dir):

        if self.chart_type == "xyline":
            XYLine(self.name, output_dir, self.params)
        elif self.chart_type == "xylinemulticlass":
            XYLineMultiClass(self.name, output_dir, self.params)
        elif self.chart_type == "xymultiline":
            XYMultiLine(self.name, output_dir, self.params)
        elif self.chart_type == "histogrambar":
            HistogramBar(self.name, output_dir, self.params)
        elif self.chart_type == "xymultiline_multisim":
            XYLineMultiLineMultisim(self.name, output_dir, self.params)
