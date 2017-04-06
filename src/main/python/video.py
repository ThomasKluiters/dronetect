import cv2
import numpy as np
import sys
import lib.image_search as image_search
import pickle

def get_sift_distances(sift_query, base):
    search = image_search.Searcher(base + '.db')
    fname = base + '_sift_vocabulary.pkl'
    # Load the vocabulary to project the features of our query image on
    with open(fname, 'rb') as f:
        sift_vocabulary = pickle.load(f)

    # Get a histogram of visual words for the query image
    image_words = sift_vocabulary.project(sift_query)
    # Use the histogram to search the database
    sift_candidates = search.query_iw('sift', image_words)
    sift_distances = [cand[0] for cand in sift_candidates][0:10]
    return sift_distances

#
def process(cap, database):
    """Processes a video capture"""

    minimal = sys.maxint
    n = -1
    while(cap.isOpened()):
        n = n + 1
        ret, frame = cap.read()
        if n % 4 != 0:
            continue

        if frame is None:
            break
        sift = cv2.SIFT()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp, desc = sift.detectAndCompute(gray, None)
        distance = min(get_sift_distances(desc, database))
        if(minimal > distance):
            minimal = distance

    return minimal < 250

