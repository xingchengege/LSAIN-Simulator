
injectionrate=${1}

./build/Garnet_standalone/gem5.debug \
    -d experiment_out/multicore_out_4x4/booksim_8VC/injectionrate_${injectionrate} \
    configs/example/garnet_synth_traffic.py   \
    --num-cpus=16  \
    --num-dirs=16  \
	--ruby-clock=1GHz \
    --network=booksim  \
    --topology=Mesh_XY  \
    --mesh-rows=4  \
    --sim-cycles=2000000 \
    --synthetic=uniform_random  \
    --injectionrate=${injectionrate} \
    --booksim-config=unican-util/booksim_configs/examples/mesh_4x4_networks.cfg


./build/Garnet_standalone/gem5.debug \
    -d experiment_out/multicore_out_4x4/garnet_8VC/injectionrate_${injectionrate} \
    configs/example/garnet_synth_traffic.py   \
    --num-cpus=16  \
    --num-dirs=16  \
	--ruby-clock=1GHz \
    --network=garnet  \
    --topology=Mesh_XY  \
	--routing-algorithm=1 \
	--vcs-per-vnet=8 \
    --mesh-rows=4  \
    --sim-cycles=2000000 \
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



# ./build/Garnet_standalone/gem5.debug \
#     configs/example/garnet_synth_traffic.py   \
#     --num-cpus=64  \
#     --num-dirs=64  \
# 	--ruby-clock=1GHz \
# 	--network=booksim  \
# 	--topology=Mesh_XY  \
#     --mesh-rows=8  \
#     --sim-cycles=10000000 \
#     --synthetic=uniform_random  \
#     --injectionrate=0.1 \
#     --booksim-config=unican-util/booksim_configs/examples/mesh_8x8_networks.cfg


#     ./build/Garnet_standalone/gem5.debug \
#     -d m5out_1 \
#     configs/example/garnet_synth_traffic.py   \
#     --num-cpus=64  \
#     --num-dirs=64  \
# 	--ruby-clock=1GHz \
#     --network=garnet  \
#     --topology=Mesh_XY  \
# 	--routing-algorithm=1 \
# 	--vcs-per-vnet=8 \
#     --mesh-rows=8  \
#     --sim-cycles=10000000 \
#     --synthetic=uniform_random  \
#     --injectionrate=0.1

