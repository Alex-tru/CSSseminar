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
		self.name = "" #this can be an answer or a question
		self.badgesCount = 0
	
	#read data of one user
	#reads id, reputation, location.
	def startElement(self, tag, attributes):
		self.CurrentData = tag
		self.badgesCount += 1
		if tag == "row":
			self.id = attributes["Id"]
			self.userId = attributes["UserId"]
			self.name = attributes["Name"]

		#write to a csv file
		if self.badgesCount < 1000:#write only first users, to debug
			writer.writerow([(self.id+'\t'+self.userId+'\t'+self.name).encode('utf-8')])

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
	with open('Badges.csv','w') as f:
		writer = csv.writer(f)
		writer.writerow("ID"+'\t'+"UserID"+'\t'+"Badge name")
		parser.parse("Badges.xml")
		

	print "Parsed (time: ",time.time()-time1,")"


