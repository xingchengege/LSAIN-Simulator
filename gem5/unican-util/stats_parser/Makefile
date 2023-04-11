CSV_FILE:=2020_01_20
OUTPUT_DIR=fig_2020_01_20
EXP_DIR=${HOME}/ATC/Tools/gem5/evaluations/2020/experiments

csv_gen:
	python stats_parser_2019_09_23.py ${EXP_DIR}/*/*/stats.txt > \
									  ${CSV_FILE}.csv

fig_gen:
	python plotter_speedup.py ${CSV_FILE}.csv style_avg_plat.json
	python plotter_speedup_log.py ${CSV_FILE}.csv style_total_flits.json
	python plotter_speedup.py ${CSV_FILE}.csv style_hops.json
	python plotter_speedup.py ${CSV_FILE}.csv style_host_inst_rate.json
	python plotter_speedup_normalized.py ${CSV_FILE}.csv \
									     style_host_tick_rate.json
	python plotter_speedup_normalized.py ${CSV_FILE}.csv style_ipc.json
	python plotter_speedup_log.py ${CSV_FILE}.csv style_miss_lat.json
	mkdir ${OUTPUT_DIR}
	#mv ${CSV_FILE}*.pdf ${OUTPUT_DIR}
	mv *.pdf ${OUTPUT_DIR}

move_fig:
	#mv ${CSV_FILE}*.pdf ${OUTPUT_DIR}
	mv *.pdf ${OUTPUT_DIR}


clean_fig:
	rm -rf ${OUTPUT_DIR}
