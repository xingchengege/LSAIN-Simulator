bash ./experiment/multicpu/run_multicpu_test.sh 0.4
bash ./experiment/cpu_gpu/run_square.sh
bash ./experiment/cpu_gpu/run_halo_finder.sh

# for i in {0..3}
# do
#    for j in {0..9}
#    do
# 	  bash ./experiment/multicpu/run_multicpu_test.sh 0.$i$j
#    done
# done
# 

bash ./experiment/cpu_gpu/run_lulesh.sh
