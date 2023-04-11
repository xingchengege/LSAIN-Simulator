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

import pandas as pd
import zlib
import sys
from StringIO import StringIO
import subprocess

class CSVHandler():
    def __init__(self, csv_file):
        self.datatable = self.create_datatable(csv_file)

    def create_datatable(self, csv_file):
        print "Reading csv: " + csv_file
        if ".gz" in csv_file:
            p = subprocess.Popen(["zcat", csv_file], stdout = subprocess.PIPE)
            data = StringIO(p.communicate()[0])
            dt = pd.read_csv(data, sep=',', index_col=False)
        elif ".csv" in csv_file:
            dt = pd.read_csv(csv_file, sep=',', index_col=False)
        else:
            print "Extension unknown. Reading file as csv with \",\" as delim"
            dt = pd.read_csv(csv_file, sep=',', index_col=False)
       # Pandas infers compression by default but cannot open compressed
           # files if haven't right crc
       # dt = pd.read_csv(csv_file, sep=',')
        return dt

    # FIXME: These are specific for BookSim.
    # Maybe I should define child classes for each simulation model
    def read_time(self):
        initial_time = self.datatable.time[0]
        return self.datatable.loc[self.datatable['class'] == 0]["time"] \
                                                             - initial_time

    def read_stat(self, stat, class_ponderation = True, message_class = 0):
        if class_ponderation:
            if "_plat" or "_nlat" in stat:
                ponderation_stat = "sent_packets"
            elif "_flat" or "_hops" in stat:
                ponderation_stat = "sent_flits"
            else:
                sys.exit("Unkown poderation stat for stat: " + stat)

            print stat
            group = self.datatable.groupby("time")[stat,ponderation_stat]
            return group.apply(self.ponderation)
        else:
            print message_class
            return self.datatable.loc[self.datatable['class'] == \
                                                    message_class][stat]

    def read_histogram(self, stat, time_start = -1, time_end=-1):
        #TODO: If time_start and time_end are defined, use them
        # to calculate the histogram of that time window
        # If both are -1 we calc the overall histogram
        if time_start == -1 and time_end == -1:
            histogram = []
            for index, row in self.datatable.iterrows():
                hist = row[stat].item()
                if type(hist) is str:
                    hist = hist.replace(" ",",")
                    hist = hist.replace("[,","[")
                    hist = hist.replace(",]","]")
                    # If file cut in the middle of an histogram
                    # ignore this iteration
                    if "]" not in hist:
                        break
                    hist = eval(hist)
                    if len(histogram) == 0:
                        histogram = hist
                    else:
                        histogram = [x+y for x, y in zip(hist, histogram) ]

            # remove trail 0
            final_histogram = []
            last_observation = 1
            for observations in histogram:
                if last_observation == 0 and observations == 0:
                    continue
                else:
                    final_histogram.append(observations)
                    last_observation = observations
            return final_histogram
        else:
            sys.exit("Unsupported histogram time window option")

    ############################################
    ########### Group operations ###############
    ############################################
    def ponderation(self, group):

        for key in group:
            if "sent_" in key:
                multiplier = group[key]
            else:
                stat = group[key]

        if multiplier.sum() > 0:
            return (stat*multiplier).sum() / multiplier.sum()
        else:
            return 0.0
