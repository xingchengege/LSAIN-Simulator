/*
DGX-1拓扑结构
*/
#ifndef __NVIDIA_DGX_1_HPP__
#define __NVIDIA_DGX_1_HPP__

#include "network.hpp"
#include "routefunc.hpp"
#include <set>
#include <map>
namespace gem5
{
	
namespace ruby
{

namespace booksim
{


	enum LinkType{
		/*
		NODE_ROUTER: Node to Router
		*/
		NODE_ROUTER = 0,
		/*
		ROUTER_ROUTER: Router to Router
		*/
		ROUTER_ROUTER
	};
	
	enum BusLatency{
		/*
		PCIe_Gen3_x16:
	    bandwidth = 16GB/s
		bandwidth per lane = 16(GB/s)/16 = 1GB/s
		latency per lane = 1(GHz)/ 1(GB/s) / 16(B/flit) = 16 cycles/flit
		*/
		PCIe_Gen3_x16 = 16,
		/*
		NVLink_V1:
	    bandwidth = 20GB/s
		latency per lane = 3(GHz)/ 20(GB/s) / 16(B/flit) = 6.4 cycles/flit ≈ 6 cycles/flit
		*/
		NVLink_V1 = 6,
		/*
	    NVLink_V2:
	    bandwidth = 25GB/s
		latency per lane = 3(GHz)/ 50(GB/s) / 16(B/flit) = 0.96 cycles/flit ≈ 1 cycles/flit
	    */
		NVLink_V2 = 2,
		QPI = 1
	};

	/*the version of NVIDIADGX-1*/
	enum version{
		/*V100-DGX-1*/
		P100 = 0,
		/*P100-DGX-1*/
		V100
	};
	
	class NVIDIADGX1: public Network
	{
		private:
		    // DGX1的版本
		    version _v;
		    // DGX1的数量
		    int num_dgx1;
			//GPU节点列表
			set<int> GPU_node_list;
			//CPU节点列表
			set<int> CPU_node_list;
			// PCIe Switch列表
			set<int> PCIe_Switch_list;
			//associtation between nodes and routers
			map<int, int > node_list;
			//[link type][src router][dest router] = (virtual port, bandwidth GB/s)
			vector<map<int, map<int, pair<int, BusLatency> > > > router_list;
			//stores NCCL routing information from every router to every node
			//[router][dest_node]=virtual port
			vector<map<int, int> > routing_table;

			//[router][virtual port] = {actual port set}
			vector<map<int, set<int > > > actual_outports;
			//[actual node] = {virtual node set}
			map<int, set<int > > virtual_nodes;
			
			map<int,int> actual_node;

			map<int, int> actual_outcnt;
			// Round Robin [actual node] = last used virtual node 
			vector<set<int>::iterator> last_vnode;

			void _ComputeSize( const Configuration &config );
			void _BuildNet( const Configuration &config );
			void _buildRoutingTable( );
			// hypermesh路由：最短路径
			void hypermesh_min_route(int r_start);
			// 二叉树结构的路由：简单的转发到对应端口
			void binarytree_route(int r_start);
			// 创建CPU-GPU间的二叉树状拓扑结构
			void _buildBinaryTree(int offset);
			// 创建GPU-GPU间的hypercube拓扑结构
			void _buildHyperCube();

			void _buildTopology();

			int _getLanesNum(BusLatency bus);

			int _getRouterPortsNum(int router);

		public:
			NVIDIADGX1( const Configuration& config, const string &name );
			~NVIDIADGX1();


			int GetN( ) const{ return -1;}
			int GetK( ) const{ return -1;}

			static void RegisterRoutingFunctions();
			double Capacity( ) const {return -1;}
			void InsertRandomFaults( const Configuration & config){}
			int GetVirtualNode(int node) ;
			int GetActualNode(int node)  {return actual_node[node];}
	};

	void nccl_nvidiadgx1( const Router *r, const Flit *f, int in_channel,
	                   OutputSet *outputs, bool inject);
		
    pair<int,int> next_hop(int x, int y);
	int dep(int x);
}

}
}
#endif