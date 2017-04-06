#!/usr/bin/env python

import argparse
import glob
import os.path
import pickle
import sys

import db_index
import feature_extraction as ft
from src.main.python import Vocabulary


# Function definitions for some repetitive tasks
# ==============================================

def feature_active(name):
    """ Check if feature 'name' is active
    
    i.e. the feature has been selected via a command line option to be used for processing"""
    return (args.feature == name or args.feature == 'all')


def load_features(name):
    """ Loads features from disk. 
    
    This is done by opening a pickle file and deserializing it. 
    name -- selected features, e.g. sift, harris
    """
    # create file name from prefix(path), base name, feature name and extension.
    fname = args.prefix + base + '_' + name + '.pkl'
    feat = None
    # open file fname in (r)eading mode in (b)inary format
    with open(fname, 'rb') as f:
        print 'Loading', fname
        # deserialize the binary file
        feat = pickle.load(f)
    return feat 

def compute_features(image_list, name, feature_function):
    """ Computes features for all images in image_list using given function.

    This function checks if features are already computed. It asks if features should be recomputed and it saves the features to disk.
    arguments:
    image_list -- list of relative paths to images
    name -- name of selected feature, used for saving filename to disk
    feature_function -- function that accepts a list of images and returns a dictionary of features with image paths as keys
    """
    # Create file name
    fname = args.prefix + base + '_' + name + '.pkl'
    # Check if file exists already. If true, ask if features need be recomputed.
    if os.path.isfile(fname):
        compute = raw_input("Found existing features: " + fname + " Do you want to recompute them? ([Y]/N): ")
    else:
        # If file is not found, mark compute flag for computing.
        compute = 'Y'

    if compute == 'Y' or compute == '':
        # Compute features using the provided function.
        features = feature_function(image_list)
        # Open file in writing mode and write serialized binary data to disk to save computing time during next runs.
        with open(fname, 'wb') as f:
            print 'saving features to', fname , '...'
            pickle.dump(features, f)
    else:
        # If features do not need to be computed, just load features from disk
        features = load_features(name)
    return features


# Starting point of the script
# =======================================

