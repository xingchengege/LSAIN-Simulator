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

import matplotlib.pyplot as plt
from csv_handler import CSVHandler
import numpy as np

class Chart():
    def __init__(self, name, output_dir, title = ""):
        self.name = name
        self.output_dir = output_dir
        self.fullname = output_dir + "/" + name + ".pdf"
        self.title = title

# FIXME: Perharps I should change the name of this class to TimeYLine(Chart)
class XYLine(Chart):
    def __init__(self, name, output_dir, plot_params):
        if "title" in plot_params:
            Chart.__init__(self, name, output_dir, plot_params["title"])
        else:
            Chart.__init__(self, name, output_dir, name)

        self.params = plot_params

        self.xlabel = plot_params["xlabel"]
        self.ylabel = plot_params["ylabel"]
        self.user_limits = False
        if "user_limits" in plot_params:
            if plot_params["user_limits"] == "true" or\
                    plot_params["user_limits"] == "True" or\
                    plot_params["user_limits"] == "TRUE":
                self.user_limits = True
                self.xlimits = plot_params["xlimits"]
                self.ylimits = plot_params["ylimits"]

        if "legend" in plot_params:
            self.legend = plot_params["legend"]
        else:
            self.legend = plot_params["simulation_dir"]

        self.simulation_reader(plot_params["simulation_dir"])

        self.create_figure()

    def simulation_reader(self, simulation_list):
        self.time_list = []
        self.y_list = []

        for sim_index, simulation in enumerate(simulation_list):
            csv_h = CSVHandler(simulation)

            # X-axis is allways time
            self.time_list.append(csv_h.read_time())
            self.y_list.append(
                    csv_h.read_stat(self.params["yaxis"][sim_index]))


    def create_figure(self):
        fig, ax = plt.subplots(figsize=(20,10))

        for i, x in enumerate(self.time_list):
            ax.plot(x, self.y_list[i], label = self.legend[i])

        fig.suptitle(self.title)
        ax.legend(loc=0)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.grid('on')
        if self.user_limits:
            ax.set_ylim(ymin = long(self.ylimits[0]),
                    ymax = long(self.ylimits[1]))
            ax.set_xlim(xmin = long(self.xlimits[0]),
                    xmax = long(self.xlimits[1]))
        fig.savefig(self.fullname)

# FIXME: Perharps I should change the name of this class to TimeYLine(Chart)
class XYLineMultiClass(Chart):
    def __init__(self, name, output_dir, plot_params):
        if "title" in plot_params:
            Chart.__init__(self, name, output_dir, plot_params["title"])
        else:
            Chart.__init__(self, name, output_dir, name)

        self.params = plot_params

        self.xlabel = plot_params["xlabel"]
        self.ylabel = plot_params["ylabel"]
        self.user_limits = False
        if "user_limits" in plot_params:
            if plot_params["user_limits"] == "true" or\
                    plot_params["user_limits"] == "True" or\
                    plot_params["user_limits"] == "TRUE":
                self.user_limits = True
                self.xlimits = plot_params["xlimits"]
                self.ylimits = plot_params["ylimits"]

        if "legend" in plot_params:
            self.legend = plot_params["legend"]
        else:
            self.legend = plot_params["simulation_dir"]

        self.simulation_reader(plot_params["simulation_dir"])

        self.create_figure()

    def simulation_reader(self, simulation_list):
        self.time_list = []
        self.y_list = []

        for simulation in simulation_list:
            csv_h = CSVHandler(simulation)

            # X-axis is allways time
            self.time_list.append(csv_h.read_time())
            for c in range(int(self.params["classes"])):
                self.y_list.append(csv_h.read_stat(self.params["yaxis"],
                    False, c))


    def create_figure(self):
        fig, ax = plt.subplots(figsize=(20,10))

        for i, x in enumerate(self.time_list):
            for c in range(int(self.params["classes"])):
                if len(x) != len(self.y_list[i+c]):
                    print x
                    print x[:-1]
                    print self.y_list[i+c]
                    print "LENGTH: ", len(self.y_list[i+c])
                    if len(self.y_list[i+c]) != 0:
                        ax.plot(x[:-1], self.y_list[i+c], label =\
                                self.legend[i] + " class: " + str(c))
                else:
                    ax.plot(x, self.y_list[i+c],
                            label = self.legend[i] + " class: " + str(c))


        fig.suptitle(self.title)
        ax.legend(loc=0)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.grid('on')
        if self.user_limits:
            ax.set_ylim(ymin = long(self.ylimits[0]),
                        ymax = long(self.ylimits[1]))
            ax.set_xlim(xmin = long(self.xlimits[0]),
                        xmax = long(self.xlimits[1]))
        fig.savefig(self.fullname)

