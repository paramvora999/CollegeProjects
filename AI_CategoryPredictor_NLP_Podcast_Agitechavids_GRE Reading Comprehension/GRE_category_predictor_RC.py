#Testing current code sample with an sklearn dataset for general purpose application. Used locally for Agitechavids Project and testing GRE Reading Comprehension passages.

from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# Defining an arbitrary category map
category_mapping = {'talk.politics.misc': 'Politics', 'rec.autos': 'Autos', 
        'rec.sport.hockey': 'Hockey', 'sci.electronics': 'Electronics', 
        'sci.med': 'Medicine', 'rec.sport.basketball': 'Basketball'}

training_data = fetch_20newsgroups(subset='train', 
        categories=category_mapping.keys(), shuffle=True, random_state=5)

# Building a count vectorizer and extracting term counts 
count_vectorizer = CountVectorizer()
train_tcount = count_vectorizer.fit_transform(training_data.data)

# Creating the tf-idf transformer
tfidf = TfidfTransformer()
train_tfidf = tfidf.fit_transform(train_tcount)

# Defining test data (Replaced with .txt file for Podcasts or a Reading Passage)
input_passage = [
    'You need to be careful with cars when you are driving on slippery roads', 
    'A lot of devices can be operated wirelessly',
    'Players need to be careful when they are close to goal posts',
    'Political debates help us understand the perspectives of both sides',
    'An electrical component is necessary to run this application',
    'Lebron James is arguably one of the best basketball players in the NBA'
]

# Training a Multinomial Naive Bayes classifier
classifier = MultinomialNB().fit(train_tfidf, training_data.target)

input_tcount = count_vectorizer.transform(input_passage)

# Transforming vectorized data using tfidf transformer
input_tfidf = tfidf.transform(input_tcount)

# Predicting the output categories
predictions = classifier.predict(input_tfidf)

for sent, category in zip(input_data, predictions):
    print('\nInput:', sent, '\nPredicted category:', \
            category_mapping[training_data.target_names[category]])

