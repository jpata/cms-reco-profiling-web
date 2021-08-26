import os
import yaml

data_path = '/eos/project/c/cmsweb/www/reco-prof/cgi-bin/data/releases/'
cmssw = os.listdir(data_path)

workflow = {}

for i in cmssw:
	print(i)
	a = os.listdir(data_path + i)[0]
	#workflow[i] = {"cmssw":a,"workflow":os.listdir(data_path + i + '/' +a)}
	workflow[i] = {"workflow":os.listdir(data_path + i)}
	
with open('cgi-bin.yaml','w') as f:
	yaml.dump(workflow,f)
