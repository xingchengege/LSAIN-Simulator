
from m5.params import *
from m5.objects import *

from common import FileSystemConfig

from topologies.BaseTopology import SimpleTopology

from topologies.Cluster import Cluster

# Creates a NVIDIA DGX1 Topology



class NVIDIADGX1(SimpleTopology):
    description = "NVIDIADGX1"

    def __init__(self, controllers):
        self.nodes = controllers
        

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes
        
        num_dgx = options.num_dgx
        # assert nodes == 10 * num_dgx
        assert options.network == "booksim"
        gpu_routers_id = []
        cpu_routers_id = []  
        cpu_nodes = []
        gpu_nodes = []
        gpu_mem_nodes = []
        cpu_mem_nodes = []
        
        for node in nodes:
            assert type(node) == Cluster
            if node.getClusterName() == "cpuCluster":
                cpus = node.getAllNodes()
                for cpu in cpus:
                    cpu_nodes.append(cpu)
            elif node.getClusterName() == "gpuCluster":
                gpus = node.getAllNodes()
                for gpu in gpus:
                    assert type(gpu) == Cluster
                    gpu_nodes.append(gpu)
            elif node.getClusterName() == "gpuMemCluster":
                mems = node.getAllNodes()
                for mem in mems:
                    gpu_mem_nodes.append(mem)
            elif node.getClusterName() == "cpuMemCluster":
                mems = node.getAllNodes()
                for mem in mems:
                    cpu_mem_nodes.append(mem)

        # for node in nodes:
        #     if node == "L1Cache_Controller" :
        # if buildEnv["PROTOCOL"] == "GPU_VIPER":
        #     for node in nodes:
        #         if type(node) == Cluster:
        #             gpu_nodes.append(node)
        #         else :
        #             cpu_nodes.append(node)
        # else :
        
        
        # add gpu node
        for i in range(num_dgx):
            for j in range(2):
                for k in range(4):
                    gpu_routers_id.append(i * 14 + j * 7 + 3 + k)
                cpu_routers_id.append(i * 14 + j * 7)
        num_routers = 14 * num_dgx
        link_latency = options.link_latency
        router_latency = options.router_latency
        routers = [
            Router(router_id = i, latency = router_latency)
            for i in range(num_routers)
        ]
        

        network.routers = routers
        
        link_count = 0
        ext_links = []

        int_links = []
        
        for (i, cpu_node) in enumerate(cpu_nodes):
            cntrl_level, j = divmod(i, len(cpu_routers_id))
            router_id = cpu_routers_id[j]
            ext_links.append(
                    ExtLink(
                    link_id = link_count,
                    ext_node = cpu_node,
                    int_node = routers[router_id],
                    latency = link_latency,
				    )
			    )
            link_count += 1
    
        for(i, mem_node) in enumerate(gpu_mem_nodes):
            cntrl_level, j = divmod(i, len(gpu_routers_id))
            router_id = gpu_routers_id[j]
            ext_links.append(
                ExtLink(
                link_id = link_count,
                ext_node = mem_node,
                int_node = routers[router_id],
                latency = link_latency
				)
			)
            link_count += 1
        
        for(i, mem_node) in enumerate(cpu_mem_nodes):
            cntrl_level, j = divmod(i, len(cpu_routers_id))
            router_id = cpu_routers_id[j]
            ext_links.append(
                ExtLink(
                link_id = link_count,
                ext_node = mem_node,
                int_node = routers[router_id],
                latency = link_latency
				)
			)
            link_count += 1
        for (i, gpu_node) in enumerate(gpu_nodes):
            cntrl_level, j = divmod(i, len(gpu_routers_id))
            router_id = gpu_routers_id[j]
            gpu_components = gpu_node.getAllNodes()
            for gpu_component in gpu_components:
                ext_links.append(
						ExtLink(
						link_id = link_count,
						ext_node = gpu_component,
						int_node = routers[router_id],
						latency = link_latency,
						)
					)
                link_count += 1
                
        # routers_id = cpu_router_id + gpu_routers_id[1:]
        # print(len(routers_id))
        # for (i, node) in enumerate(nodes):
        #     if type(node) == Cluster:
        #         gpu_nodes = node.getAllNodes()
        #         for (j, gpu_node) in enumerate(gpu_nodes):
        #             ext_links.append(
        #                 ExtLink(
        #                 link_id=link_count,
        #                 ext_node=gpu_node,
        #                 int_node=routers[gpu_routers_id[0]],
        #                 latency=link_latency,
        #                 )
        #             )
        #             link_count += 1
        #     else:
        #         cntrl_level, j = divmod(i, len(routers_id))
                
        #         router_id = routers_id[j]
        #         ext_links.append(
        #             ExtLink(
        #             link_id = link_count,
        #             ext_node = node,
        #             int_node = routers[router_id],
        #             latency = link_latency,
		# 		    )
		# 	    ) 
        #         link_count += 1
        

        # build BinaryTree Topology
        # for (id, offset) in enumerate(cpu_router_id):
                
        #         # CPU<---->PCIe Switch
        #         left_PS_node = offset + 1
        #         right_PS_node = offset + 2
        #         int_links.append(
        #             IntLink(
        #                 link_id=link_count,
        #                 src_node=routers[offset],
        #                     dst_node=routers[left_PS_node],
        #                 latency=link_latency,
        #                 bandwidth_factor=8
        #                 )
        #         )
        #         link_count += 1
        #         int_links.append(
        #             IntLink(
        #                 link_id=link_count,
        #                 src_node=routers[offset],
        #                     dst_node=routers[right_PS_node],
        #                 latency=link_latency,
        #                 bandwidth_factor=8
        #                 )
        #         )
        #         link_count += 1
        #         for i in range(2, 4):
        #             PS_node = offset + i - 1
                    
        #             # PCIe Switch <---->GPU
        #             left_GPU_node = offset + i * 2 - 1
        #             right_GPU_node = offset + i * 2
        #             int_links.append(
        #                 IntLink(
        #                     link_id=link_count,
        #                     src_node=routers[PS_node],
        #                     dst_node=routers[left_GPU_node],
        #                     latency=link_latency,
        #                     bandwidth_factor=8
        #                 )
        #             )
        #             link_count += 1
        #             int_links.append(
        #                 IntLink(
        #                     link_id=link_count,
        #                     src_node=routers[PS_node],
        #                     dst_node=routers[right_GPU_node],
        #                     latency=link_latency,
        #                     bandwidth_factor=8
        #                 )
        #             )
        #             link_count += 1
        #             # PCIe Switch <----> CPU
        #             father_CPU_node = offset + i / 2 - 1
        #             int_links.append(
        #                 IntLink(
        #                     link_id=link_count,
        #                     src_node=routers[PS_node],
        #                     dst_node=routers[int(father_CPU_node)],
        #                     latency=link_latency,
        #                     bandwidth_factor=8
        #                 )
        #             )
        #             link_count += 1
        #         for i in range(4, 8):
        #             GPU_node = offset + i - 1
                    
        #             # GPU <----> PCIe Switch 
        #             father_PC_node = offset + i / 2 - 1
        #             int_links.append(
        #                 IntLink(
        #                     link_id=link_count,
        #                     src_node=routers[GPU_node],
        #                     dst_node=routers[int(father_PC_node)],
        #                     latency=link_latency,
        #                     bandwidth_factor=8
        #                 )
        #             )
        #             link_count += 1
                    
        
        
        # # CPU <----> CPU            
        # for (id,cpu_node0) in enumerate(cpu_router_id):
        #     for (id,cpu_node1) in enumerate(cpu_router_id):
        #         if cpu_node0 == cpu_node1:
        #             continue
        #         int_links.append(
        #             IntLink(
        #                 link_id=link_count,
        #                 src_node=routers[cpu_node0],
        #                 dst_node=routers[cpu_node1],
        #                 latency=link_latency,
        #                 bandwidth_factor=8
        #             )
        #         )
        #         link_count += 1
        # # build HyperMesh Topology
        # for (i, gpu_node) in enumerate(gpu_routers_id):
        #     diagonal_gpu = 0
        #     other_plane_gpu = 0
        #     left_gpu = 0
        #     right_gpu = 0
        #     if gpu_node / 7 == (gpu_node + 2) / 7 :
        #         diagonal_gpu = gpu_node + 2
        #     else :
        #         diagonal_gpu = gpu_node - 2
            
        #     if gpu_node / 14 == (gpu_node + 7) / 14 :
        #         other_plane_gpu = gpu_node + 7
        #     else :
        #         other_plane_gpu = gpu_node - 7
            
        #     if gpu_node / 7 == (gpu_node + 3) / 7 :
        #         left_gpu = gpu_node + 3
        #     else :
        #         left_gpu = gpu_node - 1
            
        #     if gpu_node / 7 == (gpu_node + 1) / 7 :
        #         right_gpu = gpu_node + 1
        #     else :
        #         right_gpu = gpu_node - 3

        #     int_links.append(
        #         IntLink(
        #             link_id=link_count,
        #             src_node=routers[gpu_node],
        #             dst_node=routers[diagonal_gpu],
        #             latency=link_latency,
        #             bandwidth_factor=10
        #         )
        #     )
        #     link_count += 1
        #     int_links.append(
        #         IntLink(
        #             link_id=link_count,
        #             src_node=routers[gpu_node],
        #             dst_node=routers[other_plane_gpu],
        #             latency=link_latency,
        #             bandwidth_factor=10
        #         )
        #     )
        #     link_count += 1
        #     int_links.append(
        #         IntLink(
        #             link_id=link_count,
        #             src_node=routers[gpu_node],
        #             dst_node=routers[left_gpu],
        #             latency=link_latency,
        #             bandwidth_factor=10
        #         )
        #     )
        #     link_count += 1
        #     int_links.append(
        #         IntLink(
        #             link_id=link_count,
        #             src_node=routers[gpu_node],
        #             dst_node=routers[right_gpu],
        #             latency=link_latency,
        #             bandwidth_factor=10
        #         )
        #     )   
        #     link_count += 1
        
        network.ext_links = ext_links
        # network.int_links = int_links

    def registerTopology(self, options):
        for i in range(options.num_cpus):
            FileSystemConfig.register_node(
                [i], MemorySize(options.mem_size) // options.num_cpus, i
            )

