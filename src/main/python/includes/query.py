#!/usr/bin/env python

import argparse
import pickle
import cv2
import matplotlib.pyplot as plt
import numpy as np
import feature_extraction as ft
import sys
import image_search
import os.path
import metadata_distance 

# global variables
sift_candidates = None
harris_candidates = None
colorhist_candidates = None
geo_candidates = None


# Command line parsing is handled by the ArgumentParser object

features = ['sift', 'colorhist', 'harris', 'geo', 'all']

parser = argparse.ArgumentParser(description="Query tool to query the database created by the database tool (dbt.py). Retrieve images based on image content and metadata.")
parser.add_argument("database", help="Path to the database to execute the query on.")
parser.add_argument("query", help="Query image")
parser.add_argument("feature", help="The type of feature to get results on. Chose from "+str(features))

args = parser.parse_args()

# Get file name without extension
base = os.path.splitext(args.database)[0] 


def feature_active(name):
    """ Check if feature 'name' is active
    
    i.e. the feature has been selected via a command line option to be used for processing"""
    return (args.feature == name or args.feature == 'all')


# Starting point of the script
# =======================================

if __name__ == '__main__':
   
    print '\nMulti Media Analysis Query Tool'
    print '================================\n'
    print "Query the database with [", args.query, "] for [", args.feature, "] features..."
    db_name = args.database
    search = image_search.Searcher(db_name)
    if feature_active('sift'):
        print 'Loading SIFT vocabulary ...'
        fname = base + '_sift_vocabulary.pkl'
        # Load the vocabulary to project the features of our query image on
        with open(fname, 'rb') as f:
            sift_vocabulary = pickle.load(f)

        sift_query = ft.get_sift_features([args.query])[args.query]
        # Get a histogram of visual words for the query image
        image_words = sift_vocabulary.project(sift_query)
        print 'Query database with a SIFT histogram...'
        # Use the histogram to search the database
        sift_candidates = search.query_iw('sift', image_words)

    if feature_active('harris'):
        print 'Loading Harris vocabulary ...'
        fname = base + '_harris_vocabulary.pkl'
        with open(fname, 'rb') as f:
            harris_vocabulary = pickle.load(f)

        harris_query = ft.get_harris_features([args.query])[args.query]
        image_words = harris_vocabulary.project(harris_query)
        print 'Query database with an Harris histogram...'
        harris_candidates = search.query_iw('harris', image_words)


    if feature_active('colorhist'):
        print 'Load colorhist features ..'
        fname = base + '_colorhist.pkl'
        # Load all colorhistogram features of our training data
        with open(fname, 'rb') as f:
            colorhist_features = pickle.load(f)
        
        # Get colorhistogram for the query image
        colorhist_query = ft.get_colorhist([args.query])[args.query]
        print 'Query database with a colorhistogram'
        # Compare the query colorhist with the dataset and retrieve an ordered list of candidates
        colorhist_candidates = search.candidates_from_colorhist(colorhist_query, colorhist_features)
    
    if feature_active('geo'):
        print 'Load geo data ..'
        fname = base + '_meta.pkl'
        with open(fname, 'rb') as f:
            geo_features = pickle.load(f)

        metadata = ft.extract_metadata([args.query])[args.query]
        if metadata_distance.has_geotag(metadata):
            distances = []
            for key in geo_features.keys():
                candidate_metadata = geo_features[key]
                if metadata_distance.has_geotag(candidate_metadata):
                    distances.append((key, metadata_distance.compute_geographic_distance(metadata, candidate_metadata)))
                
            geo_candidates = sorted(distances, key = lambda x: x[1])
        else:
            print 'Warning: query image has no geotag!'
            



    # Visualizing Results
    # ==================
    

    # Plot query image    
    fig = plt.figure()
    query_im = cv2.imread(args.query, cv2.IMREAD_COLOR)
    # Convert colorspace from BGR to RGB since we're plotting with pyplot
    query_im = cv2.cvtColor(query_im, cv2.COLOR_BGR2RGB)
    plt.imshow(query_im)
    plt.axis('off')
    fig.canvas.set_window_title('Query Image') 

    def plot_results(im_list, title, distance, labels=None):
        fig = plt.figure()
        i = 1
        for im_name in im_list:
            geotag = ft.extract_exif(im_name)
            print i, im_name, '\t\tgeotag:', geotag, '\tdist: ', distance[i-1]
            im = cv2.imread(im_name, cv2.IMREAD_COLOR)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            plt.subplot(2,5,i)
            plt.imshow(im)
            if labels == None:
                plt.title(i)
            else:
                plt.title(labels[i-1])
            plt.axis('off')
            i += 1
        fig.canvas.set_window_title(title) 

    # If candidates exists, show the top N candidates
    N = 10
    
    if not sift_candidates == None:
        sift_winners = [search.get_filename(cand[1]) for cand in sift_candidates][0:N]
        sift_distances = [cand[0] for cand in sift_candidates][0:N]
        plot_results(sift_winners, 'SIFT Results', sift_distances)

    if not harris_candidates == None:
        harris_winners = [search.get_filename(cand[1]) for cand in harris_candidates][0:N]
        harris_distances = [cand[0] for cand in harris_candidates][0:N]
        plot_results(harris_winners, 'Harris Results', harris_distances)

    if not colorhist_candidates == None:
        distances = colorhist_candidates[1][0:N]
        filenames = colorhist_candidates[0][0:N]

        plot_results(filenames, 'Colorhistogram Results', distances)

    if not geo_candidates == None:
        filenames = [x[0] for x in geo_candidates][0:N]
        distances = [x[1] for x in geo_candidates][0:N]
        plot_results([x[0] for x in geo_candidates][0:N], 'Geodistances Results', distances)
        
   
    # Add Key event to close the application with the 'q' or 'escape' key
    def onKey(event):
        if event.key == 'q' or event.key == 'escape':
            sys.exit(0)


    plt.connect('key_release_event', onKey)
    plt.show()