class XYMultiLine(Chart):
    def __init__(self, name, output_dir, plot_params):
        if "title" in plot_params:
            Chart.__init__(self, name, output_dir, plot_params["title"])
        else:
            Chart.__init__(self, name, output_dir, name)

        self.params = plot_params

        self.xlabel = plot_params["xlabel"]
        self.ylabel = plot_params["ylabel"]
        self.user_limits = False
        if "user_limits" in plot_params:
            if plot_params["user_limits"] == "true" or\
                    plot_params["user_limits"] == "True" or\
                    plot_params["user_limits"] == "TRUE":
                self.user_limits = True
                self.xlimits = plot_params["xlimits"]
                self.ylimits = plot_params["ylimits"]

        if "legend" in plot_params:
            self.legend = plot_params["legend"]
        else:
            self.legend = plot_params["simulation_dir"]

        self.simulation_reader(plot_params["simulation_dir"])

        self.create_figure()

    def simulation_reader(self, simulation_list):
        self.time_list = []
        self.y_list = []

        for simulation in simulation_list:
            csv_h = CSVHandler(simulation)

            # X-axis is allways time
            self.time_list.append(csv_h.read_time())
            y_stat = []
            for stat in self.params["yaxis"]:
                y_stat.append(csv_h.read_stat(stat))
            self.y_list.append(y_stat)


    def create_figure(self):
        fig, ax = plt.subplots(figsize=(20,10))

        for i, x in enumerate(self.time_list):
            for j, y in enumerate(self.y_list[i]):
                if "yfactor" in self.params:
                    y = eval(self.params["yfactor"][j])
                ax.plot(x, y, label = self.legend[j])

        fig.suptitle(self.title)
        ax.legend(loc=0)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.grid('on')
        if self.user_limits:
            print self.ylimits
            ax.set_ylim(ymin = float(self.ylimits[0]),
                        ymax = float(self.ylimits[1]))
            ax.set_xlim(xmin = float(self.xlimits[0]),
                        xmax = float(self.xlimits[1]))
        fig.savefig(self.fullname)

class HistogramBar(Chart):
    def __init__(self, name, output_dir, plot_params):
        if "title" in plot_params:
            Chart.__init__(self, name, output_dir, plot_params["title"])
        else:
            Chart.__init__(self, name, output_dir, name)

        self.params = plot_params

        self.xlabel = plot_params["xlabel"]
        self.ylabel = "Observations"
        self.user_limits = False
        if "user_limits" in plot_params:
            if plot_params["user_limits"] == "true" or\
                    plot_params["user_limits"] == "True" or\
                    plot_params["user_limits"] == "TRUE":
                self.user_limits = True
                self.xlimits = plot_params["xlimits"]

        if "legend" in plot_params:
            self.legend = plot_params["legend"]
        else:
            self.legend = plot_params["simulation_dir"]

        self.simulation_reader(plot_params["simulation_dir"])

        self.create_figure()

    def simulation_reader(self, simulation_list):
        self.y_list = []

        for simulation in simulation_list:
            csv_h = CSVHandler(simulation)
            self.y_list.append(csv_h.read_histogram(self.params["yaxis"]))


    def create_figure(self):
        fig, ax = plt.subplots(figsize=(20,10))

        for y in self.y_list:
            x = np.arange(len(y))
            if "xfactor" in self.params:
                x = eval(self.params["xfactor"][0])
            ax.bar(x, y)

        fig.suptitle(self.title)
        ax.legend(loc=0)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.grid('on')
        if self.user_limits:
            ax.set_ylim(ymin = self.ylimits[0], ymax = self.ylimits[1])
            ax.set_xlim(xmin = self.xlimits[0], xmax = self.xlimits[1])
        fig.savefig(self.fullname)

# FIXME: Perharps I should change the name of this class to TimeYLine(Chart)
class XYLineMultiLineMultisim(Chart):
    def __init__(self, name, output_dir, plot_params):
        if "title" in plot_params:
            Chart.__init__(self, name, output_dir, plot_params["title"])
        else:
            Chart.__init__(self, name, output_dir, name)

        self.params = plot_params

        self.xlabel = plot_params["xlabel"]
        self.ylabel = plot_params["ylabel"]
        self.user_limits = False
        if "user_limits" in plot_params:
            if plot_params["user_limits"] == "true" or\
                    plot_params["user_limits"] == "True" or\
                    plot_params["user_limits"] == "TRUE":
                self.user_limits = True
                self.xlimits = plot_params["xlimits"]
                self.ylimits = plot_params["ylimits"]

        if "legend" in plot_params:
            self.legend = plot_params["legend"]
        else:
            self.legend = plot_params["simulation_dir"]

        self.simulation_reader(plot_params["simulation_dir"])

        self.create_figure()

    def simulation_reader(self, simulation_list):
        self.time_list = []
        self.y_list = []

        for sim_index, simulation in enumerate(simulation_list):
            csv_h = CSVHandler(simulation)

            # X-axis is allways time
            self.time_list.append(csv_h.read_time())
            for stat in self.params["yaxis"][sim_index]:
                if stat == "sent_flits":
                    self.y_list.append(csv_h.read_stat(stat, False))
                else:
                    self.y_list.append(csv_h.read_stat(stat, True))


    def create_figure(self):
        fig, ax = plt.subplots(figsize=(20,10))

#        print self.time_list
        print len(self.y_list)
        for i, x in enumerate(self.time_list):
            if len(x) != len(self.y_list[i]):
                y = self.y_list[i]
                if "yfactor" in self.params:
                    y = eval(self.params["yfactor"][i])
                if len(self.y_list[i]) != 0:
                    ax.plot(x[:-1], y, label = self.legend[i])
            else:
                ax.plot(x, self.y_list[i], label = self.legend[i])


        fig.suptitle(self.title)
        ax.legend(loc=0)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.grid('on')
        if self.user_limits:
            ax.set_ylim(ymin = long(self.ylimits[0]),
                    ymax = long(self.ylimits[1]))
            ax.set_xlim(xmin = long(self.xlimits[0]),
                    xmax = long(self.xlimits[1]))
        fig.savefig(self.fullname)
