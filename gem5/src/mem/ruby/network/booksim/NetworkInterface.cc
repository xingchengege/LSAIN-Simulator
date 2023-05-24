
#include "mem/ruby/network/booksim/NetworkSwitch.hh"
#include "mem/ruby/network/booksim/NetworkInterface.hh"
#include "mem/ruby/network/booksim/BooksimNetwork.hh"

namespace gem5
{

namespace ruby
{

namespace booksim
{
	NetworkInterface::NetworkInterface(SwitchID sid, 
	                                   NetworkSwitch *sw,
									   uint32_t virt_nets)
	    : Consumer(sw), m_switch_id(sid), m_switch(sw)
	{
		m_virtual_networks = virt_nets;

		m_next_report_time = 500000;
	}

	NetworkInterface::~NetworkInterface()
	{

	}

	void
	NetworkInterface::init(BooksimNetwork* network_ptr)
	{
		m_wrapper_ptr = network_ptr;

		for(int i = 0; i < m_virtual_networks; i++)
		{
			m_pending_message_count.push_back(0);
		}
	}
	
	void
	NetworkInterface::addInPort(const std::vector<MessageBuffer*> & in)
	{
		NodeID port = m_in.size();
		m_in.push_back(in);

		for(int i = 0; i < in.size(); i++)
		{
			if(in[i] != nullptr)
			{
				in[i]->setConsumer(this);
				in[i]->setIncomingLink(port);
				in[i]->setVnet(i);
			}
		}
	}

	void
	NetworkInterface::wakeup()
	{
		Tick current_cycle = m_switch->clockEdge();

		if(m_wrapper_ptr->getLastWakeupCycle() <= current_cycle)
		{
			m_wrapper_ptr->RunNetwork();

			if(m_wrapper_ptr->CheckInFlightPackets()){
				scheduleEvent(Cycles(1));
			}

			m_wrapper_ptr->setLastWakeupCycle(current_cycle+1);
		}
	}

	void
	NetworkInterface::RegisterMessageBuffers(
		   std::vector<std::vector<MessageBuffer*>> *in,
		   std::vector<std::vector<MessageBuffer*>> *out)
	{

	}

	void
	NetworkInterface::clearStats()
	{
		m_wrapper_ptr->clearStats();
	}

	void
	NetworkInterface::collateStats()
	{

	}

	void
	NetworkInterface::print(std::ostream& out) const
	{
		out << "[NetworkInterface " << m_switch_id << "]";
	}

} // namespace booksim
	
} // namespace ruby

} // namespace gem5