import json, pprint, os, random
from random import shuffle

dir_list = ['14-28-RAW-Solr-1/','14-28-RAW-Solr-2/','14-28-RAW-Solr-3a/','14-28-RAW-Solr-3b/','14-28-RAW-Solr-4/','14-28-RAW-Solr-5/']
pp = pprint.PrettyPrinter(indent=4)


json_list = []
for directory in dir_list:
	for filename in os.listdir(directory):
		if '.json' not in filename: continue
	
		rand = random.uniform(0,10)
		if rand < 0.5:
			f = open(directory + filename)
			j = json.loads(f.read())
			json_list.append(j)
print len(json_list)
shuffle(json_list)
with open('data_partial_40000.txt', 'w') as outfile:
  json.dump(json_list, outfile, sort_keys=True, indent=4, separators=(',', ': '))
# pp.pprint(json_list)