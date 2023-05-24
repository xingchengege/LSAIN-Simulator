docker run -u $UID:$GID --volume $(pwd):$(pwd) -w $(pwd) gcr.io/gem5-test/gcn-gpu:v22-0 \
       build/GCN3_X86/gem5.opt \
	   -d experiment_out/cpu_gpu_1/square_result/square_result_p100dgx1 \
	   configs/example/apu_se.py \
	   -n 4 \
	   -u 16 \
	   --num-dir=16 \
	   --ruby-clock=1GHz \
	   --mem-size=16GB \
	   --cpu-type=DerivO3CPU  \
	   --CPUClock=2.2GHz \
	   --cu-per-sqc=4 \
	   --cu-per-scalar-cache=2 \
	   --num-tccs=8 \
	   --cu-per-unit=2 \
	   --m-type=6 \
	   --network=booksim \
	   --topology=NVIDIADGX1 \
	   --booksim-speedup=4 \
	   --booksim-config=unican-util/booksim_configs/examples/nvidia_p100_dgx1.cfg \
	   -c gem5-resources/src/gpu/square/bin/square 


docker run -u $UID:$GID --volume $(pwd):$(pwd) -w $(pwd) gcr.io/gem5-test/gcn-gpu:v22-0 \
       build/GCN3_X86/gem5.opt \
	   -d experiment_out/cpu_gpu_1/square_result/square_result_v100dgx1 \
	   configs/example/apu_se.py \
	   -n 4 \
	   -u 16 \
	   --num-dir=16 \
	   --ruby-clock=1GHz \
	   --mem-size=16GB \
	   --cpu-type=DerivO3CPU  \
	   --CPUClock=2.2GHz \
	   --cu-per-sqc=4 \
	   --cu-per-scalar-cache=2 \
	   --num-tccs=8 \
	   --cu-per-unit=2 \
	   --m-type=6 \
	   --network=booksim \
	   --topology=NVIDIADGX1 \
	   --booksim-speedup=4 \
	   --booksim-config=unican-util/booksim_configs/examples/nvidia_v100_dgx1.cfg \
	   -c gem5-resources/src/gpu/square/bin/square 
