#!/usr/bin/python

#Parse the Users.xml file from the StackOverflow Data Dump

import xml.sax
import time
import csv

class UserHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.CurrentData = ""
		self.id = ""
		self.userId = ""
		self.name = "" 
		self.date = ""
		self.badgesCount = 0
		self.UserScore = {}
		self.badgeWeights = {'Curious':1./0.094872143,
'Inquisitive':1./0.009476646,
'Socratic':1./0.001092104,
'Nice Question':1./0.161772329,
'Good Question':1./0.051469811,
'Great Question':1./0.008419771,
'Guru':1./0.012632438,
'Nice Answer':1./0.12186287,
'Good Answer':1./0.039834882,
'Great Answer':1./0.006717754,
'Populist':1./0.00197581,
'Commentator':1./0.096253821,
'Pundit':1./0.001096256,
'Enthusiast':1./0.297222516,
'Fanatic':1./0.045169547,
'Mortarboard':1./0.048617604,
'Epic':1./0.00110855,
'Legendary':1./0.000405147
} 
	
	#read data of one user
	#reads id, reputation, location.
	def startElement(self, tag, attributes):
		self.CurrentData = tag
		self.badgesCount += 1
		if tag == "row":
			self.id = attributes["Id"]
			self.userId = attributes["UserId"]
			self.name = attributes["Name"]
			self.date = attributes["Date"]
			self.UserScore[self.userId] = self.UserScore.get(self.userId,0.)+self.badgeWeights.get(self.name,0.)#sum contribution to score of each badge (if it is in the dict of badges we consider))
			if self.badgesCount % 1000000 == 0:
				print "Badges:", self.badgesCount

#			print "----------------------------"
#			print self.userId, self.UserBadgeCount[self.userId]
		#write to a csv file
#		if self.badgesCount < 1000:#write only first users, to debug
#		writer.writerow([(self.id+'\t'+self.userId+'\t'+self.name+'\t'+self.date).encode('utf-8')])

	#for printing on screen after every X elements
#	def endElement(self, tag): 
#		if self.UserCount % 100000 == 0:
#			print "Users:", self.UserCount
#			print "Users with Reputation > 1:", self.UserCountValidRep
#			print "Users providing location (either valid or not):", self.UserCountWithLocation
#			print "Users with Rep. > 1 and location:", self.UserCountRepAndLoc 
#		print "Id:", self.id
#		print "Reputation:", self.reputation
#		print "Location:", self.location

	def endDocument(self):
		print "Total badges:", self.badgesCount
		for user,score in self.UserScore.iteritems():
			writer.writerow([(user+','+str(score)).encode('utf-8')])


if __name__ == "__main__":
	
	time1 = time.time()	

	# create an XMLReader
	parser = xml.sax.make_parser()
	# turn off namepsaces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	# override the default ContextHandler
	Handler = UserHandler()
	parser.setContentHandler( Handler )
 
	#open csv file and start parsing
	with open('BadgeWeightOfUsers.csv','w') as f:
		writer = csv.writer(f)
#		writer.writerow("ID"+'\t'+"UserID"+'\t'+"Badge name"+'\t'+"Date")
		parser.parse("Badges.xml")
		

	print "Parsed (time: ",time.time()-time1,")"


