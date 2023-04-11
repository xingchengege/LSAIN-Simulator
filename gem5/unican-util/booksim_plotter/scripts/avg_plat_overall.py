#
#  Copyright (c) 2015-2020 University of Cantabria
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met: redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer;
#  redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution;
#  neither the name of the copyright holders nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  Authors: Ivan Perez
#

#import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

def main():
#    x = np.arange(10)
    fig, ax = plt.subplots()


    #for i in range(1, 31):
    #    ax.plot(x, i * x, label=r'$y={}x$'.format(i))

    br = BookSimReader(sys.argv[1])
    br.read_time()
    ax.plot(br.read_time(), br.read_plat_ponderated(), label = "plat")
    ax.plot(br.read_time(), br.read_nlat_ponderated(), label = "nlat")

    ax.legend(loc='upper left', bbox_to_anchor=(0.8, 1),
              ncol=1, borderaxespad=0)
    fig.suptitle(sys.argv[1].split(".csv")[0],
                 va='top', size='large')
#    plt.show()
    fig.savefig(sys.argv[1].split(".csv")[0] + ".pdf")


class BookSimReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.datatable = self.create_datatable(filename)
        self.initial_time = self.datatable.time[0]

    def create_datatable(self, filename):
        dt = pd.read_csv(filename, sep=',')
        return dt

    def read_time(self):
        return self.datatable.loc[self.datatable['class'] == 0]["time"] \
                - self.initial_time

    def read_stat(self, stat, class_id):
        # if class_id is -1 it returns the sum of the stat for all the classes
        if class_id == -1:
            return self.datatable.groupby('time')[stat].sum()
        else:
            print self.datatable.loc[self.datatable['class'] ==\
                    class_id][stat]
            return self.datatable.loc[self.datatable['class'] ==\
                    class_id][stat]

    def read_plat_ponderated(self):
        group = self.datatable.groupby("time")["avg_plat","sent_packets"]
        return group.apply(plat_ponderated)

    def read_nlat_ponderated(self):
        group = self.datatable.groupby("time")["avg_nlat","sent_packets"]
        return group.apply(nlat_ponderated)


def plat_ponderated(group):
    stat = group["avg_plat"]
    multiplier = group["sent_packets"]

    return (stat*multiplier).sum() / multiplier.sum()

def nlat_ponderated(group):
    stat = group["avg_nlat"]
    multiplier = group["sent_packets"]

    return (stat*multiplier).sum() / multiplier.sum()



if __name__ == '__main__':
    main()
