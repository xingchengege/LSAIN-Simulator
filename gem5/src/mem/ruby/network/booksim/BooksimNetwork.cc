
#include "mem/ruby/network/booksim/NetworkSwitch.hh"
#include "mem/ruby/network/booksim/NetworkInterface.hh"
#include "mem/ruby/network/booksim/BooksimNetwork.hh"
#include "mem/ruby/network/simple/SimpleLink.hh"
namespace gem5
{

namespace ruby
{

namespace booksim
{

	BooksimNetwork::BooksimNetwork(const Params & p)
	    : Network(p)
	{
		m_wakeup_cycles = 0;

		m_switchID.resize(m_nodes);

		for(std::vector<BasicRouter*>::const_iterator i = p.routers.begin();
		    i != p.routers.end();
			i++)
		{
			NetworkSwitch* s = safe_cast<NetworkSwitch*> (*i);
			s->init_net_ptr(this);
			m_switches.push_back(s);
		}

		_number_switches = m_switches.size();

		m_booksim_wrapper = new BooksimWrapper(p.booksim_config);
	}

	void
	BooksimNetwork::init()
	{
		Network::init();
		assert(m_topology_ptr != NULL);
		m_topology_ptr->createLinks(this);
	}

	BooksimNetwork::~BooksimNetwork()
	{

	}

	void
	BooksimNetwork::printStats(std::ostream & out) const 
	{
		m_booksim_wrapper->PrintStats(out);
	}

	void
	BooksimNetwork::clearStats()
	{
		m_booksim_wrapper->ResetStats();
	}

	void
	BooksimNetwork::printConfig(std::ostream & out) const
	{
		m_booksim_wrapper->PrintConfig(out);
	}

	void
	BooksimNetwork::reset()
	{
		for(int node = 0; node < m_nodes; node++)
		{
			for(int j = 0; j < m_virtual_networks; j++)
			{
				m_toNetQueues[node][j]->clear();
				m_fromNetQueues[node][j]->clear();
			}
		}
	}

	void
	BooksimNetwork::print(std::ostream & out) const
	{
		out << "[BooksimNetwork]";
	}

	MachineID
	BooksimNetwork::getSwitchID(NodeID node)
	{
		for(MachineType m = MachineType_FIRST; m < MachineType_NUM; ++m)
		{
			int num_machines = MachineType_base_count(m);
			if(node < num_machines)
			{
				MachineID mid = {m, node};
				return mid;
			}
			else{
				node = node - num_machines;
			}
		}
		MachineType merror = MachineType_FIRST;
		MachineID error = {merror, node};
		return error;
	}

	void
	BooksimNetwork::makeExtOutLink(SwitchID src, NodeID dest, BasicLink * link,
	                               std::vector<NetDest>& routing_table_entry)
	{
		assert(dest < m_nodes);
		assert(src < m_switches.size());
		assert(m_switches[src] != NULL);

		SimpleExtLink* simple_link = safe_cast<SimpleExtLink* > (link);

		m_switches[src]->addOutPort(m_fromNetQueues[dest],
			                        routing_table_entry,
			                        simple_link->m_latency,
			                        simple_link->m_bw_multiplier);
	}

	void
	BooksimNetwork::makeExtInLink(NodeID src, SwitchID dest, BasicLink* link,
	                              std::vector<NetDest>& routing_table_entry)
	{
		assert(src < m_nodes);
		m_switchID[src] = dest;
		m_switches[dest]->addInPort(m_toNetQueues[src]);
	}

	void 
	BooksimNetwork::makeInternalLink(SwitchID src, SwitchID dest, BasicLink *link,
			                      std::vector<NetDest>& routing_table_entry,
								  PortDirection src_outport_dirn,
								  PortDirection dest_inport_dirn)
	{
	}

	void
	BooksimNetwork::RunCycles(int cycles)
	{
		incTotalCycles();

		for (int i = 0; i < m_switches.size(); i++){
			m_switches[i]->ReadMessage();
		}

		m_booksim_wrapper->RunCycles(cycles);

		RetirePackets();
	}
	bool 
	BooksimNetwork::functionalRead(Packet* pkt)
	{

	}
	uint32_t 
	BooksimNetwork::functionalWrite(Packet* pkt)
	{
		
	}

	void
	BooksimNetwork::collateStats()
	{

	}

	void
	BooksimNetwork::regStats()
	{
		Network::regStats();
		total_packet_lat
		    .name(name() + ".total_plat")
			.desc("Total packet latency")
			;
		total_network_lat
		    .name(name() + ".total_nlat")
			.desc("Total network latency")
			;
		total_hops
		    .name(name() + ".total_hops")
			.desc("Total hops")
			;
		total_cycles
		    .name(name() + ".total_cycles")
			.desc("Total cycles")
			;
		total_inject_flits
		    .name(name() + ".total_inject_flits")
			.desc("Total inject flits")
		    ;
		total_accept_flits
		    .name(name() + ".total_accept_flits")
			.desc("Total accept flits")
			;
		total_inject_packets
		    .name(name() + ".total_inject_packets")
			.desc("Total inject packets")
			;
		total_accept_packets
		    .name(name() + ".total_accept_packets")
			.desc("Total accept packets")
			;
		avg_plat
		    .name(name() + ".avg_plat")
			.desc("Avg. packet latency")
			;
		avg_nlat
		    .name(name() + ".avg_nlat")
			.desc("Avg. network latency")
			;
		avg_throughput
		    .name(name() + ".avg_throughput")
			.desc("Avg. throughput")
			;
		avg_hops
		    .name(name() + ".avg_hops")
			.desc("Avg. number of hops")
			;
		avg_packet_size
		    .name(name() + ".avg_packet_size")
			.desc("Avg. packet size")
			;
		avg_inject_flits
		    .name(name() + ".avg_inject_flits")
			.desc("Avg. inject flits")
			;
		avg_inject_packets
		    .name(name() + ".avg_inject_packets")
			.desc("Avg. inject packets")
			;
		avg_plat = total_packet_lat / total_accept_packets;
		avg_nlat = total_network_lat / total_accept_packets;
		avg_throughput = total_accept_flits/ total_cycles / _number_switches;
		avg_hops = total_hops / total_accept_packets;
		avg_packet_size = total_accept_flits / total_accept_packets;
		avg_inject_flits = total_inject_flits / total_cycles / _number_switches;
		avg_inject_packets = total_inject_packets / total_cycles / _number_switches;
	}
}

}

}