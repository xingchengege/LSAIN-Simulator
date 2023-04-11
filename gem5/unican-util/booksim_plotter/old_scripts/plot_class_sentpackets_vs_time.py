# Author: Ivan Perez (UC)
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

import pandas as pd
from plotly.offline import plot, iplot
import plotly.graph_objs as go
import sys

if len(sys.argv) < 2:
    print "Usage: python plot_stat_vs_time.py <csv file 1>"

layout = go.Layout(
#        title='Avg. Packet Latency',
        xaxis=dict(
            title='time (cycles)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
                )
            ),
        yaxis=dict(
#            title='Avg. packet latency (cycles)',
            title='Sent Packets',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
                )
            )
        )

data = []

csv_file = sys.argv[1]

df = pd.read_csv(csv_file, sep=',')

# FIXME: Read from file
classes = max(df['class'])

initial_time = df.time[0]

for c in range(classes+1):
    data.append(
            go.Scatter(
            x = df.time[df['class'] == c] - initial_time,
            y = df.sent_packets[df['class'] == c],
            mode = 'lines+marksers',
            name = csv_file + '_class_' + str(c)
        )
    )

del df

fig = go.Figure(data=data, layout=layout)
plot(fig, filename='test')
