import os
import sys

def main(video_folder, database_location):
    """Process each video in the folder"""
    
    # Validate parameters
    
    if not os.path.isdir(video_folder):
        print 'Invalid video directory path: {}'.format(video_folder)
        return
        
    if not os.path.exists(database_location):
        print 'Invalid database location: {}'.format(database_location)
        return
    
    print 'Videos at: {}'.format(video_folder)
    print 'Database at: {}'.format(database_location)

if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print "Please provide path to videos and database."
