#! /usr/bin/env python3

import os

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
