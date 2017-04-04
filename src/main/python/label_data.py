from os import listdir, path
import sqlite3
import sys

import cv2
import pygame

def main(video_folder, database_location):
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
    
    # Set up audio playback
    pygame.init()
    
    for video_id in video_ids:
        
        labeled = False
        stop    = False
        
        while not labeled and not stop:
        
            # Make sure both a .avi and .wav file are available for this id
            video_location = path.join(video_folder, '{}.avi'.format(video_id))
            audio_location = path.join(video_folder, '{}.wav'.format(video_id))
            
            if not path.exists(video_location) or not path.exists(audio_location):
                continue
            
            print 'Labeling `{}`...'.format(video_id) 
            
            # Parse metadata from video_id
            metadata = video_id.split('-')
            db_video_id = ''.join(metadata[:-2])
            db_start_time_ms = metadata[-2]
            
            # Play audio
            pygame.mixer.music.load(audio_location)
            pygame.mixer.music.play()
            
            # Play video
            cap = cv2.VideoCapture(video_location)
            
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    cv2.imshow('frame', gray)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            for i in range (1,10):
                cv2.waitKey(1)
            
            # Ask user for label
            print 'Please pick one of the following options:'
            print '\tLabel as 3rd-person drone video with sound: `1`'
            print '\tLabel as 1st-person drone video with sound: `2`'
            print '\tLabel as trash: `3`'
            print '\tSave and quit: `q`'
            print '\tRewatch this clip: `r` (or anything else)'
            
            user_input = raw_input('> ')
            
            if user_input in ['1', '2', '3']:
                cursor.execute(
                    'INSERT INTO classifications VALUES (?, ?, ?)',
                    (db_video_id, db_start_time_ms, int(user_input))
                )
                labeled = True
            
            elif user_input == 'q':
                stop = True
        
        print
        
        if stop:
            break
        
    # Commit and close database
    conn.commit()
    conn.close()
    
if __name__ == "__main__":

    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print "Please provide path to videos and database."
