# bash ./experiment/multicpu/run_multicpu_test.sh 0.4
bash ./experiment/cpu_gpu/run_square.sh

# for j in {1..9}
# do
# 	  bash ./experiment/multicpu/run_multicpu_test.sh 0.0$j
# done
# for j in {0..9}
# do
# 	  bash ./experiment/multicpu/run_multicpu_test.sh 0.1$j
# done

# for j in {0..9}
# do
# 	  bash ./experiment/multicpu/run_multicpu_test.sh 0.2$j
# done
# for j in {0..9}
# do
# 	  bash ./experiment/multicpu/run_multicpu_test.sh 0.1$j
# done

# for j in {0..5}
# do
# 	  bash ./experiment/multicpu/run_multicpu_test.sh 0.2$j
# done

bash ./experiment/cpu_gpu/run_halo_finder.sh



bash ./experiment/cpu_gpu/run_lulesh.sh
