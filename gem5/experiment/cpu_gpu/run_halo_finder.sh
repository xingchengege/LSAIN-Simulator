docker run --rm -v $PWD:$PWD -w $PWD -u $UID:$GID halo_finder_image  \
       build/GCN3_X86/gem5.opt \
	   --debug-flag=Booksim \
	   -d experiment_out/cpu_gpu_1/halo_finder/halo_finder_result_p100dgx1 \
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
	   --benchmark-root=gem5-resources/src/gpu/halo-finder/src/hip -cForceTreeTest \
	   --options="0.5 0.1 64 0.1 1 N 12 rcb"



docker run --rm -v $PWD:$PWD -w $PWD -u $UID:$GID halo_finder_image  \
       build/GCN3_X86/gem5.opt \
	   -d experiment_out/cpu_gpu_1/halo_finder/halo_finder_result_v100dgx1 \
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
	   --benchmark-root=gem5-resources/src/gpu/halo-finder/src/hip -cForceTreeTest \
	   --options="0.5 0.1 64 0.1 1 N 12 rcb"

