#include <numeric>
#include "base/cast.hh"
#include "mem/ruby/network/booksim/NetworkSwitch.hh"
#include "mem/ruby/network/booksim/NetworkInterface.hh"
#include "mem/ruby/network/booksim/BooksimNetwork.hh"
// #include "mem/ruby/protocol/ResponseMsg.hh"
#include "debug/BooksimSwitch.hh"
namespace gem5
{

namespace ruby
{

namespace booksim
{

	NetworkSwitch::NetworkSwitch(const Params & p)
	    : BasicRouter(p)
	{
		m_booksim_interface = new NetworkInterface(m_id, this, p.virt_nets);
		m_last_port = 0;
	}

	NetworkSwitch::~NetworkSwitch()
	{
		delete m_booksim_interface;
	}

	void 
	NetworkSwitch::init()
	{
		BasicRouter::init();
		m_booksim_interface->init(m_wrapper_ptr);
	}

	void
	NetworkSwitch::addInPort(const std::vector<MessageBuffer*>& in)
	{
		m_booksim_interface->addInPort(in);
		m_in_buffers.push_back(in);
	}

	void
	NetworkSwitch::addOutPort(const std::vector<MessageBuffer*>& out,
	                          const std::vector<NetDest>& routing_table_entry,
							  Cycles link_latency,
							  int bw_multiplier)
	{
		m_out_buffers.push_back(out);

		std::vector<NetDest> dest_tables = routing_table_entry;

		std::vector<NodeID> all_dest;
		for(std::vector<NetDest>::iterator dest_table = dest_tables.begin();
		    dest_table != dest_tables.end(); dest_table++)
		{
			std::vector<NodeID> dests = dest_table->getAllDest();
			for(std::vector<NodeID>::iterator dest = dests.begin();
			    dest != dests.end(); dest++)
			{
				all_dest.push_back(*dest);
			}
		}

		for(std::vector<NodeID>::iterator dest = all_dest.begin(); 
		    dest != all_dest.end(); dest++)
		{
			m_dest_port[*dest] = m_out_buffers.size() - 1;
		}
		if(m_id == 3)
		{NodeID destID=all_dest[0];
		for(int m = 0; m < (int) MachineType_NUM; m++)
		{
			if((destID >= 
				MachineType_base_number(
					(MachineType) m)) &&
					destID < MachineType_base_number(
					(MachineType) (m+1))
										
				){
					std::cout<<"Link NodeID:"<<destID<<" MachineID: "<<(MachineID){
												    (MachineType) m, (destID -
													MachineType_base_number(
														(MachineType) m))}<<std::endl;
					// DPRINTF(Booksim, "Link NodeID: %d MachineType: %d MachineID: %d\n",
					                // NodeID, (MachineType) m, (MachineID){
									// 			    (MachineType) m, (destID -
									// 				MachineType_base_number(
									// 					(MachineType) m))});
						
					break;
				}
		}}
		// DPRINTF(Booksim, "In: ",)
	}
	//
	void
	NetworkSwitch::ReadMessage()
	{
		Tick current_time = clockEdge();

		if(m_in_buffers.size() > 0)
		{
			int port = (m_last_port + 1) % m_in_buffers.size();
			for(int i = 0; i < m_in_buffers.size(); i++)
			{
				for(int vn = 0; vn < m_in_buffers[port].size(); vn++)
				{
					if(m_in_buffers[port][vn] != nullptr)
					{
						if(m_in_buffers[port][vn]->isReady(current_time))
						{
							//获取message
							MsgPtr msg_ptr = m_in_buffers[port][vn]->peekMsgPtr();

							//生成booksim
							Message* net_msg_ptr = msg_ptr.get();
							NetDest msg_dest = net_msg_ptr->getDestination();
							std::vector<NodeID> all_dest = msg_dest.getAllDest();

							bool dequeue_msg = false;

							if(all_dest.size() == 0)
							{
								dequeue_msg = true;
							}

							int size = (int) ceil((double) m_wrapper_ptr->
							        MessageSizeType_to_int(net_msg_ptr->
									getMessageSize())*8/128);
							
							for (int dest_index = 0;
							    dest_index < all_dest.size();
								dest_index++)
							{
								MsgPtr new_msg_ptr = msg_ptr->clone();
								NodeID destID = all_dest[dest_index];

								Message* new_net_msg_ptr = new_msg_ptr.get();

								NetDest personal_dest;
								if(all_dest.size() > 1)
								{
									for(int m = 0; m < (int) MachineType_NUM; m++)
									{
										if((destID >= 
										   MachineType_base_number(
											   (MachineType) m)) &&
											   destID < MachineType_base_number(
												   (MachineType) (m+1))
										  
										  ){
											personal_dest.clear();
											personal_dest.add((MachineID){
												    (MachineType) m, (destID -
													MachineType_base_number(
														(MachineType) m))});
											new_net_msg_ptr->getDestination() = personal_dest;
											break;
										  }
									}
								}


								NodeID packet_dest = all_dest[dest_index];
								packet_dest = m_wrapper_ptr->
								    TranslateSwitchID(packet_dest);

								
								int packet_class = vn;

								Cycles inject_cycle = curCycle() - ticksToCycles(
									                        msg_ptr->getTime()
								                        ) ;
								
								// if(dynamic_cast<ResponseMsg*>(net_msg_ptr)!=nullptr&&dynamic_cast<ResponseMsg*>(net_msg_ptr)->getaddr()==26906624)
									DPRINTF(Booksim, "GeneratePacket:\n  src: %lld \n dest: %lld \n  size: %lld \n packet_class: %lld\n inject_cycle: %lld\n",
											m_id,packet_dest,size,packet_class,inject_cycle);
								long pid = -1;
								if( m_id != packet_dest){
									pid = m_wrapper_ptr->GeneratePacket(
																m_id,
																packet_dest,
																size,
																packet_class,
																inject_cycle * _internal_speedup
															);
								}
								else{
									pid = 1;
								}

								if(pid > -1)
								{
									
									msg_dest.removeNetDest(personal_dest);
									net_msg_ptr->getDestination().removeNetDest(
														personal_dest
														);
									if(m_id != packet_dest){
										m_wrapper_ptr->updateInjectStats(size);
										m_wrapper_ptr->putBooksimMessage(this,
																		pid,
																		destID,
																		vn,
																		new_msg_ptr,
																		packet_dest);
									}
									else{
										DPRINTF(BooksimSwitch,"src: %d, dest: %d, vn %d",m_id, destID, vn);
										EnqueueMessage(destID, vn, new_msg_ptr);
									}
									dequeue_msg = true;
								}
							}

							if(dequeue_msg)
							{
								m_in_buffers[port][vn]->dequeue(current_time);

								m_last_port = port;
							}
						}
					}
				}

				port = (port + 1) % m_in_buffers.size();
			}
		}
	}

