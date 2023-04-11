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
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])

simulations = df.sim_name.unique()
width = 0.6

colours=['red','blue','yellow','green','violet']

benchmarks = df.benchmark.unique()
ind = np.arange(len(simulations))  # the x locations for the groups

fig, ax = plt.subplots()
values_list = []
for sim_ind, simulation in enumerate(simulations):
    table = df[df.sim_name==simulation]
    value = table.speedup.tolist()
    values_list.append(value[0])

print ind
print values_list
rects = ax.bar(ind,values_list, width, color=colours)
#
#rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)
#
# add some text for labels, title and axes ticks
ax.set_ylabel('Speedup')
ax.set_title('Speedup normalized to IQ router')
ax.legend()
ax.grid()
plt.xticks(ind,simulations,rotation='vertical')
#
#
#"""
#def autolabel(rects):
#    """
#    Attach a text label above each bar displaying its height
#    """
#    for rect in rects:
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                '%d' % int(height),
#                ha='center', va='bottom')
#
#autolabel(rects1)
#autolabel(rects2)
#"""
#
plt.show()
