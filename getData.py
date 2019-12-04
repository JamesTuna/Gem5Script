#! /usr/bin/env python3

import os
import pickle

weights = {"bzip2":[0.249573,0.176068,0.112821,0.461538],"hmmer":[0.018519,0.388889,0.203704,0.388889],"cactusADM":[0.006173,0.006173,0.376543,0.555556,0.055556],"mcf":[0.116505,0.601942,0.213592,0.067961],"sphinx3":[0.231481,0.055556,0.106481,0.259259,0.347222]}

benchMarks = ['bzip2','cactusADM','hmmer','mcf','sphinx3']
numFiles = {'bzip2':4,'cactusADM':5,'hmmer':4,'mcf':4,'sphinx3':5}


cache_size = ['128kB','256kB','512kB']
associativity = ['1','2','4']
rep_policy = ['BRRIPRP','LRURP']

os.system('mkdir extracted_data')
for bench in benchMarks:
	print("collect data for bench %s"%(bench))
	os.system('mkdir extracted_data/'+bench)
	for c_size in cache_size:
		for assoc in associativity:
			for rep in rep_policy:
				overall_cpi = 0
				overall_weight = 0
				outfile = open('extracted_data/'+bench+'/'+c_size+'_'+assoc+'_'+rep+'.txt','w')
				for simID in range(numFiles[bench]):
					outfile.write('simpoint %s\n'%simID)
					fileDir = './'+bench+'/'+c_size+'_'+assoc+'_'+rep+'_simID'+str(simID)
					print("Analyse stats.txt under directory %s..."%(fileDir))
					with open (fileDir+"/"+"stats.txt") as f:
						target1 = 'system.switch_cpus.numCycles'
						target2 = 'sim_insts'
						count1 = 0
						count2 = 0
						while(True):
							line = f.readline()
							if line.startswith(target1):
								count1 += 1
								if count1 == 2:
									cycles = int(line.split()[1])
									outfile.write("\tTotal number of cycles: %s\n"%cycles)
							elif line.startswith(target2):
								count2 += 1
								if count2 == 2:
									insts = int(line.split()[1])
									outfile.write("\tTotal number of instructions: %s\n"%insts)
							if line == '':
								break
						if count1 != 2:
							print(target1,'appears',count1,'times, program exits')
							#exit(1)
						if count2 != 2:
							print(target2,'appears',count2,'times, program exits')
							#exit(1)
						if count1==2 && count2==2:
							CPI = cycles/insts
							overall_cpi += weights[bench][simID] * CPI
							overall_weight += weights[bench]
					outfile.write('weighted_cpi:%s\n'%(overall_cpi/overall_weight))