if __name__ == '__main__':

    # List supported features.
    features = ['sift', 'colorhist', 'harris', 'meta', 'all']
    # List common photo extensions used by glob to search for images.
    types = ('*.jpg', '*.JPG', '*.png')

    # Initialize ArgumentParser object to handle command line input
    parser = argparse.ArgumentParser(description="Database tool creates features and Visual Bag of Words database for a specified training set of images.")
    parser.add_argument("feature", help="The type of features you want to generate. Chose from " + str(features))
    parser.add_argument("training_set", help="Path to training images.")
    parser.add_argument("--database", "-d", help="Optional output name for the database", default="MMA.db")
    parser.add_argument("--prefix","-p",  help="prefix path to database directory, default = 'db/'", default="db/")
    parser.add_argument("--clusters", "-c", help="Number of clusters for K-Means clustering algorithm'", default=100)
    
    # Parse command line arguments and store them in args.
    args = parser.parse_args()
    # The prefix argument can be an nonexisting folder. This folder is created if needed.
    if not os.path.exists(args.prefix):
        os.makedirs(args.prefix)

    print '\nMulti Media Analysis Database tool'
    print '==================================\n'
    print 'Creating', args.feature, 'features for', args.training_set ,'\n'


    # Retrieve image list from traning_set argument specified on the command line.
    image_list = []
    for type_ in types:
        files = args.training_set + type_
        image_list.extend(glob.glob(files))	

    # Get file name without extension and prefix
    base=os.path.basename(args.database).split('.')[0]

    sift_features = None
    sift_vocabulary = None
    harris_features = None
    harris_vocabulary = None
    colorhist_features = None
    meta_features = None

    # Compute sift features and vocabulary if sift is 'active'
    if feature_active('sift'):
        sift_features = compute_features(image_list, 'sift', ft.get_sift_features)

        # Create a visual vocabulary (Bag of Words) from the sift extracted features.  If the vocabulary already exists the user will be asked if the vocabulary needs to be recreated.
        
        fname = args.prefix + base + '_sift_vocabulary.pkl'
        if os.path.isfile(fname):
            compute = raw_input("Found existing vocabulary: " + fname + " Do you want to recompute it? ([Y]/N): ")
        else:
            compute = 'Y'
        if compute == 'Y' or compute == '':
            print 'Creating SIFT vocabulary ... '
            sift_vocabulary = Vocabulary.Vocabulary(base)
            sift_vocabulary.train(sift_features, args.clusters)
            fname = args.prefix + base + '_sift_vocabulary.pkl'
            with open(fname, 'wb') as f: 
                pickle.dump(sift_vocabulary,f)


    if feature_active('colorhist'):
        colorhist_features = compute_features(image_list, 'colorhist', ft.get_colorhist)

    if feature_active('harris'):
        harris_features = compute_features(image_list, 'harris', ft.get_harris_features)

        # Create the visual vocabulary for Harris features.
        
        fname = args.prefix + base + '_harris_vocabulary.pkl'
        if os.path.isfile(fname):
            compute = raw_input("Found existing vocabulary: " + fname + " Do you want to recompute it? ([Y]/N): ")
        else:
            compute = 'Y'
        if compute == 'Y' or compute == '':
            print 'Creating Harris vocabulary ... '
            harris_vocabulary = Vocabulary.Vocabulary(base)
            harris_vocabulary.train(harris_features, args.clusters)
            fname = args.prefix + base + '_harris_vocabulary.pkl'
            with open(fname, 'wb') as f: 
                pickle.dump(harris_vocabulary,f)


    if feature_active('meta'):
        meta_features = compute_features(image_list, 'meta', ft.extract_metadata)


    # DATABASE Creating and insertion
    # If the database already exsists, we can remove it and recreate it, or we can just insert new data. 


    db_name = args.prefix + base + '.db'

    #check if database already exists
    new = False
    if os.path.isfile(db_name):
        action = raw_input('Database already exists. Do you want to (r)emove, (a)ppend or (q)uit? ')
        print 'action =', action
    else:
        action = 'c'

    if action == 'r':
        print 'removing database', db_name , '...'
        os.remove(db_name)
        new = True

    elif action == 'a':
        print 'appending to database ... '

    elif action == 'c':
        print 'creating database', db_name, '...'
        new = True

    else:
        print 'Quit database tool'
        sys.exit(0)



    # Create indexer which can create the database tables and provides an API to insert data into the tables.
    indx = db_index.Indexer(db_name) 
    if new == True:
        indx.create_tables()


    # Loading necessary features if not in memory yet. Then add features 
    # to their corresponding database tables.
    if feature_active('sift'): 
        if sift_vocabulary == None:
            sift_vocabulary = load_features('sift_vocabulary')
        if sift_features == None:
            sift_features = load_features('sift')

        print '\nAdding sift features to database ...\n'
        for i in range(len(image_list)):
            indx.add_to_index('sift', image_list[i], sift_features[image_list[i]], sift_vocabulary)

   # if feature_active('colorhist'):
   #     if colorhist_features == None:
   #         colorhist_features = load_features('colorhist')
#
 #       print '\nAdding colorhist features to database ...\n'
  #      for i in range(len(image_list)):
   #         indx.add_to_colorhist_index(image_list[i], colorhist_features[image_list[i]])

    if feature_active('harris'):
        if harris_vocabulary == None:
            harris_vocabulary = load_features('harris_vocabulary')
        if harris_features == None:
            harris_features = load_features('harris')

        print '\nAdding harris features to database ...\n'
        for i in range(len(image_list)):
            indx.add_to_index('harris', image_list[i], harris_features[image_list[i]], harris_vocabulary)

    indx.db_commit()

    print '\nDone\n'
