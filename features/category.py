from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import cPickle
import pyfscache

cache_it = pyfscache.FSCache('./cache', days=10, hours=12, minutes=30)


class Classifier(object):

	@cache_it
	def getModels(self):
		categories = cPickle.load(open('./data/categories.pkl', 'rb'))
		category_map = cPickle.load(open('./data/category_map.pkl', 'rb'))
		clf = cPickle.load(open('./data/article_classifier_model.pkl', 'rb'))

		count_vect = CountVectorizer()
		count_vect = cPickle.load(open('./data/count_vect.pkl', 'rb'))

		tfidf_transformer = TfidfTransformer()
		tfidf_transformer = cPickle.load(open('./data/tfidf_transformer.pkl', 'rb'))

		tree = cPickle.load(open('./data/tree.pkl', 'rb'))

		return categories, category_map, clf, count_vect, tfidf_transformer, tree

	def predict(self, text):
		categories, category_map = [], []
		categories, category_map, clf, count_vect, tfidf_transformer, tree = self.getModels()

		# tree.show()
		X_new_counts = count_vect.transform([text])
		X_new_tfidf = tfidf_transformer.transform(X_new_counts)

		predicted = clf.predict(X_new_tfidf)

		predictions = []
		for doc, cats in zip([text], predicted):
			if isinstance(cats, list):
				predictions += [categories[cat] for cat in cats]
			else:
				predictions.append(tree.get_node(cats).tag)

		return predictions

if __name__ == '__main__':
	clf = Classifier()
	text = 'Six Nations 2016: Wales 67-14 Italy Wales will finish second in the Six Nations after a record-breaking win over Italy. Warren Gatland team scored nine tries on their way to their biggest points total in a Championship game in Cardiff. Scrum-half Rhys Webb started the rout with the opening try within five minutes, and wing George North scored his fourth try in successive games. Dan Biggar also scored a try in a personal tally of 20 points. Replacement Ross Moriarty crossed twice as Wales won by a record margin of 53 points against the Italians - beating the 41-point mark set last year in Rome. Italy were completely outclassed, but crossed twice in the second half through scrum-half Guiglielmo Palazzini and centre Gonzalo Garcia. But for lacklustre first-half displays in the 16-16 draw with Ireland and the 25-21 loss to England, Wales could have been championship contenders. As it is, they will watch England - already crowned champions - go for a Grand Slam in Paris.'
	print clf.predict(text)
