#ifndef __NVIDIA_DGX_1_CPP__
#define __NVIDIA_DGX_1_CPP__

#include "nvidia_dgx_1.hpp"
#include <fstream>
#include <sstream>
#include <limits>
#include <algorithm>
namespace gem5
{
	
namespace ruby
{

namespace booksim
{

	// map<int, int>* global_routing_table;
	map<int, set<int > >* global_out_ports;
	map<int, int>* global_actual_node;
	NVIDIADGX1::NVIDIADGX1(const Configuration& config, const string &name)
	    : Network( config, name)
	{
		router_list.resize(2);
		num_dgx1 = config.GetInt("num_dgx1");
		assert(num_dgx1 >= 1);
		string tv = config.GetStr("dgx1_version");
		if(tv=="P100")
		    _v = version::P100;
		else if(tv=="V100")
		    _v = version::V100;
		else Error( "Unkown DGX-1 Version: " + tv );
		_buildTopology();
		_ComputeSize( config );
		_Alloc( );
		_BuildNet( config );
	}

	NVIDIADGX1::~NVIDIADGX1(){
		
		GPU_node_list.clear();
		CPU_node_list.clear();
	}

	void NVIDIADGX1::_buildTopology()
	{
		
		// 将node与CPU/GPU对应起来，每个dgx1中有14个节点，结构为：
		//             node0(CPU)
		//            /          \
		//           /            \
		//          /              \
		//    node1(PS)            node2(PS)
		//    /       \            /        \
		//   /         \          /          \
		//  /           \        /            \
		//node3(GPU) node4(GPU) node5(GPU) node6(GPU)
			
		for(int i = 0; i < num_dgx1; i++)
		{
			for(int plane = 0; plane < 2; plane++)
			{
				_buildBinaryTree(i * 14 + plane * 7);
			}
			_buildHyperCube();
			int CPU_0 = i * 14;
			int CPU_1 = i * 14 + 7;
			router_list[ROUTER_ROUTER][CPU_0][CPU_1]=
			                    pair<int, BusLatency>(-1, QPI);
			router_list[ROUTER_ROUTER][CPU_1][CPU_0]=
			                    pair<int, BusLatency>(-1, QPI);
		}
	}

	void NVIDIADGX1::_ComputeSize( const Configuration &config)
	{
		_channels = 0;
		cout<<"******************node listing**********************\n";
		map<int,  int >::iterator iter;
		for(iter = node_list.begin(); iter!=node_list.end(); iter++){
			cout<<"Node "<<iter->first;
			cout<<"\tRouter "<<iter->second<<endl;
		}

		map<int,   map<int, pair<int,BusLatency> > >::iterator iter3;
		_nodes = 0;
		cout<<"\n****************router to node listing*************\n";
		for(iter3 = router_list[NODE_ROUTER].begin(); iter3!=router_list[NODE_ROUTER].end(); iter3++){
			cout<<"Router "<<iter3->first<<endl;
			map<int, pair<int,BusLatency> >::iterator iter2;
			for(iter2 = iter3->second.begin(); 
			iter2!=iter3->second.end(); 
			iter2++){
			cout<<"\t Node "<<iter2->first<<" lat "<<iter2->second.second<<endl;
			// if(GPU_node_list.find(iter2->first)!=GPU_node_list.end())
			//    _nodes+=8;
			// else _nodes+=16;
			// // _nodes += _getLanesNum(iter2->second.second);
			// // _nodes += 1;
			}
		}

		cout<<"\n*****************router to router listing************\n";
		for(iter3 = router_list[ROUTER_ROUTER].begin(); iter3!=router_list[ROUTER_ROUTER].end(); iter3++){
			cout<<"Router "<<iter3->first<<endl;
			map<int, pair<int, BusLatency> >::iterator iter2;
			if(iter3->second.size() == 0){
			cout<<"Caution Router "<<iter3->first
			<<" is not connected to any other Router\n"<<endl;
			}
			for(iter2 = iter3->second.begin(); 
			iter2!=iter3->second.end(); 
			iter2++){
				cout<<"\t Router "<<iter2->first<<" lat "<<iter2->second.second<<endl;
				//总线的每条lanes对应于一个channel
				_channels += _getLanesNum(iter2->second.second);
				// _channels++;
			}
		}
		_size = router_list[ROUTER_ROUTER].size();
		_nodes = 64 * node_list.size();
		// cout<<_nodes<<endl;
	}

