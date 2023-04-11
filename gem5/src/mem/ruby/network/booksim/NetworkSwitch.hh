#ifndef __MEM_RUBY_NETWORK_BOOKSIM_NETWORKSWITCH_HH__
#define __MEM_RUBY_NETWORK_BOOKSIM_NETWORKSWITCH_HH__

#include "mem/packet.hh"
#include "mem/ruby/slicc_interface/Message.hh"
#include "mem/ruby/common/TypeDefines.hh"
#include "mem/ruby/network/BasicRouter.hh"
#include "params/NetworkSwitch.hh"

namespace gem5
{

namespace ruby
{
	class NetDest;
	class MessageBuffer;

namespace booksim
{
	class NetworkInterface;

	class BooksimNetwork;
	
	class NetworkSwitch: public BasicRouter
	{
		public:
		    typedef NetworkSwitchParams Params;
			NetworkSwitch(const Params & p);
			~NetworkSwitch();

			void init();
			void addInPort(const std::vector<MessageBuffer*> & in);

			void addOutPort(const std::vector<MessageBuffer*> & out,
			                const std::vector<NetDest> & routing_table_entru,
							Cycles link_latency,
							int bw_multiplier);

			void resetStats();
			void collateStats();
			void regStats();

			void print(std::ostream & out) const;
			void init_net_ptr(BooksimNetwork* net_ptr)
			{
				m_wrapper_ptr = net_ptr;
			}

			void ReadMessage();

			void EnqueueMessage(int dest, int subnetwork, MsgPtr msg);
		private:
		    NetworkSwitch(const NetworkSwitch & obj);
			NetworkSwitch & operator=(const NetworkSwitch & obj);

			NetworkInterface* m_booksim_interface;
			BooksimNetwork* m_wrapper_ptr;

			std::vector<std::vector<MessageBuffer*>> m_in_buffers;
			std::vector<std::vector<MessageBuffer*>> m_out_buffers;

			// 映射目的与输出端口
			std::map<int,int> m_dest_port;

			// Round Robin
			int m_last_port;
	};
	
	inline std::ostream&
	operator<<(std::ostream& out, const NetworkSwitch& obj)
	{
		obj.print(out);
		out << std::flush;
		return out;
	}
	
} // booksim

} // ruby

} // gem5

#endif