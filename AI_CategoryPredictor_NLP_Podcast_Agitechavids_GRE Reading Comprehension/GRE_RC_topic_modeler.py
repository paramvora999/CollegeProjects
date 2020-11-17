from nltk.tokenize import RegexpTokenizer  
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from gensim import models, corpora

def load_data(input_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f.readlines():
            data.append(line[:-1])

    return data

# Processor function for tokenizing, removing stop words, and stemming
def control_fn(input_text):
    # Creating a regular expression tokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    stemmer = SnowballStemmer('english')

    stop_word = stopwords.words('english')
    
    token = tokenizer.tokenize(input_text.lower())

    token = [x for x in tokens if not x in stop_word]
    
    token_stemmed = [stemmer.stem(x) for x in token]

    return token_stemmed
    
if __name__=='__main__':
    data = load_data('podcast_n.txt')

    token = [process(x) for x in data]

    # Creating a dictionary based on the sentence tokens 
    dictionary_token = corpora.Dictionary(tokens)
        
    doc_term_matrix = [dictionary_token.doc2bow(token) for tokens in token]

    num_topic = 7

    # Generating the LDA model 
    ldamodel = models.ldamodel.LdaModel(doc_term_matrix, 
            num_topics=num_topic, id2word=dictionary_token, passes=50)

    for item in ldamodel.print_topics(num_topics=num_topics, num_words=num_words):
        print('\nTopic', item[0])

