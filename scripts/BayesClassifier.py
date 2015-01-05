import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import LinearSVC
from random import shuffle

##CONSTANTS
NUM_FOLDS = 10

json_data = json.loads(open("labeled_data_all_shuffled.json").read())

subset_size = len(json_data)/NUM_FOLDS
generalized_error = [0.0,0.0,0.0,0.0,0.0]
labels = ['fair business','free gov', 'idea freedom', 'personal', 'form letter']


for i in range(NUM_FOLDS):
	testing_data = json_data[i*subset_size:][:subset_size]
	training_data = json_data[:i*subset_size] + json_data[(i+1)*subset_size:]

	comments_train = []
	comments_test = []

	fair_business_training_labels = []
	fair_business_testing_labels = []

	free_gov_training_labels = []
	free_gov_testing_labels = []

	idea_freedom_training_labels = []
	idea_freedom_testing_labels = []

	personal_training_labels = []
	personal_testing_labels = []

	form_letter_training_labels = []
	form_letter_testing_labels = []

	for obj in training_data:
		comments_train.append(obj['text'])
		fair_business_training_labels.append(obj['topiclabels']['fairbusiness'])
		free_gov_training_labels.append(obj['topiclabels']['freegov'])
		idea_freedom_training_labels.append(obj['topiclabels']['ideafreedom'])
		personal_training_labels.append(obj['personal'])
		form_letter_training_labels.append(obj['formletter'])
	for obj in testing_data:
		comments_test.append(obj['text'])
		fair_business_testing_labels.append(obj['topiclabels']['fairbusiness'])
		free_gov_testing_labels.append(obj['topiclabels']['freegov'])
		idea_freedom_testing_labels.append(obj['topiclabels']['ideafreedom'])
		personal_testing_labels.append(obj['personal'])
		form_letter_testing_labels.append(obj['formletter'])

	count_vect = CountVectorizer(stop_words = 'english', ngram_range = (1,2), strip_accents = 'unicode', min_df = 1, max_df = 0.7)
	tfidf_transformer = TfidfTransformer(smooth_idf = True, use_idf = True)

	X_train_counts = count_vect.fit_transform(comments_train)
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

	X_test_counts = count_vect.transform(comments_test)
	X_test_tfidf = tfidf_transformer.transform(X_test_counts)

	training_labels = [fair_business_training_labels, free_gov_training_labels, idea_freedom_training_labels, personal_training_labels, form_letter_training_labels]
	testing_labels = [fair_business_testing_labels, free_gov_testing_labels, idea_freedom_testing_labels, personal_testing_labels, form_letter_testing_labels]

	print "Cross Validation", i
	for label in range(len(training_labels)):
		#Fit model
		clf = BernoulliNB(alpha=1.0, binarize=0.0, class_prior=None, fit_prior=True)
		clf.fit(X_train_tfidf, training_labels[label])

		predicted = clf.predict(X_test_tfidf)

		num_correct = 0.0
		num_total = len(predicted)
		for index in range(len(predicted)):
			if predicted[index] == testing_labels[label][index]:
				num_correct += 1

		# print labels[label], num_correct/num_total
		generalized_error[label] += num_correct/num_total

generalized_error = [x/NUM_FOLDS for x in generalized_error]
print labels
print generalized_error

