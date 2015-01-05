import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn import metrics
from random import shuffle


training_data = json.loads(open("labeled_data_all_shuffled.json").read())
labels = ['fair business','free gov', 'idea freedom', 'personal', 'form letter']

comments_train = []

fair_business_training_labels = []

free_gov_training_labels = []

idea_freedom_training_labels = []

personal_training_labels = []

form_letter_training_labels = []

for obj in training_data:
	comments_train.append(obj['text'])
	fair_business_training_labels.append(obj['topiclabels']['fairbusiness'])
	free_gov_training_labels.append(obj['topiclabels']['freegov'])
	idea_freedom_training_labels.append(obj['topiclabels']['ideafreedom'])
	personal_training_labels.append(obj['personal'])
	form_letter_training_labels.append(obj['formletter'])



training_labels = [fair_business_training_labels, free_gov_training_labels, idea_freedom_training_labels, personal_training_labels, form_letter_training_labels]

#Processing of the unlabeled data is here
unlabeled_data = json.loads(open("data_all_800000.json").read())
comments_unlabeled = []
for obj in unlabeled_data:
	comment = obj['text']
	if comment != None:
		comments_unlabeled.append(obj['text'])
	else:
		comments_unlabeled.append("")

predicted_labels = []

for label in range(len(training_labels)):
	print "Getting optimized parameters for:", labels[label], "..."
	#Put your desired classifer here
	text_clf = Pipeline([('vect', CountVectorizer(stop_words = 'english', strip_accents = 'unicode', max_df = 0.7)),
		       ('tfidf', TfidfTransformer(smooth_idf = True)),
               ('clf', SVC(C=100.0, kernel='rbf', gamma=0.5, tol=0.001))])

	# Usage: use the name of the component, double underdash, then the name of the parameter, with its possible values
	parameters = {
					'vect__ngram_range': [(1, 1), (1, 2)],
					'vect__min_df': (1, 2),
					'tfidf__use_idf': (True, False),
					'clf__gamma': (0.3, 0.7),
					'clf__C': (1, 5)
					}

	gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
	gs_clf = gs_clf.fit(comments_train, training_labels[label])

	#Get and Print Best Parameters For Each Label
	best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
	print score
	for param_name in sorted(parameters.keys()):
	    print("%s: %r" % (param_name, best_parameters[param_name]))


	# print ""
	# print "Using parameters above, running the classifer on data of size ", len(comments_unlabeled)

	# predicted = gs_clf.predict(comments_unlabeled)
	# print "number of comments with topic ", labels[label], ":", sum(predicted)
	# predicted_labels.append(predicted.tolist()); 


# #Write to a file called results
# with open('results_data_all_800000.txt', 'w') as outfile:
#   json.dump(predicted_labels, outfile, sort_keys=True, indent=4, separators=(',', ': '))

