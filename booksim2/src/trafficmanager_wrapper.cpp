
#include "trafficmanager_wrapper.hpp"

namespace gem5{
namespace ruby{
namespace booksim
{
	TrafficManagerWrapper::TrafficManagerWrapper(const Configuration &config,
	                                             const vector<Network *> &net
												 )
		: TrafficManager(config, net)
	{
		_ejection_queue.resize(_classes);
		for(int cl=0; cl < _classes; cl++)
		{
			_ejection_queue[cl].resize(_nodes);
		}

		_last_print = 0;
		_sim_state = running;
	}

	TrafficManagerWrapper::~TrafficManagerWrapper()
	{

	}

	long
	TrafficManagerWrapper::GeneratePacket(int source,
	                                      int dest,
										  int size,
										  int cl,
										  long long time)
	{
		// cout<<"TrafficManagerWrapper: GeneratePacket!"<<endl;
		return _GeneratePacket(source, dest, size, cl, GetSimTime() - time);
	}
	
	void
	TrafficManagerWrapper::_RetirePacket(Flit * head, Flit *tail)
	{
		TrafficManager::_RetirePacket(head, tail);
		_ejection_queue[head->cl][head->dest].push(make_pair(*head, *tail));
	}

	void 
	TrafficManagerWrapper::RunCycles(int cycles)
	{
		for(int i = 0; i < cycles; i++){
			_Step();
		}
		if(_print_csv_results && _sample_period < GetSimTime() - _last_print)
		{
			std::cout<< "Cur PID: " << _cur_pid << std::endl;
			UpdateStats();
			_UpdateOverallStats();
			DisplayOverallStats();
			_ClearStats();

			_last_print = GetSimTime();
		}
	}

	bool
	TrafficManagerWrapper::CheckInFlightPackets()
	{
		bool in_flight_packets = false;
		for(int cl=0; cl < _classes; cl++)
		{
			in_flight_packets |= !_total_in_flight_flits[cl].empty();

			if(in_flight_packets)
				break;

			for(int n = 0; n < _nodes; n++){
				in_flight_packets |= ! _ejection_queue[cl][n].empty();
				if(in_flight_packets)
				   break;
			}
		}
		return in_flight_packets;
	}

	std::pair<Flit,Flit>
	TrafficManagerWrapper::RetirePacket()
	{
		for(int cl = 0; cl < _classes; cl++)
		{
			for(int n = 0; n < _nodes; n++)
			{
				if(!_ejection_queue[cl][n].empty())
				{
					pair<Flit, Flit> rp = _ejection_queue[cl][n].front();

					_ejection_queue[cl][n].pop();

					return rp;
				}
			}
		}
		Flit head = Flit();
		head.pid = -1;
		return make_pair(head, head);
	}

	void
	TrafficManagerWrapper::UpdateSimTime(int cycles)
	{
		_time += cycles;
		assert(_time);
	}

	int
	TrafficManagerWrapper::CheckInjectionQueue(int source, int cl)
	{
		int cur_occupancy;
		cur_occupancy = _partial_packets[source][cl].size();
		return _inj_size - cur_occupancy;
	}

	void
	TrafficManagerWrapper::ClearStats()
	{
		TrafficManager::_ClearStats();
	}

	
}
}
}