from os import listdir, path
import sqlite3
import sys

import process_video

def main(video_folder, database_location, sift_database_location):
    """Process each video in the folder"""
    
    # Validate parameters
    if not path.isdir(video_folder):
        print 'Invalid video directory path: {}'.format(video_folder)
        return
        
    if not path.exists(database_location):
        print 'Invalid database location: {}'.format(database_location)
        return

    # Connect to database
    conn = sqlite3.connect(database_location)
    cursor = conn.cursor()

    # Get data
    video_files = listdir(video_folder)
    video_ids   = [f.split('.')[0] for f in video_files if f.endswith('.avi')]
    
    # Stats
    true_positives  = 0 # Category 1 classified as category 1
    false_positives = 0 # Categories 2 or 3 classified as category 1
    true_negatives  = 0 # Categories 2 or 3 classified as categories 2 or 3
    false_negatives = 0 # Category 1 classified as categories 2 or 3

    for video_id in video_ids:
        
        # Make sure both a .avi and .wav file are available for this id
        video_location = path.join(video_folder, '{}.avi'.format(video_id))
        audio_location = path.join(video_folder, '{}.wav'.format(video_id))
        
        if not path.exists(video_location) or not path.exists(audio_location):
            continue
        
        # Process video
        print 'Processing `{}`...'.format(video_id) 
        category_classifier = process_video.process(
            video_location,
            audio_location,
            database_location,
            sift_database_location
        )

        # Get actual label
        metadata = video_id.split('-')
        db_video_id = ''.join(metadata[:-2])
        db_start_time_ms = metadata[-2]

        query = '''
            SELECT category FROM classifications
            WHERE video_id = ?
            AND start_time_ms = ?
        '''
        cursor.execute(query, (db_video_id, db_start_time_ms))
        category_actual = cursor.fetchone()[0]

        # Mark as TP, FP, TN, or FN
        if category_classifier == 1:
            if category_actual == 1:
                true_positives += 1
                mark = 'TP'
            else:
                false_positives += 1
                mark = 'FP'
        else:
            if category_actual == 1:
                false_negatives += 1
                mark = 'FN'
            else:
                true_negatives += 1
                mark = 'TN'
        
        print 'Classified as category {} ({})'.format(
            category_classifier,
            mark
        )
        
        print

    print

    print 'RESULTS:'
    print
    print 'True Positives  (TP) =', true_positives
    print 'False Positives (FP) =', false_positives
    print 'True Negatives  (TN) =', true_negatives
    print 'False Negatives (FN) =', false_negatives

    print
    print 'Recall    [TP / (TP + FN)] =', float(true_positives) / (true_positives + false_negatives)
    print 'Precision [TP / (TP + FP)] =', float(true_positives) / (true_positives + false_positives)
        
if __name__ == "__main__":

    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "Please provide path to videos and database."
