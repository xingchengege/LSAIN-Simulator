
injectionrate=${1}

docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID gcr.io/gem5-test/gcn-gpu:v22-0 \
    ./build/X86_MESI_Two_Level/gem5.opt \
    -d experiment_out/multicore_out__1/booksim/injectionrate_${injectionrate} \
    configs/example/garnet_synth_traffic.py   \
    --num-cpus=64  \
    --num-dirs=4  \
	--ruby-clock=1GHz \
    --num-l2caches=64  \
    --network=booksim  \
    --topology=MeshDirCorners_XY  \
    --mesh-rows=8  \
    --sim-cycles=1000000000 \
    --synthetic=uniform_random  \
    --injectionrate=${injectionrate} \
    --booksim-config=unican-util/booksim_configs/examples/mesh_8x8_networks.cfg


docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID gcr.io/gem5-test/gcn-gpu:v22-0 \
    ./build/X86_MESI_Two_Level/gem5.opt \
    -d experiment_out/multicore_out__1/garnet/injectionrate_${injectionrate} \
    configs/example/garnet_synth_traffic.py   \
    --num-cpus=64  \
    --num-dirs=4  \
	--ruby-clock=1GHz \
    --num-l2caches=64  \
	--mem-size=8GB \
    --network=garnet  \
    --topology=MeshDirCorners_XY  \
	--routing-algorithm=1 \
	--vcs-per-vnet=8 \
    --mesh-rows=8  \
    --sim-cycles=1000000000 \
    --synthetic=uniform_random  \
    --injectionrate=${injectionrate}



# docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID gcr.io/gem5-test/gcn-gpu:v22-0 \
#     ./build/X86_MESI_Two_Level/gem5.opt \
#     -d experiment_out/multicore_out/booksim/injectionrate_1.0 \
#     configs/example/garnet_synth_traffic.py   \
#     --num-cpus=64  \
#     --num-dirs=4  \
# 	--ruby-clock=1GHz \
#     --num-l2caches=64  \
#     --network=booksim  \
#     --topology=MeshDirCorners_XY  \
#     --mesh-rows=8  \
#     --sim-cycles=400000000 \
#     --synthetic=uniform_random  \
#     --injectionrate=1.0 \
#     --booksim-config=unican-util/booksim_configs/examples/mesh_8x8_networks.cfg


# docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID gcr.io/gem5-test/gcn-gpu:v22-0 \
#     ./build/X86_MESI_Two_Level/gem5.opt \
#     -d experiment_out/multicore_out/garnet/injectionrate_1.0 \
#     configs/example/garnet_synth_traffic.py   \
#     --num-cpus=64  \
#     --num-dirs=4  \
# 	--ruby-clock=1GHz \
#     --num-l2caches=64  \
# 	--mem-size=8GB \
#     --network=garnet  \
#     --topology=MeshDirCorners_XY  \
# 	--routing-algorithm=1 \
# 	--vcs-per-vnet=8 \
#     --mesh-rows=8  \
#     --sim-cycles=1000000000 \
#     --synthetic=uniform_random  \
#     --injectionrate=0.40

# docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID gcr.io/gem5-test/gcn-gpu:v22-0 \
#     ./build/X86_MESI_Two_Level/gem5.debug \
#     -d experiment_out/multicore_out/simple \
#     configs/example/garnet_synth_traffic.py   \
#     --num-cpus=64  \
#     --num-dirs=4  \
# 	--ruby-clock=1GHz \
#     --num-l2caches=64  \
# 	--mem-size=8GB \
#     --network=simple  \
#     --topology=MeshDirCorners_XY  \
# 	--routing-algorithm=1 \
# 	--vcs-per-vnet=4 \
#     --mesh-rows=8  \
#     --sim-cycles=100000000 \
#     --synthetic=uniform_random  \
#     --injectionrate=0.1

