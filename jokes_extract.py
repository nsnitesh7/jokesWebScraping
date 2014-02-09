import pickle

#read from pickle data structure
with open('jokes.pickle', 'rb') as handle:
	b = pickle.load(handle)
#print len(b)