	void NVIDIADGX1::_BuildNet( const Configuration &config)
	{
		// cout<<_nodes<<endl;
		actual_outports.resize(_size);
		last_vnode.resize(_size);
		int* virtual_outport = (int *) malloc(sizeof(int)* _size);
		for(int i = 0; i < _size; i++)virtual_outport[i] = 0;
		// int* outport = (int *) malloc(sizeof(int)* _size);
		// for(int i = 0; i < _size; i++)outport[i] = 0;

		cout<<"==========================Node to Router =====================\n";
		//adding the injection/ejection channels first
		int vnode = 0;
		map<int, map<int, pair<int, BusLatency> > >::iterator niter;
		for(niter = router_list[NODE_ROUTER].begin(); niter != router_list[NODE_ROUTER].end(); niter++)
		{
			// map<int, map<int, pair<int, BusLatency> > >::iterator riter = 
			//                         router_list[ROUTER_ROUTER].find(niter->first);
			//caculate radix
			// int radix = 32 * niter->second.size()+riter->second.size();
			int radix = _getRouterPortsNum(niter->first);
			int node = niter->first;
			cout<<"router "<<node<<" radix "<<radix<<endl;
			//declare the routers
			ostringstream router_name;
			router_name << "router";
			router_name << "_" << node;
			_routers[node] = Router::NewRouter( config, this, router_name.str(),
			                        node, radix, radix);
			_timed_modules.push_back(_routers[node]);
			//add injection ejection channels
			map<int, pair<int, BusLatency>>::iterator nniter;
			for(nniter = niter->second.begin(); nniter!=niter->second.end(); nniter++)
			{
				int link = nniter->first;
				(niter->second)[link].first = virtual_outport[node];
				last_vnode[link] = virtual_nodes[link].begin();
				// outport[node]++;
				cout<<"\t connected to node "<<link<<" at outport "<<nniter->second.first
				<<" lat "<<nniter->second.second<<endl;
				// int lat_perlane = (int)nniter->second.second;
		        // int lanes_num = 1;
				// int lanes_num = _getLanesNum(nniter->second.second);
				// if(GPU_node_list.find(link)!=GPU_node_list.end())
				int lanes_num = 64;
				// else lanes_num = 16;
				for(int i = 0; i < lanes_num; i++){
					actual_outports[node][nniter->second.first].insert(actual_outcnt[node]);
					// cout<<"vnode: "<<vnode<<" actual outport: "<< actual_outcnt[node]<<endl;
			     	actual_outcnt[node]++;
					virtual_nodes[link].insert(vnode);
					actual_node[vnode] = link;
					_inject[vnode]->SetLatency(1);
					_inject_cred[vnode]->SetLatency(1);
					_eject[vnode]->SetLatency(1);
					_eject_cred[vnode]->SetLatency(1);

					_routers[node]->AddInputChannel(_inject[vnode], _inject_cred[vnode]);
					_routers[node]->AddOutputChannel(_eject[vnode], _eject_cred[vnode]);
					vnode++;
				}
				virtual_outport[node]++;
				// for(int i = 0; i < lanes_num; i++){
			    //   	// actual_outports[node][nniter->second.first].insert(actual_outcnt[node]);
				// 	// cout<<"vnode: "<<vnode<<" actual outport: "<< actual_outcnt[node]<<endl;
			    //  	// actual_outcnt[node]++;
				// 	// virtual_nodes[link].insert(vnode);
				// 	// actual_node[vnode] = link;
			    //  	// link += i;
				// 	// _inject[link]->SetLatency(1);
				// 	// _inject_cred[link]->SetLatency(1);
				// 	// _eject[link]->SetLatency(1);
				// 	// _eject_cred[link]->SetLatency(1);
				// 	_inject[vnode]->SetLatency(1);
				// 	_inject_cred[vnode]->SetLatency(1);
				// 	_eject[vnode]->SetLatency(1);
				// 	_eject_cred[vnode]->SetLatency(1);

				// 	_routers[node]->AddInputChannel( _inject[vnode], _inject_cred[vnode] );
				// 	_routers[node]->AddOutputChannel( _eject[vnode], _eject_cred[vnode] );
			    //     vnode++;
				// }
				// actual_outports[node][virtual_outport[node]]
				// virtual_outport[node]++;
			}

		}

		cout<<"==========================Router to Router =====================\n";
		//add inter router channels
		//since there is no way to systematically number the channels we just start from 0
		//the map, is a mapping of output->input
		// int channel_count = 0;
		int vchannel_count = 0;
		int pchannel_count = 0;
		for(niter = router_list[NODE_ROUTER].begin(); niter != router_list[NODE_ROUTER].end(); niter++)
		{
			map<int, map<int, pair<int, BusLatency> > >::iterator riter = 
			                                router_list[ROUTER_ROUTER].find(niter->first);
			int node = niter->first;
			map<int, pair<int, BusLatency> >::iterator rriter;
			cout<<"router "<<node<<endl;
			for(rriter = riter->second.begin(); rriter != riter->second.end(); rriter++)
			{
				int other_node = rriter->first;
				int link = vchannel_count;
				//add the output port assigned to the map
				(riter->second)[other_node].first = virtual_outport[node];
				cout<<"\t connected to router "<<other_node<<" using link "<<link
				<<" at outport "<<rriter->second.first
				<<" lat "<<rriter->second.second<<endl;
				int lat_perlane = (int)rriter->second.second;
		        int lanes_num = _getLanesNum(rriter->second.second);
				for(int i = 0; i < lanes_num; i++){
			      	actual_outports[node][rriter->second.first].insert(actual_outcnt[node]);
			     	actual_outcnt[node]++;
					link = pchannel_count;
					// cout<<"plink "<<link<<" actual outport: "<<actual_outcnt[node] - 1 <<endl;
			     	_chan[link]->SetLatency(lat_perlane);
					_chan_cred[link]->SetLatency(lat_perlane);

					_routers[node]->AddOutputChannel( _chan[link], _chan_cred[link] );
					_routers[other_node]->AddInputChannel( _chan[link], _chan_cred[link]);
					pchannel_count++;
				}
				vchannel_count++;
			    virtual_outport[node]++;
			}
		}
		_buildRoutingTable();
	}