	void
	NetworkSwitch::EnqueueMessage(int dest, int subnet, MsgPtr msg)
	{
		Tick current_time = clockEdge();
		int dest_port = m_dest_port[dest];
		// DPRINTF(Booksim, "msg dest is:%d \n", msg->getDestination());
		// auto net_msg_ptr = msg.get();
		// if(dynamic_cast<ResponseMsg*>(net_msg_ptr)!=nullptr&&dynamic_cast<ResponseMsg*>(net_msg_ptr)->getaddr()==26906624){
				// DPRINTF(Booksim, "AcceptPacket:\n  src: %lld \n dest: %lld \n",
									// m_id,dest);
				// if(dest==22){dest_port=m_dest_port[30];std::cout<<30<<std::endl;}
		// }
							
		m_out_buffers[dest_port][subnet]->enqueue(msg,
		                                          current_time,
												  cyclesToTicks(Cycles(1)));
	}


	void
	NetworkSwitch::resetStats()
	{
		m_booksim_interface->clearStats();
	}

	void
	NetworkSwitch::collateStats()
	{
		m_booksim_interface->collateStats();
	}

	void
	NetworkSwitch::print(std::ostream& out) const
	{
		out << "[NetworkSwitch " << m_id << "]";
	}


	void
	NetworkSwitch::regStats()
	{
		BasicRouter::regStats();
		
		
	}
			
}

}

// ruby::booksim::NetworkSwitch * NetworkSwitchParams::create() const
// {
//     return new ruby::booksim::NetworkSwitch(*this);
// }

}