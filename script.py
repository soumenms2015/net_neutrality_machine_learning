import json
from pprint import pprint

##CONSTANTS
NUM_FOLDS = 10


# turns unicode objects to strings(easier to work with)
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


json_data=open('labeled_data_all_final.json')
data = byteify(json.load(json_data))

#verify
pprint(data[0])
json_data.close()


subset_size = len(data)/num_folds
accuracy = []

for i in range(NUM_FOLDS):
    testing_this_round = data[i*subset_size:][:subset_size]
    training_this_round = data[:i*subset_size] + training[(i+1)*subset_size:]

    # train using training_this_round with whatever algorithm
    # train(training_this_round)

    # evaluate against testing_this_round with algorithm
    # curr_accuracy = evaluate(testing_this_round)

    # save accuracy
    # accuracy.append(curr_accuracy)


# find mean accuracy over all rounds
# mean = sum(accuracy)/NUM_FOLDS
