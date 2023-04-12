
#include "mem/ruby/network/booksim/src/booksim_wrapper.hpp"
#include<iostream>
#include<fstream>
#include<sstream>
namespace gem5{
namespace ruby{
namespace booksim{

	class Stats;


	ostream * gWatchOut;
	BooksimWrapper::BooksimWrapper(std::string const & config_flie)
	{
		BookSimConfig config;
		//读取解析配置文件
		config.ParseFile(config_flie);

		//初始化路由算法、流量、注入函数
		InitializeRoutingMap(config);
		
		string watch_out_flie = config.GetStr("watch_out");

		if(watch_out_flie == ""){
			gWatchOut = NULL;
		} else if(watch_out_flie == "-"){
			gWatchOut = &cout;
		} else {
			gWatchOut = new ofstream(watch_out_flie.c_str());
		}

		//初始化网络
		vector<Network *> nets;

		int subnets = config.GetInt("subnets");
		nets.resize(subnets);
		for(int i = 0; i < subnets; i++)
		{
			ostringstream name;
			name << "network_" << i;
			nets[i] = Network::New(config, name.str());
		}

		//初始化TrafficManager
		_traffic_manager = new TrafficManagerWrapper(config, nets);
	}

	BooksimWrapper::~BooksimWrapper()
	{
		delete _traffic_manager;
	}

	long
	BooksimWrapper::GeneratePacket(int source,
	                               int dest,
								   int size,
								   int cl,
								   long long time)
	{
		return _traffic_manager->GeneratePacket(source, dest, size, cl, time);
	}

	void
	BooksimWrapper::RunCycles(const unsigned int cycles)
	{
		_traffic_manager->RunCycles(cycles);
	}

	std::vector<RetiredPacket>&
	BooksimWrapper::RetirePackets()
	{
		_retired_packets.clear();
        long pid = -1;
		do{
			pair<Flit,Flit> rp = _traffic_manager->RetirePacket();
			Flit head = rp.first;
			Flit tail = rp.second;
			RetiredPacket p = {head.pid,
			                   head.src,
							   head.dest,
							   head.cl,
							   head.packet_size,
							   (int)(tail.atime - head.ctime),
							   (int)(tail.atime - head.itime),
							   head.hops
							   };
			pid = head.pid;
			if(pid > -1)
			{
				_retired_packets.push_back(p);
			}
		}while(pid != -1);
		return _retired_packets;
	}
	
	bool
	BooksimWrapper::CheckInFlightPackets()
	{
		return _traffic_manager->CheckInFlightPackets();
	}

	bool
	BooksimWrapper::CheckInFlightCredits()
	{
		return Credit::OutStanding()!=0;
	}

	void
	BooksimWrapper::UpdateSimTime(int cycles)
	{
		assert(!CheckInFlightPackets());
		_traffic_manager->UpdateSimTime(cycles);
	}

	int
	BooksimWrapper::CheckInjectionQueue(int source, int cl)
	{
		return _traffic_manager->CheckInjectionQueue(source, cl);
	}
	
	void
	BooksimWrapper::ResetStats()
	{
		_traffic_manager->ClearStats();
	}

	void 
	BooksimWrapper::PrintStats(std::ostream & os)
	{
		_traffic_manager->UpdateStats();
		_traffic_manager->DisplayStats(os);
	}
	
	long
	BooksimWrapper::GetSimTime()
	{
		return _traffic_manager->getTime();
	}

}
}
}