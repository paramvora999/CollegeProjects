import argparse
import json
import numpy as np

from compute_scores import pearson_score
from collaborative_filtering import find_similar_users

def build_arg_parser():
    parser = argparse.ArgumentParser(description='Let us find out what movies you can watch next !')
    parser.add_argument('--user', dest='user', required=True,
            help='Input user')
    return parser
 
# Getting the movie recommendations for the given input user
def get_recommendations(dataset, input_user):
    if input_user not in dataset:
        raise TypeError('Cannot find ' + input_user + ' your record in our database !')

    overall_score = {}
    total_similarity_score = {}

    for user in [x for x in dataset if x != input_user]:
        similarity_score = pearson_score(dataset, input_user, user)

        if similarity_score <= 0:
            continue
        
        filtered_list = [x for x in dataset[user] if x not in \
                dataset[input_user] or dataset[input_user][x] == 0]

        for item in filtered_list: 
            overall_score.update({item: dataset[user][item] * similarity_score})
            total_similarity_score.update({item: similarity_score})

    if len(overall_score) == 0:
        return ['We cannot make any recommendations just yet !']

    # Generating movie ranks by normalization 
    movie_score = np.array([[score/total_similarity_score[item], item] 
            for item, score in overall_score.items()])

     
    movie_score = movie_score[np.argsort(movie_score[:, 0])[::-1]]

    # Extracting the movie recommendations
    movie_recommendation = [movie for _, movie in movie_score]

    return movie_recommendation
 
if __name__=='__main__':
    args = build_arg_parser().parse_args()
    user = args.user

    ratings_file = 'ratings.json'

    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    print("\nMovie recommendations for " + user + ":")
    movie = get_recommendations(data, user) 
    for i, movie in enumerate(movie):
        print(str(i+1) + '. ' + movie)

