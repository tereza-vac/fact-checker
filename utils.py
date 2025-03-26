
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def measure_latency(start_time):
    return time.time() - start_time

def calculate_relevance(tvrzeni, odpoved):
    corpus = [tvrzeni, odpoved]
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()
    similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return similarity
