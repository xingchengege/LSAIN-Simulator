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
from datetime import date
import os

def plotter(stats_dict):
   print "Not implemented"

#files = sys.argv[1]
files = sys.argv[1::]
#statname = sys.argv[2]
stats = [
         "sim_seconds ",
         "host_seconds ",
         "host_inst_rate ",
         "host_tick_rate ",
         "host_mem_usage ",
         ".ipc ",
         "system.ruby.miss_latency_hist_seqr::mean ",
         "system.ruby.network.average_packet_latency ",
         "system.ruby.network.average_hops ",
         "system.ruby.network.flits_injected::total ",
         "system.ruby.network.packets_injected::total ",
         "system.ruby.network.avg_plat ",
         "system.ruby.network.avg_hops ",
         "system.ruby.network.total_flits ",
         "system.ruby.network.total_packets ",
         ".avg_stall_time ",
        ]
translate_stats = {
        "sim_seconds "    : "sim_seconds",
        "host_seconds "   : "host_seconds",
        "host_inst_rate " : "host_inst_rate",
         "host_tick_rate " : "host_tick_rate",
        "host_mem_usage " : "host_mem_usage",
        ".ipc " : "ipc",
        "system.ruby.miss_latency_hist_seqr::mean " : "miss_lat",
        "system.ruby.network.average_packet_latency " : "avg_plat",
        "system.ruby.network.average_hops " : "avg_hops",
        "system.ruby.network.flits_injected::total " : "total_flits",
        "system.ruby.network.packets_injected::total " : "total_packets",
        "system.ruby.network.avg_plat " : "avg_plat",
        "system.ruby.network.avg_hops " : "avg_hops",
        "system.ruby.network.total_flits " : "total_flits",
        "system.ruby.network.total_packets " : "total_packets",
        ".avg_stall_time " : "avg_stall_time",
        }
output_stats = [
        "sim_seconds",
        "host_seconds",
        "host_inst_rate",
        "host_tick_rate",
        "host_mem_usage",
        "ipc",
        "miss_lat",
        "avg_plat",
        "avg_hops",
        "total_flits",
        "total_packets",
        "avg_stall_time",
            ]
#statname = "bw_total::total"
#statblock = int(sys.argv[3])
statblock = 0

current_block = -1;

header = "sim_name,benchmark,version,"
for stat in output_stats:
    header += stat + ","
print header

current_date = date.today().strftime("%Y_%m_%d")
#os.makedirs("results/" + current_date)

dict_values = dict()

for filename in files:
    current_block = -1;
    subdirs = filename.split("/")
    sim_name = subdirs[-3]
#    for subdir in subdirs:
    if "pthreads" in subdirs[-2] or "ompss" in subdirs[-2]:
        name = subdirs[-2].split("_")
        benchmark = name[0]
        version = name[1]
    else:
        name = subdirs[-2].split("_")
        benchmark = name[0]
        version = "None"

    if benchmark in dict_values:
        if sim_name in dict_values[benchmark]:
            dict_values[benchmark][sim_name] = dict()
        else:
            dict_values[benchmark] = {sim_name : dict()}
    else:
        dict_values[benchmark] = {sim_name : dict()}

    total = {key: list() for key in output_stats}

    for line in open(filename):
        # FILTER statblock
        if "---------- Begin Simulation Statistics ----------" in line:
            current_block = current_block + 1

        if current_block == statblock:
            for statname in stats:
                if statname in line:
                    line_list = line.split()
                    stat_value = line_list[1]
                    if stat_value != "nan":
                        total[translate_stats[statname]].append(float(
                            stat_value))
    print_string = sim_name + "," + benchmark + "," + version + ","
    #print_string = "0;"
    for key in output_stats:
        if len(total[key]) > 0:
            print_string += str(sum(total[key])/len(total[key])) + ","
        else:
            print_string += "0,"

    print print_string
