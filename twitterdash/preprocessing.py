import re
import os
from time import time
from PIL import Image
import numpy as np
from collections import Counter
from sklearn.feature_extraction import stop_words
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud

MASK_PATH = os.path.join(os.path.dirname(__file__), os.path.join("static", "img", "twitter_mask.png"))
CLOUD_PATH = os.path.join(os.path.dirname(__file__), os.path.join("static", "img"))

def process_text(tweets, query_string):
    query_string = query_string.lower()
    response = {}
    text = " ".join(tweets)
    # make all words in small letter
    text = text.lower()
    # get all hashtags
    hashtags = re.findall(r"#\w+",  text)
    hashtags = Counter(hashtags).most_common()[:6]
    response['hashtags'] = hashtags
    # remove links
    text = re.sub(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(/\S+)?|\S+\.com\S+", "", text)
    # remove the hashtags and mentions
    text = re.sub(r"#\w+|@\w+", "", text)
    # remove stop words and query word
    text = " ".join([word for word in text.split() if word not in stop_words.ENGLISH_STOP_WORDS])
    # lemitize words
    lemmatizer = WordNetLemmatizer()
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
    # remove non alpha words
    text = re.findall(r"\w{3,}", text)
    # get most common words
    words = Counter(text)
    if words.get(query_string):
        words.pop(query_string)
    response['common'] = words.most_common()[:10]
    # create the word cloud
    mask = np.array(Image.open(MASK_PATH))
    wc = WordCloud(background_color="white", mask=mask)
    wc.generate_from_frequencies(words)
    # create new cloud image
    image_name = "twitter_cloud_"+str(int(time()))+".png"
    image_path = os.path.join(CLOUD_PATH, image_name)
    wc.to_file(image_path)
    response['cloud_sign'] = image_name

    return response
