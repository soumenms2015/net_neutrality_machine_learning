import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn import metrics
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

	training_labels = [fair_business_training_labels, free_gov_training_labels, idea_freedom_training_labels, personal_training_labels, form_letter_training_labels]
	testing_labels = [fair_business_testing_labels, free_gov_testing_labels, idea_freedom_testing_labels, personal_testing_labels, form_letter_testing_labels]

	precision = [0, 0, 0, 0, 0];
	accuracy = [0, 0, 0, 0, 0];

	print "Cross Validation", i
	for label in range(len(training_labels)):

		text_clf = Pipeline([('vect', CountVectorizer(stop_words = 'english', ngram_range = (1,2), strip_accents = 'unicode', min_df = 2, max_df = 0.7)),
			       ('tfidf', TfidfTransformer(smooth_idf = True, use_idf = True)),
                   ('clf', LinearSVC(penalty='l2', loss='l1', dual=True, tol=0.0001, C=10.0))])
		text_clf.fit(comments_train, training_labels[label])

		predicted = text_clf.predict(comments_train)

		num_correct = 0.0
		num_total = len(predicted)
		for index in range(len(predicted)):
			if predicted[index] == training_labels[label][index]:
				num_correct += 1


		#print(metrics.classification_report(testing_labels[label], predicted, target_names=["Topic Present(1)", "Topic not Present(0)"]))
		#print(metrics.confusion_matrix(testing_labels[label], predicted))
		# precision[label]+=metrics.precision_score(testing_labels[label], predicted);
		# accuracy[label]+=metrics.accuracy_score(testing_labels[label], predicted);
		# print labels[label], num_correct/num_total
		generalized_error[label] += num_correct/num_total



generalized_error = [x/NUM_FOLDS for x in generalized_error]
print labels
print generalized_error