	void NVIDIADGX1::_buildBinaryTree(int offset)
	{
		int CPU_node = offset;
		CPU_node_list.insert(CPU_node);
		node_list[CPU_node] = CPU_node;
		router_list[NODE_ROUTER][CPU_node][CPU_node] = 
		                        pair<int, BusLatency>(-1, PCIe_Gen3_x16);
		// CPU---PCIe Switch
		int left_PS_node = offset + 1;
		int right_PS_node = offset + 2;
		router_list[ROUTER_ROUTER][CPU_node][left_PS_node] = 
		                        pair<int, BusLatency>(-1, PCIe_Gen3_x16);
		router_list[ROUTER_ROUTER][CPU_node][right_PS_node] = 
		                        pair<int, BusLatency>(-1, PCIe_Gen3_x16); 
		for(int i = 2; i <= 3; i++) {
			int PS_node = offset + i - 1;
			PCIe_Switch_list.insert(PS_node);
			node_list[PS_node] = PS_node;

			router_list[NODE_ROUTER][PS_node][PS_node] = 
			                        pair<int, BusLatency>(-1, PCIe_Gen3_x16);
			// PCIe Switch----GPU
			int left_GPU_node = offset + i * 2 - 1;
			int right_GPU_node = offset + i * 2;
			router_list[ROUTER_ROUTER][PS_node][left_GPU_node] = 
			                        pair<int, BusLatency>(-1, PCIe_Gen3_x16);
			router_list[ROUTER_ROUTER][PS_node][right_GPU_node] = 
			                        pair<int, BusLatency>(-1, PCIe_Gen3_x16);
		    // PCIe Switch----CPU
			int father_CPU_node = offset + i / 2 - 1;
			router_list[ROUTER_ROUTER][PS_node][father_CPU_node] = 
		                        pair<int, BusLatency>(-1, PCIe_Gen3_x16);
		
		}
		for(int i = 4; i <= 7; i++) {
			int GPU_node = offset + i - 1;
			GPU_node_list.insert(GPU_node);
			node_list[GPU_node] = GPU_node;
			router_list[NODE_ROUTER][GPU_node][GPU_node] = 
			                        pair<int, BusLatency>(-1, NVLink_V1);
			// GPU----PCIe Switch
			int father_PS_node = offset + i / 2 - 1;
			router_list[ROUTER_ROUTER][GPU_node][father_PS_node] = 
			                        pair<int, BusLatency>(-1, PCIe_Gen3_x16);
		}
		
	}

