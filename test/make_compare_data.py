import yaml
import os
import sys

yaml_file = yaml.load(open('data.yaml','r'))
sequential_file = open('cmssw.list','r')
cmssw_list = sequential_file.readlines()

data_path = '/eos/cms/store/user/cmsbuild/profiling/data/'

if sys.argv[1] == "N03_timeDiffFromReport.sh":
	result_path = '/eos/project/c/cmsweb/www/reco-prof/results/TimeDiff/'

if sys.argv[1] == "N04_compareProducts.sh":
	result_path = '/eos/project/c/cmsweb/www/reco-prof/results/CompProd/'

for i in range(len(cmssw_list)-1):
	for step in ['step3','step4']:
		for workflow in yaml_file[cmssw_list[i].strip('\n')]["workflow"]:
			if workflow in yaml_file[cmssw_list[i+1].strip('\n')]["workflow"]:
				os.system("source ./{8} {0}{2}/{3}/{6}/{7} {0}{4}/{5}/{6}/{7} > {1}{4}/{5}/{6}/{7}.txt".format(
				data_path,result_path,
				cmssw_list[i].strip('\n'),yaml_file[cmssw_list[i].strip('\n')]['gcc'],
				cmssw_list[i+1].strip('\n'),yaml_file[cmssw_list[i+1].strip('\n')]['gcc'],
				workflow,step,sys.argv[1]))

