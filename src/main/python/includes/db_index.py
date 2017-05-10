import pickle
import numpy as np
from pysqlite2 import dbapi2 as sqlite

class Indexer(object):

    def __init__(self, db):
        self.con = sqlite.connect(db)

    def __del__(self):
        self.con.close()
    
    def db_commit(self):
        self.con.commit()
    
    def create_tables(self):
        self.con.execute('create table imlist(filename)') 
        self.con.execute('create index im_idx on imlist(filename)') 

        self.con.execute('create table sift_imwords(imid,wordid,vocname)') 
        self.con.execute('create index sift_imid_idx on sift_imwords(imid)') 
        self.con.execute('create index sift_wordid_idx on sift_imwords(wordid)') 

        self.con.execute('create table sift_imhistograms(imid,histogram,vocname)') 
        self.con.execute('create index sift_imidhist_idx on sift_imhistograms(imid)') 

        self.con.execute('create table colorhists(imid, hist)')
        self.con.execute('create index colorhist_idx on colorhists(imid)') 

        self.con.execute('create table harris_imwords(imid,wordid,vocname)') 
        self.con.execute('create index harris_imid_idx on harris_imwords(imid)') 
        self.con.execute('create index harris_wordid_idx on harris_imwords(wordid)') 

        self.con.execute('create table harris_imhistograms(imid,histogram,vocname)') 
        self.con.execute('create index harris_imidhist_idx on harris_imhistograms(imid)') 


        self.db_commit()

    def add_to_index(self, type, imname, descr, voc):
        """ Take an image with feature descriptors, 
            project on vocabulary and add to database. """

        print 'indexing', imname

        # get the imid
        imid = self.get_id(imname)

        #get the words
        imwords = voc.project(descr)
        nbr_words = imwords.shape[0]

        # link each word to image
        for i in range(nbr_words):
            word = imwords[i]
            # wordid is the word number itself
            self.con.execute("insert into "+type+"_imwords(imid,wordid,vocname) values (?,?,?)", (imid,word,voc.name))

        # store word histogram for image
        # use pickle to encode NumPy arrays as strings
        self.con.execute("insert into "+type+"_imhistograms(imid,histogram,vocname) values (?,?,?)", (imid,pickle.dumps(imwords), voc.name))

    def add_to_colorhist_index(self, imname, hist):

        print 'indexing', imname

        # get the imid
        imid = self.get_id(imname)

        self.con.execute("insert into colorhists(imid, hist) values (?,?)", (imid, pickle.dumps(hist)))

    def is_indexed(self, imname):
        """ Returns True is imname has been indexed. """

        im = self.con.execute("select rowid from imlist where filename='%s'" % imname).fetchone()
        return im != None

    def get_id(self, imname):
        """ Get an entry id and add if not present. """

        cur = self.con.execute("select rowid from imlist where filename='%s'" % imname)
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute("insert into imlist(filename) values ('%s')" % imname)
            return cur.lastrowid
        else:
            return res[0]


