import json
import pprint
import collections
import operator
import random
def states_data(data, labels):
	raw_states_count = collections.defaultdict(lambda: 0)
	states_count_by_topic = {'fairbusiness':collections.defaultdict(lambda: 0), 
	'freegov':collections.defaultdict(lambda: 0), 'ideafreedom':collections.defaultdict(lambda: 0),
	'formletters':collections.defaultdict(lambda: 0)}

	total_count = 0;
	topics_count = collections.defaultdict(lambda: 0)
	for i, obj in enumerate(data):
		state = obj['stateCd']
		if (state is None):
			state = "NOT_SPECIFIED"
		raw_states_count[state] = raw_states_count[state] + 1
		total_count+=1

		for topic in ["fairbusiness", "freegov", "ideafreedom"]:
			v = 0;
			if topic == "fairbusiness":
				v = labels[0][i]
			if topic == "freegov":
				v = labels[1][i]
			if topic == "ideafreedom":
				v = labels[2][i]
			if v:
				topics_count[topic] = topics_count[topic] + 1
				states_count_by_topic[topic][state] = states_count_by_topic[topic][state] + 1

		v = labels[4][i] #Labels for the form letters tag
		if v:
			topics_count["formletters"] = topics_count["formletters"] + 1;
			states_count_by_topic["formletters"][state] = states_count_by_topic["formletters"][state] + 1; 		

	print "Total number of comments:", len(data)
	print "Total count of topic tags: ", topics_count

	for key in sorted(raw_states_count):
		raw_states_count[key]/=(float)(total_count)

	for count in states_count_by_topic:
		for key in sorted(states_count_by_topic[count]):
			states_count_by_topic[count][key]/=(float)(topics_count[count])

	raw_states_count_sorted = sorted(raw_states_count.items(), key=operator.itemgetter(1))

	print "Total"
	for key, value in reversed(raw_states_count_sorted):
		print key, value
	
	print "\n\n"
	for count in states_count_by_topic:
		print count
		count_sorted = sorted(states_count_by_topic[count].items(), key=operator.itemgetter(1))
		for key, value in reversed(count_sorted):
			print key, value

		print "\n\n"



def print_text(label_vec, topic, data):
	f = open(topic + "_text", 'w');
	texts = []
	for idx in range(len(label_vec)):
		if label_vec[idx]:
			texts.append(data[idx])

	rand_smpl = [ texts[i] for i in sorted(random.sample(xrange(len(texts)), 100)) ]

	json.dump(rand_smpl, f, sort_keys=True, indent=4, separators=(',', ': '))


labeled_data = json.loads(open("labeled_data_all_shuffled.json").read())

unlabeled_data = json.loads(open("data_all_800000.json").read())
predicted_labels = json.loads(open("results_data_all_800000.json").read())
# print "##################################################################"
# print "state stats for labeled data\n"
# states_data(labeled_data);

# print "##################################################################"
print "state stats for unlabeled data\n"
#states_data(unlabeled_data, predicted_labels);
freebiz = predicted_labels[0]
freegov = predicted_labels[1]
idea = predicted_labels[2]

print_text(freegov, "freegov", unlabeled_data);
print_text(freebiz, "fairbusiness", unlabeled_data);
print_text(idea, "ideafreedom", unlabeled_data);

# print len(freebiz)
# print "freegov+freebiz", [x + y for x, y in zip(freebiz, freegov)].count(2)
# print "idea+freebiz", [x + y for x, y in zip(freebiz, idea)].count(2)
# print "freegov+idea", [x + y for x, y in zip(idea, freegov)].count(2)

# print "all", [x + y + z for x, y, z in zip(freebiz, freegov, idea)].count(3)
# print "none", [x + y + z for x, y, z in zip(freebiz, freegov, idea)].count(0)
