
#ifndef __MEM_RUBY_NETWORK_BOOKSIM_BOOKSIMNETWORK_HH__
#define __MEM_RUBY_NETWORK_BOOKSIM_BOOKSIMNETWORK_HH__

#include "base/types.hh"
#include "mem/ruby/network/Network.hh"
#include "mem/ruby/network/booksim/NetworkSwitch.hh"
#include "params/BooksimNetwork.hh"

#include "booksim_wrapper.hpp"
#include "debug/Booksim.hh"


namespace gem5
{

namespace ruby
{
	class NetDest;
	class MessageBuffer;

namespace booksim
{
	class NetworkInterface;

	class BooksimNetwork: public gem5::ruby::Network
	{
		struct BooksimMessage {
			NetworkSwitch * network_switch;
			NodeID dest;
			int subnet;
			MsgPtr msg;
		};
		private:
		    std::vector<NetworkSwitch *> m_switches;
			int _number_switches;

			BooksimNetwork(const BooksimNetwork & obj);
			BooksimNetwork & operator=(const BooksimNetwork & obj);

			long m_wakeup_cycles;

			std::vector<MessageBuffer*> m_buffers_to_free;
			int m_buffer_size;

			std::vector<SwitchID> m_switchID;

		    BooksimWrapper * m_booksim_wrapper;

			std::vector<int> _retired_packets;

			//存储packet ID与message的映射，
			//并在packet到达目的地时将message发送给目的地
			std::map<int, BooksimMessage> m_packet_map;

			void RetirePackets()
			{
				RetiredPacket rp;
				rp.pid = -1;
				do{
				    rp = m_booksim_wrapper->RetirePacket();
					if(rp.pid > -1){
						updatePacketStats(rp.plat, rp.nlat, rp.hops, rp.psize);
						enqueueBooksimMessage(rp.pid);
					}
				}while(rp.pid != -1);
			}

			void incTotalCycles()
			{
				total_cycles++;
			}

			void updatePacketStats(int p_lat, int n_lat, int hops, int packet_size)
			{
				total_packet_lat += p_lat;
				total_network_lat += n_lat;
				total_hops += hops;
				total_accept_flits += packet_size;
				total_accept_packets++;
			}

			
		public:
		    typedef BooksimNetworkParams Params;

			BooksimNetwork(const Params & p);
			~BooksimNetwork();

			int GeneratePacket(int source, int dest, int size, int cl,
		                       long long time)
			{
				return m_booksim_wrapper->GeneratePacket(source,
				                                         dest,
														 size,
														 cl,
														 time);
			}

			void RunCycles(int cycles);

			bool CheckInFlightPackets()
			{
				return m_booksim_wrapper->CheckInFlightPackets();
			}

			void init();

			void printStats(std::ostream & out) const;
			void clearStats();
			void printConfig(std::ostream & out) const;
			void reset();
			void print(std::ostream & out) const;

			int getNumNodes() { return m_nodes; }

			//Topology使用以下方法建立网络

			void makeExtOutLink(SwitchID src, NodeID dest, BasicLink* link,
			                    std::vector<NetDest>& routing_table_entry);
			void makeExtInLink(SwitchID src, NodeID dest, BasicLink* link,
			                   std::vector<NetDest>& routing_table_entry);
			void makeInternalLink(SwitchID src, SwitchID dest, BasicLink *link,
			                      std::vector<NetDest>& routing_table_entry,
								  PortDirection src_outport_dirn,
								  PortDirection dest_inport_dirn);
			
			void collateStats();
			void regStats();

			bool functionalRead(Packet* pkt);
			uint32_t functionalWrite(Packet* pkt);

			std::vector<std::vector<MessageBuffer *>>* GetInBuffers()
			{
				return &m_toNetQueues;
			}
			std::vector<std::vector<MessageBuffer *>>* GetOutBuffers()
			{
				return &m_fromNetQueues;
			}

			/*
			functionalRead/Write
			写total inject packet和total accept packet
			*/
			gem5::Stats::Scalar total_packet_lat;
			gem5::Stats::Scalar total_network_lat;
			gem5::Stats::Scalar total_hops;
			gem5::Stats::Scalar total_cycles;
			gem5::Stats::Scalar total_inject_flits;
			gem5::Stats::Scalar total_accept_flits;
			gem5::Stats::Scalar total_inject_packets;
			gem5::Stats::Scalar total_accept_packets;
			gem5::Stats::Formula avg_plat;
			gem5::Stats::Formula avg_nlat;
			gem5::Stats::Formula avg_throughput;
			gem5::Stats::Formula avg_hops;
			gem5::Stats::Formula avg_packet_size;
			gem5::Stats::Formula avg_inject_flits;
			gem5::Stats::Formula avg_inject_packets;
			

			void updateInjectStats(int packet_size){
				total_inject_flits += packet_size;
				total_inject_packets++;
			}

			MachineID getSwitchID(NodeID node);

			SwitchID TranslateSwitchID(NodeID ID)
			{
				return m_switchID[ID];
			}

			NetworkSwitch* GetSwitchPtr(int ID)
			{
				return m_switches[ID];
			}

			int GetNumSwitches() {return m_switches.size();}

			//查看和设置booksim上一次运行的周期
			Tick getLastWakeupCycle(){return m_wakeup_cycles;}
			void setLastWakeupCycle(Tick cycle){m_wakeup_cycles = cycle;}

			//设置packet与message的映射
			void putBooksimMessage(NetworkSwitch * switch_ptr,
			                       int pid,
								   NodeID destID,
								   int subnet,
								   MsgPtr msg,
								   int packet_dest)
			{
				BooksimMessage message = {GetSwitchPtr(packet_dest),
				                          destID,
										  subnet,
										  msg};
				m_packet_map[pid] = message;
			}
			
			//将packet对应的message取出，发送给dest
			void enqueueBooksimMessage(int pid)
			{
				BooksimMessage message = m_packet_map[pid];
				if(message.network_switch != nullptr)
				{
					message.network_switch->EnqueueMessage(message.dest,
					                                       message.subnet,
														   message.msg);
				}
				m_packet_map.erase(pid);
			}




	};

	std::ostream & operator<<(std::ostream & out, const BooksimNetwork & obj);


	extern inline std::ostream &
	operator<<(std::ostream & out, const BooksimNetwork & obj)
	{
		obj.print(out);
		out<<std::flush;
		return out;
	}
}

}

}
#endif