	void NVIDIADGX1::_buildHyperCube()
	{
		for(auto GPU_node: GPU_node_list)
		{
			int diagonal_GPU = (GPU_node / 7 == (GPU_node + 2) / 7) ?
			                   GPU_node + 2 : GPU_node - 2;
			int other_plane_GPU = (GPU_node / 14 == (GPU_node + 7) / 14) ?
			                   GPU_node + 7 : GPU_node - 7;
			int left_GPU = (GPU_node / 7 == (GPU_node + 3) / 7) ?
			                   GPU_node + 3 : GPU_node - 1;
			int right_GPU = (GPU_node / 7 == (GPU_node + 1) / 7) ?
			                   GPU_node + 1 : GPU_node - 3;
			// GPU---GPU
			if(_v==version::P100){
				router_list[ROUTER_ROUTER][GPU_node][diagonal_GPU] = 
										pair<int, BusLatency>(-1, NVLink_V1);
				router_list[ROUTER_ROUTER][GPU_node][other_plane_GPU] = 
										pair<int, BusLatency>(-1, NVLink_V1);
				router_list[ROUTER_ROUTER][GPU_node][left_GPU] = 
										pair<int, BusLatency>(-1, NVLink_V1);
				router_list[ROUTER_ROUTER][GPU_node][right_GPU] = 
										pair<int, BusLatency>(-1, NVLink_V1);
			}
			else{
				router_list[ROUTER_ROUTER][GPU_node][diagonal_GPU] = 
										pair<int, BusLatency>(-1, NVLink_V1);
				if( GPU_node / 7 == (GPU_node + 2) / 7 ){
					router_list[ROUTER_ROUTER][GPU_node][other_plane_GPU] = 
											pair<int, BusLatency>(-1, NVLink_V2);
					if( GPU_node / 7 == (GPU_node + 3) / 7 ){
						router_list[ROUTER_ROUTER][GPU_node][left_GPU] = 
											pair<int, BusLatency>(-1, NVLink_V2);
						router_list[ROUTER_ROUTER][GPU_node][right_GPU] = 
											pair<int, BusLatency>(-1, NVLink_V1);
					}
					else {
						router_list[ROUTER_ROUTER][GPU_node][left_GPU] = 
											pair<int, BusLatency>(-1, NVLink_V1);
						router_list[ROUTER_ROUTER][GPU_node][right_GPU] = 
											pair<int, BusLatency>(-1, NVLink_V2);
					}
				}
				else {
					router_list[ROUTER_ROUTER][GPU_node][other_plane_GPU] = 
											pair<int, BusLatency>(-1, NVLink_V1);
					router_list[ROUTER_ROUTER][GPU_node][left_GPU] = 
											pair<int, BusLatency>(-1, NVLink_V2);
					router_list[ROUTER_ROUTER][GPU_node][right_GPU] = 
											pair<int, BusLatency>(-1, NVLink_V2);
				}
				
			}
		}	
		
	}
	
	int NVIDIADGX1::_getLanesNum(BusLatency bus){
		int lanes_num = 0;
		// return 1;
		switch (bus)
		 {
		 	case BusLatency::PCIe_Gen3_x16 :
				lanes_num = 16;
				break;
			case BusLatency::NVLink_V1 :
			    lanes_num = 8;
				break;
			case BusLatency::NVLink_V2 :
			    lanes_num = 8;
				break;
			default:
			    lanes_num = 1;
				break;
		}
		return lanes_num;
	}

    int NVIDIADGX1::_getRouterPortsNum(int router){
		map<int, map<int, pair<int, BusLatency> > >::iterator niter = 
			                        router_list[NODE_ROUTER].find(router);
		map<int, map<int, pair<int, BusLatency> > >::iterator riter = 
			                        router_list[ROUTER_ROUTER].find(router);
		// int radix = niter->second.size();
		int radix = 0;
		for(auto x : niter->second){
			radix += 64;
		}
		for(auto x : riter->second){
			radix += _getLanesNum(x.second.second);
		}
		return radix;
	}
	
