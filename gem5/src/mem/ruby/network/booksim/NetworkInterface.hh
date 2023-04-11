
#ifndef __MEM_RUBY_NETWORK_BOOKSIM_NETWORKINTERFACE_HH__
#define __MEM_RUBY_NETWORK_BOOKSIM_NETWORKINTERFACE_HH__

#include "mem/ruby/common/Consumer.hh"


#include "mem/ruby/network/MessageBuffer.hh"

namespace gem5
{

namespace ruby
{

namespace booksim
{
	class NetworkSwitch;
	class BooksimNetwork;

	class NetworkInterface : public Consumer
	{
		public:
		    static bool trigger_wakeup;
			NetworkInterface(SwitchID sid, NetworkSwitch *sw, uint32_t virt_nets);
			~NetworkInterface();

			void init(BooksimNetwork* network_ptr);

			void wakeup();

			void addInPort(const std::vector<MessageBuffer*>& in);

			void RegisterMessageBuffers(
				    std::vector<std::vector<MessageBuffer*>> *in,
					std::vector<std::vector<MessageBuffer*>> *out);
			
			void clearStats();
			void collateStats();
			void print(std::ostream& out) const;

		private:
		    SwitchID m_switch_id;
			NetworkSwitch * const m_switch;

			std::vector<std::vector<MessageBuffer*> > m_in;
			std::vector<std::vector<MessageBuffer*> > m_out;
			uint32_t m_virtual_networks;

			BooksimNetwork * m_wrapper_ptr;

			int m_next_report_time;

			std::vector<int> m_pending_message_count;
	};
}

}

}

#endif