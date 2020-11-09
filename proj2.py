import tweepy
import statistics
import preprocessor
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from keys import key, secret_key

auth = tweepy.AppAuthHandler(key, secret_key)

def get_tweets(keyword: str):
    tweets_list = []
    for tweet in tweepy.Cursor(tweepy.API(auth).search, q = keyword, tweet_mode = 'extended', lang = 'en').items(100):
        tweets_list.append(tweet.full_text)
    return tweets_list

def format_tweets(tweets_list):
    formatted_list = []
    for tweet in tweets_list:
        formatted_list.append(preprocessor.clean(tweet))
    return formatted_list

def save_file(formatted_list):
    with open('tweets.txt', 'w') as f:
        for item in formatted_list:
            f.write("%s\n" % item)
    return

def get_sentiment(filename):
    client = language.LanguageServiceClient()

    with open(filename, 'r') as review_file:
        content = review_file.read()

    document = types.Document(
        content = content,
        type = enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document = document, encoding_type = 'UTF32')

    return annotations

def get_score(annotations):
    score = annotations.document_sentiment.score
    return score

def get_results(keyword1, keyword2, score1, score2):
    print("{} has an average sentiment score of {}.".format(keyword1, score1))
    print("{} has an average sentiment score of {}.".format(keyword2, score2))
    if(score1 > score2):
        print("Based on collected data, people seem to prefer {} over {}.\n".format(keyword1, keyword2))
    else:
        print("Based on collected data, people seem to prefer {} over {}.\n".format(keyword2, keyword1))
    return

if __name__ == '__main__':
    print("Restaurant Sentiment Comparison Tool")
    print("Enter a restaurant name:")
    keyword1 = input()
    print("Enter another restaurant name:")
    keyword2 = input()
    print("Comparing overall sentiment towards {} and {}...".format(keyword1, keyword2))
    tweets_list1 = get_tweets(keyword1)
    formatted_list1 = format_tweets(tweets_list1)
    save_file(formatted_list1)
    annotations1 = get_sentiment('tweets.txt')
    score1 = get_score(annotations1)
    tweets_list2 = get_tweets(keyword2)
    formatted_list2 = format_tweets(tweets_list2)
    save_file(formatted_list2)
    annotations2 = get_sentiment('tweets.txt')
    score2 = get_score(annotations2)
    get_results(keyword1, keyword2, score1, score2)