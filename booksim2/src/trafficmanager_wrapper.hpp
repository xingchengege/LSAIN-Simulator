/*
TrafficManager的Interface
*/
#ifndef _TRAFFICMANAGER_WRAPPER_HPP_
#define _TRAFFICMANAGER_WRAPPER_HPP_

#include "trafficmanager.hpp"
namespace gem5{
namespace ruby{
namespace booksim{

	class TrafficManagerWrapper : public TrafficManager
	{
		protected:
		   //Pure virtual method used to generate packets.
		   //在这里packet被从Booksim外部注入
		   virtual void _Inject() {}
		   // Pure virtual method called by Run() in main.cpp
		   virtual bool _SingleSim() { return true; } 	   
	    
		private:
		    vector<vector<queue<pair<Flit,Flit>>>> _ejection_queue;

			virtual void _RetirePacket(Flit *head, Flit *tail);

			long _sameple_period;

			long _last_print;

		public:
		   TrafficManagerWrapper(const Configuration &config,
		                         const vector<Network *> &net
								 );
		   ~TrafficManagerWrapper();

		   //TrafficManager的Interface
		   //向Booksim内部注入流量
		   long GeneratePacket(int source, 
		                       int dest,
							   int size,
							   int cl,
							   long long time);
			//操控Booksim网络运行指定周期
			void RunCycles(int cycles);
			//查看网络中是否有剩余的packet
			bool CheckInFlightPackets();
			//查看输入队列空闲数量
			int CheckInjectionQueue(int source, int cl);
			//获取收到的Packet
			std::pair<Flit,Flit> RetirePacket();
			//更新周期计数
			void UpdateSimTime(long long cycles);
	        //清空网络数据
			void ClearStats();

	};
}
}
}


#endif