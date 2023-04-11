# Copyright (c) 2015 University of Cantabria.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Ivan Perez

# This topology is used to map controllers to concentrated ckncube topologies
# of BookSim

from m5.params import *
from m5.objects import *

from topologies.BaseTopology import SimpleTopology
from topologies.BooksimConfig import BooksimConfig

class BooksimMeshDirCorners(SimpleTopology):
    description='BookSimMeshDirCorners'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes

        # First determine which nodes are cache cntrls vs. dirs vs. dma
        l1cache_nodes = []
        l2cache_nodes = []
        dir_nodes = []
        dma_nodes = []
        for node in nodes:
            if node.type == 'L1Cache_Controller':
                l1cache_nodes.append(node)
            elif node.type == 'L2Cache_Controller':
                l2cache_nodes.append(node)
            elif node.type == 'Directory_Controller':
                dir_nodes.append(node)
            elif node.type == 'DMA_Controller':
                dma_nodes.append(node)

        print("""
L1 cache nodes: {}
L2 cache nodes: {}
DIR nodes:      {}
DMA nodes:      {}
                 """.format(
                     len(l1cache_nodes),  
                     len(l2cache_nodes),  
                     len(dir_nodes),  
                     len(dma_nodes)  
                     )
                 )

        # Directories only in corners
        assert(len(dir_nodes) == 4)
        # assert(len(dir_nodes) == 2)



        # We need more routers than nodes to map IDs with BookSim's topology
        # The number of nodes is equal to the number of cpus times 4 as there
        # are 4 types of nodes: L1, L2, DIR, DMA
        num_routers = options.num_cpus * 4

        # Create the routers in the mesh
        routers = [Router(router_id=i) for i in range(num_routers)]
        network.routers = routers

        # link counter to set unique link ids
        link_count = 0

        # Connect each cache controller to the appropriate router
        ext_links = []

        # Read BookSim's configuration file
        booksim_config = BooksimConfig(options.booksim_config)

        # Read k and c. They should be lists of 2 elements
        print 
        booksim_config.params
        k = eval(booksim_config.params["k"])
        c = eval(booksim_config.params["c"])
        assert(len(k) == 2 and
                len(c) == 2 and
                int(booksim_config.params["n"]) == 2)
        # FIXME: this assert is only valid if there is no more
        # concentration than tile one
        assert(k[0]*k[1] == len(l1cache_nodes)) 


        # FIXME: Used concentration configuration: c={2,2}
        assert(c[0] == 2 and c[1] == 2)

        # FIXME: with generic concentrations these iterations
        # must be calculated
        l1_iter = 0 # BookSim node ID (== router_id)
        l1_count = 0 # l1cache_node index
        l2_iter = 1 # BookSim node ID (== router_id)
        l2_count = 0 # l2cache_node index
        for y in range(k[1]):
            for x in range(k[0]):
                ext_links.append(ExtLink(link_id = link_count,
                    ext_node=l1cache_nodes[l1_count],
                    int_node=routers[l1_iter]))
                link_count += 1
                l1_count += 1
                # FIXME: this increment must be evaluated outside these loops
                l1_iter += c[0] 
                ext_links.append(ExtLink(link_id = link_count,
                    ext_node=l2cache_nodes[l2_count],
                    int_node=routers[l2_iter]))
                link_count += 1
                l2_count += 1
                # FIXME: this increment must be evaluated outside these loops
                l2_iter += c[0]
            # FIXME: this increment must be evaluated outside these loops
            l1_iter += k[0]*c[0] 
            # FIXME: this increment must be evaluated outside these loops
            l2_iter += k[0]*c[0]

        # FIXME: these index must be calculated considering
        #        generic concentrations
        dir_iter = [k[0]*c[0],
                #k[0]*c[0]*c[1]-1,
                #num_routers-k[0]*c[0],
                num_routers-2
		]
                
        for index, i in enumerate(dir_iter):
            ext_links.append(ExtLink(link_id = link_count,
                ext_node=dir_nodes[index],
                int_node=routers[i]))
            link_count += 1

        if len(dma_nodes) > 0:
            # FIXME: can the number of DMAs change in function of the ISA used?
            # Yes, indeed. ARM has 3 DMA nodes while X86 1.
            # Perhaps it depends on the coherence protocol
            dma_iter = [k[0]*c[0]+1,
                        k[0]*c[0]*c[1],
                        num_routers-k[0]*c[0] +1
                        ]
            # FIXME: calc index considering generic k and c
            for index, i in enumerate(dma_iter):
                ext_links.append(ExtLink(link_id = link_count,
                    ext_node=dma_nodes[index],
                    int_node=routers[i]))
                link_count += 1

        network.ext_links = ext_links

        # Create internal links following a ring topology. 
        # FIXME: are they required to build the network?
        # Booksim doesn't use them
        int_links = []
        for i in range(num_routers):
            print("""
i: {}
routers: {}
num_router: {}
link_id: {}
            """.format(
                i,
                routers[i],
                num_routers,
                link_count
                ))
            int_links.append(IntLink(link_id=link_count,
                dst_node=routers[i],
                src_node=routers[(i+1)%num_routers]
                #node_a = routers[i],
                #node_b = routers[(i+1)%num_routers])
                )
                )
            link_count += 1

        network.int_links = int_links










