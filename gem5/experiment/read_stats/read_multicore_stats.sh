



for j in {1..9}
do
    grep average_packet_latency experiment_out/multicore_out_4x4/garnet_8VC/injectionrate_0.0$j/stats.txt
done
for j in {0..9}
do
	  grep average_packet_latency experiment_out/multicore_out_4x4/garnet_8VC/injectionrate_0.1$j/stats.txt
done
for j in {0..9}
do
	  grep average_packet_latency experiment_out/multicore_out_4x4/garnet_8VC/injectionrate_0.2$j/stats.txt
done
# for j in {0..5}
# do
# 	 grep average_packet_latency experiment_out/multicore_out_2/garnet/injectionrate_0.2$j/stats.txt
# done


for j in {1..9}
do
    grep avg_plat experiment_out/multicore_out_4x4/booksim_8VC/injectionrate_0.0$j/stats.txt
done
for j in {0..9}
do
	  grep avg_plat experiment_out/multicore_out_4x4/booksim_8VC/injectionrate_0.1$j/stats.txt
done
for j in {0..9}
do
	  grep avg_plat experiment_out/multicore_out_4x4/booksim_8VC/injectionrate_0.2$j/stats.txt
done
# for j in {0..5}
# do
# 	 grep avg_plat experiment_out/multicore_out_2/booksim/injectionrate_0.2$j/stats.txt
# done


for j in {1..9}
do
    grep avg_throughput experiment_out/multicore_out_4x4/booksim_8VC/injectionrate_0.0$j/stats.txt
done
for j in {0..9}
do
	  grep avg_throughput experiment_out/multicore_out_4x4/booksim_8VC/injectionrate_0.1$j/stats.txt
done
for j in {0..9}
do
	  grep avg_throughput experiment_out/multicore_out_4x4/booksim_8VC/injectionrate_0.2$j/stats.txt
done
# for j in {0..5}
# do
# 	 grep avg_throughput experiment_out/multicore_out_2/booksim/injectionrate_0.2$j/stats.txt
# done


# for i in {1..1}
# do
#    for j in {0..9}
#    do
# 	   grep average_packet_latency experiment_out/multicore_out_2/garnet/injectionrate_0.$i$j/stats.txt
#    done
# done


#  grep average_packet_latency experiment_out/multicore_out_2/garnet/injectionrate_0.2/stats.txt


# for i in {1..1}
# do
#    for j in {0..9}
#    do
# 	   grep avg_plat experiment_out/multicore_out_2/booksim/injectionrate_0.$i$j/stats.txt
#    done
# done


#  grep avg_plat experiment_out/multicore_out_2/booksim/injectionrate_0.2/stats.txt




# for i in {1..1}
# do
#    for j in {0..9}
#    do
# 	   grep average_packet_network_latency experiment_out/multicore_out_2/garnet/injectionrate_0.$i$j/stats.txt
#    done
# done


#  grep average_packet_network_latency experiment_out/multicore_out_2/garnet/injectionrate_0.2/stats.txt




# for i in {1..1}
# do
#    for j in {0..9}
#    do
# 	   grep avg_nlat experiment_out/multicore_out_2/booksim/injectionrate_0.$i$j/stats.txt
#    done
# done


#  grep avg_nlat experiment_out/multicore_out_2/booksim/injectionrate_0.2/stats.txt



#  for i in {1..1}
# do
#    for j in {0..9}
#    do
# 	   grep avg_throughput experiment_out/multicore_out_2/booksim/injectionrate_0.$i$j/stats.txt
#    done
# done


#  grep avg_throughput experiment_out/multicore_out_2/booksim/injectionrate_0.2/stats.txt
