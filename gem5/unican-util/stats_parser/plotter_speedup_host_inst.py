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

"""
========
Barchart
========
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import json
import sys

def format_label(label):
    if "r\'" in label or "r\"" in label:
        return eval(label)
    else:
        return label

def CreateColormap(data):
    colormap = 'viridis'
    ## FIXME: Is there a way to simplify the following two lines?
    if 'colormap' in data:
        colormap = data['colormap']

    cmap = plt.get_cmap(colormap)
    total_colors = len(cmap.colors)
    # Find latest colormap index
    no_colors = 1
    for color in data['colors']:
        if 'colormap' in color:
            color_index = int(color.replace('colormap[','').replace(']',''))
            no_colors = color_index+1 if color_index+1 > no_colors \
                    else no_colors
    color_offset = int(total_colors/(no_colors))
    return list(reversed(cmap.colors))[0:-1:color_offset]

df = pd.read_csv(sys.argv[1])
print df

json_file = open(sys.argv[2],'r')
data_json = json.load(json_file)
json_file.close()

simulations = df.sim_name.unique()
total_width = 0.8
width = total_width/len(simulations)       # the width of the bars

benchmarks = df.benchmark.unique()
ind = np.arange(len(benchmarks)+1)  # the x locations for the groups

if "figsize" in data_json:
    figsize = eval(data_json["figsize"])
else:
    figsize = (8,6)

fig, ax = plt.subplots(figsize=figsize)

colormap = CreateColormap(data_json)

for sim_ind, simulation in enumerate(simulations):
        values_list = []
        for benchmark in benchmarks:
            table = df[df.sim_name==simulation]
            table = table[df.benchmark == benchmark]
            #value = table.total_packets.tolist()
            #value = table.host_seconds.tolist()
            #value = table.sim_seconds.tolist()
            value = table[data_json['stat']].tolist()
            if len(value) == 0:
                values_list.append(0)
            elif len(value) == 1:
                values_list.append(value[0])
            else:
                print "ERRRROOOOOOORRRRR"
        values_list.append(sum(values_list)/len(values_list))
        values_list = [value/100000.0 for value in values_list]
        rects = ax.bar(ind+sim_ind*width,values_list, width,
                    label=data_json['series-label'][sim_ind],
                    color=eval(data_json['colors'][sim_ind]),
                    edgecolor='black', linewidth=0.3)
        print "{} : {}".format(data_json['series-label'][sim_ind],
                values_list)
#
#rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)
#
# add some text for labels, title and axes ticks
ax.set_ylabel(r'Simulated ticks/s ($x10^5$)')
ax.set_xlabel(format_label(data_json["x-label"]))
ax.legend()
#ax.grid()
benchmarks = np.append(benchmarks,"Avg")
plt.xticks([x-width/2 + len(simulations)/2*width for x in ind],
        benchmarks,rotation='vertical')

if "title" in data_json:
    ax.set_title(data_json["title"])

ax.grid(b=True, which='major', axis='y', color='gray',
        linewidth=0.05, linestyle="-")

# FIXME: Check if output path exists
#	 Current implementation only supports linux filesystems
output_dir = ""

if "output" not in data_json:
    data_json["output"] = sys.argv[1].replace(".csv",
            data_json["stat"]+".pdf")

for x in data_json["output"].split("/")[0:-1]:
    output_dir += x + "/"
print('output_dir: ', output_dir)

if output_dir != "":
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

if "disable_legend" in data_json:
    if data_json["disable_legend"] == "1":
        ax.legend().remove()

box = ax.get_position()
#self.ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#self.ax.legend(loc='center left', bbox_to_anchor=(1,0.5))

fig.savefig(data_json["output"], bbox_inches='tight')
