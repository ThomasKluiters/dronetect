import pickle

import numpy as np
from pysqlite2 import dbapi2 as sqlite
from scipy.spatial.distance import cosine

class Searcher:

	def __init__(self, db):
		self.con = sqlite.connect(db)

	def __del__(self):
		self.con.close()

	def candidates_from_word(self, type, imword):
		""" Get list of images containing imword/ """

		im_ids = self.con.execute(
				"select distinct imid from "+type+"_imwords where wordid=%d" % imword).fetchall()
		return [i[0] for i in im_ids]


    	def color_hist_distance(hist1, hist2):
       		return cosine(hist1,hist2)
#		return np.sum((hist1-hist2)**2)

	def candidates_from_colorhist(self, hist, features):
		result = []
		names = []
		for key in features.keys():
			d = np.sum((hist-features[key])**2)
			result.append(d)
			names.append(key)
		i = np.argsort(result)
		return (np.array(names)[i] , np.array(result)[i])

	def candidates_from_histogram(self, type, imwords):
		""" Get list of images wth similar words. """

		# get the word ids
		words = imwords.nonzero()[0]
		# find candidates
		candidates = []
		for word in words:
			c = self.candidates_from_word(type, word)
			candidates += c
		
		# take all unique words and reverse sort on occurence
		tmp = [(w, candidates.count(w)) for w in set(candidates)]
		tmp.sort(cmp=lambda x, y:cmp(x[1],y[1]))
		tmp.reverse()

		# return sorted list, best matches first
		return [w[0] for w in tmp]

	def get_colorhist(self, imname):
		""" Return the color histogram for an image. """
		im_id = self.con.execute(
				"select rowid from imlist where filename='%s'" % imname).fetchone()
		s = self.con.execute(
				"select hist from colorhists where rowid='%d'" % im_id).fetchone()

		# use pickle to decode NumPy arrays from string
		return pickle.loads(str(s[0]))


	
	def get_imhistogram(self, type, imname):
		""" Return the word histogram for an image. """

		im_id = self.con.execute(
				"select rowid from imlist where filename='%s'" % imname).fetchone()
		s = self.con.execute(
				"select histogram from "+type+"_imhistograms where rowid='%d'" % im_id).fetchone()

		# use pickle to decode NumPy arrays from string
		return pickle.loads(str(s[0]))

	def query(self, type, imname):
		""" Find a list of matching images for imname"""

		h = self.get_imhistogram(imname)
		candidates = self.candidates_from_histogram(type,h)

		matchscores = []
		for imid in candidates:
			# get the name
			cand_name = self.con.execute(
					"select filename from imlist where rowid=%d" % imid).fetchone()
			cand_h = self.get_imhistogram(cand_name)
			cand_dist = np.sqrt( np.sum( (h-cand_h)**2 ) ) #use L2 distance
			matchscores.append( (cand_dist, imid) )

			#return a sorted list of distances and databse ids
			matchscores.sort()
		return matchscores

	def query_iw(self,type, h):
		""" Find a list of matching images for image histogram h"""
		candidates = self.candidates_from_histogram(type,h)
		matchscores = []
		for imid in candidates:
			# get the name
			cand_name = self.con.execute(
							"select filename from imlist where rowid=%d" % imid).fetchone()
			cand_h = self.get_imhistogram(type, cand_name)

			cand_dist = np.sqrt( np.sum( (h-cand_h)**2 ) ) #use L2 distance
			matchscores.append( (cand_dist, imid) )
			#return a sorted list of distances and databse ids
		matchscores.sort()
		return matchscores



	def get_filename(self,imid):
		""" Return the filename for an image id"""
		s = self.con.execute(
				"select filename from imlist where rowid='%d'" % imid).fetchone()
		return s[0]