	void NVIDIADGX1::_buildRoutingTable(){
		cout<<"========================== Routing table  =====================\n";  
        routing_table.resize(_size);
		for(auto GPU_node : GPU_node_list)
		    hypermesh_min_route(GPU_node);
		for(auto CPU_node : CPU_node_list){
		    binarytree_route(CPU_node);
		}
		for(auto PS : PCIe_Switch_list){
		    // cout<<"PS: "<<PS<<endl; 
			binarytree_route(PS);
		}
		// for(int i = 0; i < _size; i++)
		// {
		// 	// if(GPU_node_list.find(i) != GPU_node_list.end())
		// 		hypermesh_min_route(i);
		// 	// else
		// 	    // binarytree_route(i);
			
		// }

		for(int i = 0; i<_size;i++){
			cout<<"router i: "<<i<<endl;
			for(int j =0;j<_size;j++){
				cout<<"router i: "<<i<<" to router j: "<<j<<" to output: "<< routing_table[i][j]<<endl;
			}
			cout<<endl;
		}
		global_routing_table = &routing_table[0];
		global_out_ports = &actual_outports[0];
		global_actual_node = &actual_node;
	}
	
	// basically dijkstra's
	void NVIDIADGX1::hypermesh_min_route(int r_start){
		int* dist = new int[_size];
		int* prev = new int[_size];
		set<int> rlist;
		for(int i = 0; i < _size; i++)
		{
			dist[i] = numeric_limits<int>::max();
			prev[i] = -1;
			rlist.insert(i);
		}
		dist[r_start] = 0;
		while (!rlist.empty())
		{
			//find min
			int min_dist = numeric_limits<int>::max();
			int min_cand = -1;
			for(set<int>::iterator i = rlist.begin(); i != rlist.end(); i++)
			{
				if(dist[*i] < min_dist)
				{
					min_dist = dist[*i];
					min_cand = *i;
				}
			}
			rlist.erase(min_cand);
			
			//neighbor
			for(map<int, pair<int, BusLatency> >::iterator i = router_list[ROUTER_ROUTER][min_cand].begin();
			i != router_list[ROUTER_ROUTER][min_cand].end();
			i++)
			{
				//distance is hops not cycles
				int new_dist = dist[min_cand] + i->second.second;
				if(new_dist < dist[i->first]){
					dist[i->first] = new_dist;
					prev[i->first] = min_cand;
				}
			}
		}
		
		// post process from the prev list
		for(int i = 0; i < _size; i++)
		{
			if(prev[i] == -1){// self
				assert(i == r_start);
				for(map<int, pair<int, BusLatency> >::iterator iter = router_list[NODE_ROUTER][i].begin();
				iter != router_list[NODE_ROUTER][i].end();
				iter++)
				{
					routing_table[r_start][iter->first] = iter->second.first;
				}
			} else {
				int distance = 0;
				int neighbor = i;
				while(prev[neighbor] != r_start)
				{
					assert(router_list[ROUTER_ROUTER][neighbor].count(prev[neighbor]) > 0);
					distance += router_list[ROUTER_ROUTER][prev[neighbor]][neighbor].second; // REVERSE lat
					neighbor = prev[neighbor];
				}
				distance += router_list[ROUTER_ROUTER][prev[neighbor]][neighbor].second;//lat

				assert( router_list[ROUTER_ROUTER][r_start].count(neighbor) != 0);
				int port = router_list[ROUTER_ROUTER][r_start][neighbor].first;
				for(map<int, pair<int, BusLatency> >::iterator iter = router_list[NODE_ROUTER][i].begin();
				 iter != router_list[NODE_ROUTER][i].end();
				 iter++)
				 {
					routing_table[r_start][iter->first] = port;
				 }
			}
		}
		
	}
    // based on lca
	void  NVIDIADGX1::binarytree_route(int r_start){
		
				
		for(int i = 0; i < _size; i++){
			if( i == r_start){
				routing_table[r_start][r_start] = router_list[NODE_ROUTER][r_start][r_start].first;
			} else {
				int next_hop_x, next_hop_y;
				if(r_start / 7 == i / 7){
					pair<int,int> next_node = next_hop(r_start % 7, i % 7);
				    next_node.first += r_start / 7 * 7;
				    next_node.second += i / 7 * 7;
					next_hop_x = next_node.first;
					next_hop_y = next_node.second;
				}
				else{
					if(r_start % 7 == 0)
					   next_hop_x = (r_start + 7) % 14 + r_start / 14 * 14;
					else {
						pair<int,int> next_node = next_hop(0, r_start % 7);
					    next_hop_x = next_node.second + r_start / 7 * 7;
					}
					pair<int,int> next_node = next_hop(0, i % 7);
					next_hop_y = next_node.second + i / 7 * 7;
					
				}
				
				routing_table[r_start][i] = router_list[ROUTER_ROUTER][r_start][next_hop_x].first;
			
				if(GPU_node_list.find(i) != GPU_node_list.end())
					routing_table[i][r_start] = router_list[ROUTER_ROUTER][i][next_hop_y].first;
	
			}
		}
		
	}

	

	
	void NVIDIADGX1::RegisterRoutingFunctions() {
		gRoutingFunctionMap["nccl_nvidiadgx1"] = &nccl_nvidiadgx1;
	}
	
