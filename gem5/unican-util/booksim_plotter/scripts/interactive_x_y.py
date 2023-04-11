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
    ax.plot(br.read_time(), br.read_overall_stat("avg_plat"), label = "ASD")

    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1),
              ncol=2, borderaxespad=0)
    fig.subplots_adjust(right=0.55)
    fig.suptitle('Right-click to hide all\nMiddle-click to show all',
                 va='top', size='large')

    interactive_legend().show()

def interactive_legend(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.legend_)

class InteractiveLegend(object):
    def __init__(self, legend):
        self.legend = legend
        self.fig = legend.axes.figure

        self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
        self._setup_connections()

        self.update()

    def _setup_connections(self):
        for artist in self.legend.texts + self.legend.legendHandles:
            artist.set_picker(10) # 10 points tolerance

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def _build_lookups(self, legend):
        labels = [t.get_text() for t in legend.texts]
        handles = legend.legendHandles
        label2handle = dict(zip(labels, handles))
        handle2text = dict(zip(handles, legend.texts))

        lookup_artist = {}
        lookup_handle = {}
        for artist in legend.axes.get_children():
            if artist.get_label() in labels:
                handle = label2handle[artist.get_label()]
                lookup_handle[artist] = handle
                lookup_artist[handle] = artist
                lookup_artist[handle2text[handle]] = artist

        lookup_handle.update(zip(handles, handles))
        lookup_handle.update(zip(legend.texts, handles))

        return lookup_artist, lookup_handle

    def on_pick(self, event):
        handle = event.artist
        if handle in self.lookup_artist:
            artist = self.lookup_artist[handle]
            artist.set_visible(not artist.get_visible())
            self.update()

    def on_click(self, event):
        if event.button == 3:
            visible = False
        elif event.button == 2:
            visible = True
        else:
            return

        for artist in self.lookup_artist.values():
            artist.set_visible(visible)
        self.update()

    def update(self):
        for artist in self.lookup_artist.values():
            handle = self.lookup_handle[artist]
            if artist.get_visible():
                handle.set_visible(True)
            else:
                handle.set_visible(False)
        self.fig.canvas.draw()

    def show(self):
        plt.show()

class BookSimReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.datatable = self.create_datatable(filename)
        self.initial_time = self.datatable.time[0]

    def create_datatable(self, filename):
        dt = pd.read_csv(filename, sep=',')
        return dt

    def read_time(self):
        return self.datatable.loc[self.datatable['class'] == 0]["time"] -\
                self.initial_time

    def read_stat(self, stat, class_id):
        # if class_id is -1 it returns the sum of the stat for all the classes
        if class_id == -1:
            return self.datatable.groupby('time')[stat].sum()
        else:
            print self.datatable.loc[self.datatable['class'] ==\
                    class_id][stat]
            return self.datatable.loc[self.datatable['class'] ==\
                    class_id][stat]

    def read_overall_stat(self, stat):
        total_sent = self.datatable.groupby('time')["sent_packets"].sum()
        classes = max(self.datatable['class'])

        stat_overall = self.datatable.groupby('time')[stat,"sent_packets"]\
                .apply(ponderation)
        return stat_overall


def ponderation(group):
    stat = group["avg_plat"]
    multiplier = group["sent_packets"]

    return (stat*multiplier).sum() / multiplier.sum()



if __name__ == '__main__':
    main()
