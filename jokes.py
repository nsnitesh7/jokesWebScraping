import pickle
import urllib2
from bs4 import BeautifulSoup
import types
import sys
sys.setrecursionlimit(50000)

jokesList={}

def replace_with_newlines(element):
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, types.StringTypes):
            text += elem.strip()
        elif elem.name == 'br':
            text += '\n'
    return text

def extractJoke(jokeLink):
	print jokeLink
	try:
		page = urllib2.urlopen(jokeLink)
	except:
		print "Couldn't retrieve joke from ", jokeLink
		return ""
	soup = BeautifulSoup(page)
	mydivs = soup.findAll("div", { "class" : "content_wrap" })
	newJoke=""
	for p in mydivs[0].find_all("p"):
		newJoke+= replace_with_newlines(p)
#		print p.name
#		print ''.join(p.findAll(text=True))
	newJoke+='\n'
	return newJoke

def extractJokeLinks(categoryLink):
	page = urllib2.urlopen(categoryLink)
	soup = BeautifulSoup(page)
	for l in soup.findAll("ul")[4].find_all("li"):
#		print l.a["href"]
#		print l.h3.string
		if l.h3.string in jokesList:
			continue
		newString=extractJoke(l.a["href"])
		if(newString!=""):
			jokesList[l.h3.string]=newString

def gotoDiffCategories(siteLink):
	page = urllib2.urlopen(siteLink)
	soup = BeautifulSoup(page)
	mydivs = soup.findAll("ul", { "class" : "list_horiz" })
	for link in mydivs[0].findAll("a"):
		#print link["href"]
		extractJokeLinks(link["href"])

gotoDiffCategories("http://www.jokes.com/")

#extractJokeLinks('http://www.jokes.com/funny-news---politics')

#print jokesList


#extractJoke('http://www.jokes.com/funny-god-jokes/t59agc/coincidentally')

items = list(jokesList.items())

with open('jokes.pickle', 'wb') as handle:
	pickle.dump(items, handle)


#read from pickle data structure
#with open('jokes.pickle', 'rb') as handle:
#  b = pickle.load(handle)
