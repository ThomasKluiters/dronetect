# -*- coding: utf-8 -*-
import cv2
import numpy as np
import progressbar
import harris
import exifread
import pyexiv2
from scikits.talkbox.features import mfcc

def extract_metadata(im_list):
	features = {}
	for im_name in im_list:
		tags = None
		geotags = extract_exif(im_name)
		features[im_name] = (tags, geotags)
		
	return features	

def harris_features(im):
    response = cv2.cornerHarris(im, 7, 5, 0.05)
    points = harris.get_harris_points(response)
    desc = harris.get_descriptors(im, points)
    return points, desc

def get_harris_features(im_list):
    total = len(im_list)
    bar = progressbar.ProgressBar(maxval=total, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    print 'Generating Harris features for [', total, '] images ...'
    bar.start()
    features = {}
    count = 0
    for im_name in im_list:
        im = cv2.imread(im_name, 0)
        points, desc = harris_features(im)
        features[im_name] = np.array(desc)
        bar.update(count)
        count += 1
    bar.finish()
    return features

def colorhist(im):
    chans = cv2.split(im)
    color_hist = np.zeros((256,len(chans)))
    for i in range(len(chans)):
        color_hist[:,i] = np.histogram(chans[i], bins=np.arange(256+1))[0]/float((chans[i].shape[0]*chans[i].shape[1]))
    return color_hist


def get_colorhist(im_list):
    total = len(im_list)
    bar = progressbar.ProgressBar(maxval=total, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    print 'Generating ColorHist features for [', total, '] images ...'
    bar.start()
    features = {}
    count = 0
    for im_name in im_list:
        im = cv2.imread(im_name)
        color_hist = colorhist(im)
        features[im_name] = color_hist
        bar.update(count)
        count += 1
    bar.finish()
    return features

def get_sift_features(im_list):
    """get_sift_features accepts a list of image names and computes the sift descriptos for each image. It returns a dictionary with descriptor as value and image name as key """
    sift = cv2.SIFT()
    features = {}
    total = len(im_list)
    bar = progressbar.ProgressBar(maxval=total, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    count = 0
    print 'Generating SIFT features for [', total, '] images ...'
    bar.start()
    for im_name in im_list:
        bar.update(count)
        # load grayscale image
        im = cv2.imread(im_name, 0)
        kp, desc = sift.detectAndCompute(im, None)
        features[im_name] = desc
        count += 1
    bar.finish()
    return features
    
# extract tags
def extract_tags(filename):
    try:
        print 'tags for', filename
        exif_data = pyexiv2.ImageMetadata(filename)
        exif_data.read()
        tags = exif_data['Exif.Photo.UserComment'].value.split(',')
        print tags
        tags = [t.strip() for t in tags]
        return tags
    except:
        print 'No tags could be found for: ' + filename
        return []

# extract exif
def extract_exif(filename):
    # find if there is a geolocation tag, and if so return it.
    # if geolocation was not turned on, return 'no-geotag'
    with open(filename) as f:
        exif_tags = exifread.process_file(f)
        if 'GPS GPSLongitude' in exif_tags:
            # assume that all other GPS tags are in there now
            '''
            GPS GPSLongitude [4, 21, 761/20]
            GPS GPSImgDirection 17621/362
            GPS GPSLatitude [52, 0, 1054/25]
            GPS GPSDate 2014:02:18
            Image GPSInfo 704
            GPS GPSLatitudeRef N
            GPS GPSImgDirectionRef T
            GPS GPSAltitudeRef 0
            GPS GPSTimeStamp [11, 56, 6]
            GPS GPSAltitude 3653/1134
            GPS GPSLongitudeRef E
            '''
            longitude     = [x.num / x.den for x in exif_tags['GPS GPSLongitude'].values]
            latitude     = [x.num / x.den for x in exif_tags['GPS GPSLatitude'].values]
            longRef        = exif_tags['GPS GPSLongitudeRef'].values
            latRef        = exif_tags['GPS GPSLatitudeRef'].values        
            
            friendly_name = str(longitude[0]) + 'd ' + str(longitude[1]) +'\' ' + str(longitude[2]) +'\'\' ' + longRef 
            friendly_name += ', ' + str(latitude[0]) + 'd ' + str(latitude[1]) +'\' ' + str(latitude[2]) +'\'\' ' + latRef 
            
            return (longitude, longRef, latitude, latRef, friendly_name)
        
    return 0
    
def extract_mfcc(audio_samples, fs):
    # find the smallest non-zero sample in both channels
    #nonzero = min(min([abs(x) for x in audio_samples[:,0] if abs(x) > 0]), min([abs(x) for x in audio_samples[:,1] if abs(x) > 0]))
    nonzero = 1
    audio_samples[audio_samples==0] = nonzero
    return mfcc(audio_samples, fs=fs)
    