	int NVIDIADGX1::GetVirtualNode(int node) {
		int vnode = *last_vnode[node];
		last_vnode[node]++;
		if(last_vnode[node] == virtual_nodes[node].end())
		   last_vnode[node] = virtual_nodes[node].begin();
		return vnode;
	}
	
	void nccl_nvidiadgx1( const Router *r, const Flit *f, int in_channel,
	                   OutputSet *outputs, bool inject)
	{
		
		set<int> out_ports;
		if(!inject) {
			// int actual_dest = (*global_actual_node)[f->dest]; 
			// if(f->id == 9)
		
			// cout<<"router ID: "<<r->GetID();
			assert(global_routing_table[r->GetID()].count(f->dest)!=0);
			int virtual_outport = global_routing_table[r->GetID()][f->dest];
			assert(global_out_ports[r->GetID()].count(virtual_outport)!=0);
			// if(f->id == 9)
			// cout<<" virtual outport: "<<virtual_outport<<endl;
			out_ports = global_out_ports[r->GetID()][virtual_outport];
		}
		else {
			out_ports.insert(-1);
		}
		int vcBegin = gBeginVCs[f->cl];
		int vcEnd = gEndVCs[f->cl];
		//   int vcBegin = 0, vcEnd = gNumVCs-1;
		//   if ( f->type == Flit::READ_REQUEST ) {
		//     vcBegin = gReadReqBeginVC;
		//     vcEnd   = gReadReqEndVC;
		//   } else if ( f->type == Flit::WRITE_REQUEST ) {
		//     vcBegin = gWriteReqBeginVC;
		//     vcEnd   = gWriteReqEndVC;
		//   } else if ( f->type ==  Flit::READ_REPLY ) {
		//     vcBegin = gReadReplyBeginVC;
		//     vcEnd   = gReadReplyEndVC;
		//   } else if ( f->type ==  Flit::WRITE_REPLY ) {
		//     vcBegin = gWriteReplyBeginVC;
		//     vcEnd   = gWriteReplyEndVC;
		//   }
		outputs->Clear( );

		for(auto out_port: out_ports){
			// if(f->id == 9)
		    // cout<<"actual output: "<< out_port<<endl;
			outputs->AddRange( out_port, vcBegin, vcEnd);
		}

	}
	//based on lca
	pair<int,int> next_hop(int x, int y){
		bool flag = 0;
		x++;
		y++;
		if( dep(x) > dep(y) ){
		   swap(x, y);
		   flag = 1;
		}
		int first_hop_x = x;
		
		int first_hop_y = y;

		int last_hop_y = y;
		bool flag1 = 0, flag2 = 0;
		while(dep(x) < dep(y) ){
			last_hop_y = y;
			y >>= 1;
			if(!flag1){
				first_hop_y = y;
			    flag1 = 1;
			}
		}

		if(x == y) first_hop_x = last_hop_y;

		while( x != y ){
			x >>= 1;
			if(!flag2){
				first_hop_x = x;
			    flag2 = 1;
			}
			y >>= 1;
		}

		if(flag)
			swap(first_hop_x,first_hop_y);
		return {first_hop_x - 1, first_hop_y - 1};
	}

	int dep(int x){
		int d = 0;
		while(x > 0){
			d++;
			x >>= 1;
		}
		return d;
	}

}
}
}
#endif