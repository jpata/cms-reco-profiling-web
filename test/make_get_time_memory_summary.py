import os
import yaml
import Log_check

data_path = '/eos/cms/store/user/cmsbuild/profiling/data/'
result_path = '/eos/project/c/cmsweb/www/reco-prof/results/Time_Mem_Summary/'
Log = Log_check.TimeMem()

yaml_file = yaml.load(open('test.yaml','r'))
for step in ['step3','step4']:
	for cmssw in yaml_file:
		for workflow in yaml_file[cmssw]["workflow"]:
			gcc = yaml_file[cmssw]['gcc']
			file_path = data_path + "{0}/{1}/{2}/{3}_TimeMemoryInfo.log".format(cmssw,gcc,workflow,step)
			if os.path.isfile(file_path):
				Log.Get_TimeMem(file_path)
				Log.summary(result_path+"{0}/{1}/{2}/{3}.txt".format(cmssw,gcc,workflow,step))
