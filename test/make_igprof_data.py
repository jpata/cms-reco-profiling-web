import sqlite3
import sys
import pandas as pd
import yaml
import os

yaml_file = yaml.load(open('cgi-bin.yaml','r'))

data_path = '/eos/project/c/cmsweb/www/reco-prof/cgi-bin/data/releases'

for datatype in ['cpu_endjob','mem_live.1','mem_live.99']:
	for step in ['step3','step4']:
	        for cmssw in yaml_file:
	                for workflow in yaml_file[cmssw]["workflow"]:
				path = "{0}/{1}/{2}/{3}/{4}.sql3".format(data_path,cmssw,workflow,step,datatype)
				if os.path.isfile(path):
					csv_name = "./comp_igprof/{0}/{1}/{2}/{3}.csv".format(cmssw,workflow,step,datatype)
					
					conn = sqlite3.connect(path)
					cur = conn.cursor()
					
					cur.execute("SELECT summary.tick_period FROM summary")
					tick_period = cur.fetchone()[0]
					
					cur.execute("SELECT symbols.name, mainrows.cumulative_count FROM symbols INNER JOIN mainrows ON mainrows.symbol_id IN (symbols.id)")
					spont = cur.fetchone()
					
					cur.execute("SELECT s.name,mr.id FROM mainrows mr INNER JOIN symbols s ON s.id IN(mr.symbol_id)")
					rows = cur.fetchall()
					
					child = []
					
					for row in rows:
					
						if "doEvent" in row[0]:
							cur.execute("""SELECT sym.name,
									myself.cumulative_count,
									c.pct
								FROM children c
								INNER JOIN mainrows mr ON mr.id IN (c.parent_id)
								INNER JOIN mainrows myself ON myself.id IN (c.self_id)
								INNER JOIN symbols sym ON sym.id IN (myself.symbol_id)
								WHERE c.parent_id = %s
								ORDER BY c.from_parent_count DESC;
								""" % row[1])
					
						child += cur.fetchall()
					
					child = pd.DataFrame(child)
					child.columns = ['name','cumulative','pct']
					child['cumulative'] = child['cumulative']
					if datatype == "cpu_endjob":
						child['cumulative'] = child['cumulative']*tick_period
					child.sort_values(by=['cumulative'],axis=0,ascending=False,inplace=True)
					child['spontaneous'] = spont[1]
					if datatype == "cpu_endjob":
						child['spontaneous'] = spont[1]*tick_period 
					
					child = child[~child["name"].str.contains("edm::service::Timing::postModuleEvent")] 
					child = child[~child["name"].str.contains("edm::Event::commit_")]
					child = child[~child["name"].str.contains("edm::Event::~Event()")]
					child = child[~child["name"].str.contains("edm::Event::setProducer")]
					child = child[~child["name"].str.contains("edm::Event::setConsumer")]
					child = child[~child["name"].str.contains("edm::SystemTimeKeeper::startModuleEvent")]
					child = child[~child["name"].str.contains("edm::ModuleCallingContext::getStreamContext()")]
					child = child[~child["name"].str.contains("edm::service::MessageLogger::unEstablishModule")]
					
					child.to_csv(csv_name,index=False)
