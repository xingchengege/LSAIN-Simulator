#!/usr/bin/python3

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

import sys
import re
import matplotlib.pyplot as plt
import numpy as np

log_file = sys.argv[1]
num_L1s = int(sys.argv[2])
window_size = float(sys.argv[3])

generated_messages_dicts = list()
for l1 in range(num_L1s):
    generated_messages_dicts.append(dict())
#generated_messages_dict = dict()

initial_arrival_time = sys.maxsize
final_arrival_time = 0


for line in open(log_file):
    if 'requestFromL1Cache' in line:
        m = re.match(r"(\d+): system\.ruby\.l1_cntrl(\d+)\.requestFromL1Cache:
                                Enqueue arrival_time: (\d+)",line)
        #print("Cache: ", m.group(2), " Cycle: ", int(m.group(3))/500)
        thread = int(m.group(2))
        arrival_time = int(int(m.group(3))/500)

        if arrival_time < initial_arrival_time:
            initial_arrival_time = arrival_time
        if arrival_time > final_arrival_time:
            final_arrival_time = arrival_time

        if str(arrival_time) in generated_messages_dicts[thread]:
            generated_messages_dicts[thread][str(arrival_time)] += 1
        else:
            generated_messages_dicts[thread][str(arrival_time)] = 1

# Convert fict into list filling all empty cycles with 0s

generated_messages_list = list()
for thread in range(num_L1s):
    last_window = 0
    generated_messages_list.append(list())
    for i in range(initial_arrival_time, final_arrival_time):
        if int(i/window_size) == last_window:
            if str(i) in generated_messages_dicts[thread]:
                generated_messages_list[thread][-1] += \
                          generated_messages_dicts[thread][str(i)]
        else:
            if str(i) in generated_messages_dicts[thread]:
                generated_messages_list[thread].append(
                          generated_messages_dicts[thread][str(i)]
                                        )
            else:
                generated_messages_list[thread].append(0)
        last_window = int(i/window_size)

    samples = np.array(generated_messages_list[thread])
    print('Thread: ', thread, ' histogram: ', np.histogram(samples))
