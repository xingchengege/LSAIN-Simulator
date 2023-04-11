/*
Booksim网络的Interface
*/
#include "mem/ruby/network/booksim/src/trafficmanager_wrapper.hpp"
#include "mem/ruby/network/booksim/src/booksim_config.hpp"
#ifndef __BOOKSIM_WRAPPER_HH_
#define __BOOKSIM_WRAPPER_HH_
namespace gem5{
namespace ruby{
namespace booksim{
	
	class TrafficManagerWrapper;
	struct RetiredPacket{
			   long pid; // packet ID
			   int src; // source
			   int dest; // destination
			   int cl; //packet class
			   int psize; // packet size
			   int plat; // packet latency
			   int nlat; //network latency
			   int hops; // number of hops done
		   };
	class BooksimWrapper
	{
		private:
		   TrafficManagerWrapper *_traffic_manager;
		   std::vector<RetiredPacket> _retired_packets; 
		public:
		   BooksimWrapper(std::string const & config_flie);
		   virtual ~BooksimWrapper();

		   //生成一个packet，并返回其ID
		   long GeneratePacket(int source, int dest, int size, int cl,
		                       long long time);

			//运行cycles个内部周期
			void RunCycles(const unsigned int cycles);

			//返回所有弹出队列中的packets
			std::vector<RetiredPacket>& RetirePackets();

			//查看网络中是否还有剩余flits
			bool CheckInFlightPackets();

			//查看网络中是否还有剩余credits
			bool CheckInFlightCredits();

			//查看注入队列的剩余大小
			int CheckInjectionQueue(int source, int cl);

			//更新周期计数
			void UpdateSimTime(int cycles);

			//打印数据，更新截止到当前的数据并打印它们
			void PrintStats(std::ostream & os);

			//打印配置文件
			void PrintConfig(std::ostream & os);

			//重置数据
			void ResetStats();

			//获取模拟的时间
			long GetSimTime();

	};
}	
}
}

#endif