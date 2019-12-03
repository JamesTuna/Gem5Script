#! /usr/bin/env python3

import os

benchMarks = ['bzip2','cactusADM','hmmer','mcf','sphinx3']

numFiles = {'bzip2':4,'cactusADM':5,'hmmer':4,'mcf':4,'sphinx3':5}

numBenches = 5

args = {'bzip2':'dryer.jpg','cactusADM':'benchADM.par','hmmer':'bombesin.hmm','mcf':'inp.in','sphinx3':'ctlfile . args.an4'}

EMU = '/home/james/Desktop/gem5/build/X86/gem5.opt'
TUNE = 'base'
EXT = 'amd64-ee382n1'
CHKPT_DIR = '/home/james/Desktop/bench_backup/bench/'
FULL_EXT = TUNE + '.' + EXT
SYSCFG = '/home/james/Desktop/gem5/configs/example/se.py'

cache_size = ['128kB','256kB','512kB','1024kB']
associativity = ['1','2','4','8']
rep_policy = ['rrip']

for bench in benchMarks:
	os.system('mkdir ' + bench)
	for c_size in cache_size:
		for assoc in associativity:
			for rep in rep_policy:
				for simID in range(numFiles[bench]):
					outDir = './'+bench+'/'+c_size+'_'+assoc+'_'+rep+'_simID'+str(simID)
					ckptdir = CHKPT_DIR + bench + '.m5out'
					cmd = [EMU,'-d',SYSCFG,'--caches','--l2cache','--l2_size='+c_size]
					cmd += ['--l2_assoc='+assoc,'--l2tag='+rep,'--checkpoint-dir',ckptdir]
					cmd += ['--restore-simpoint-checkpoint']
					cmd += ['-r',str(simID+1),'--restore-with-cpu=DerivO3CPU']
					cmd += ['-c','/home/james/Desktop/bench/'+bench+'_'+FULL_EXT]
					cmd += ['-o','/home/james/Desktop/bench/'+args[bench]]
					print('-------------------------------------------')
					print('c_size',c_size,'assoc',assoc,'policy',rep)
					print('-------------------------------------------')
					print(' '.join(cmd))
