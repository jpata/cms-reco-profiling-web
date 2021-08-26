import re
import sys
import numpy as np
import pandas as pd

class TimeMem():

	def Get_TimeMem(self,input_data):

		matching1 = re.compile('^MemoryCheck')
		matching2 = re.compile('^TimeEvent')

		self.vsize = []
		self.rss = []
		self.event = []
		self.time = []

		with open(input_data,'r') as file:

			for i in file:

				if matching1.match(i):
					self.vsize.append(float(i.split()[4]))
					self.rss.append(float(i.split()[7]))

				if matching2.match(i):
					self.event.append(int(i.split()[1]))
					self.time.append(float(i.split()[3]))

		return pd.DataFrame({"vsize":self.vsize,"rss":self.rss,"event":self.event,"time":self.time})

	def summary(self,output_data):

		f = open(output_data,"w")
		f.write("Summary for {} events\n".format(len(self.vsize)))
		f.write("Max VSIZ {0} on evt {1} ; max RSS {2} on evt {3}\n".format(max(self.vsize),self.vsize.index(max(self.vsize))+1,max(self.rss),self.rss.index(max(self.rss))+1))
		f.write("Time av {0:0.5f} s/evt   max {1} s on evt {2}\n".format(sum(self.time)/len(self.time),max(self.time),self.time.index(max(self.time))+1))
		f.write("M1 Time av {0:0.5f} s/evt   max {1} s on evt {2}\n".format(sum(self.time[1:])/len(self.time[1:]),max(self.time[1:]),self.time.index(max(self.time[1:]))+1))
		f.write("M8 Time av {0:0.5f} s/evt   max {1} s on evt {2}".format(sum(self.time[8:])/len(self.time[8:]),max(self.time[8:]),self.time.index(max(self.time[8:]))+1))
		f.close()
