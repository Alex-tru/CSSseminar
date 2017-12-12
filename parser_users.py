#!/usr/bin/python

#Parse the Users.xml file from the StackOverflow Data Dump

import xml.sax
import time
import csv

class UserHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.CurrentData = ""
		self.id = ""
		self.reputation = ""
		self.location = ""
		self.UserCount = 0
		self.UserCountValidRep = 0
		self.UserCountWithLocation = 0#might be unvalid
		self.UserCountRepAndLoc = 0
	
	#read data of one user
	#reads id, reputation, location.
	def startElement(self, tag, attributes):
		self.CurrentData = tag
		self.UserCount += 1
		if tag == "row":
			self.id = attributes["Id"]
			self.reputation = attributes["Reputation"]
			if "Location" in attributes.getNames():
				self.location = attributes["Location"]
				self.UserCountWithLocation += 1
			else: 
				#if no location is specified in the xml, it is set to unknown
				self.location = "Unknown"
			if int(self.reputation) > 1:
				self.UserCountValidRep += 1
				if self.location != "Unknown":
					self.UserCountRepAndLoc += 1	
					writer.writerow([(self.id+'\t'+self.reputation+'\t'+self.location).encode('utf-8')])
	#TODO write only the data of users with rep>threshold and location known
		#write to a csv file
#		if self.UserCount < 1000:#write only first users, to debug
#			writer.writerow([(self.id+'\t'+self.reputation+'\t'+self.location).encode('utf-8')])

#NOTE: For some reason, when location has at least a comma in it, the entire row has " " around it (as text delimiter?)

#TODO clean Location field

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
		print "Users:", self.UserCount
		print "Users with Reputation > 1:", self.UserCountValidRep
		print "Users providing location (either valid or not):", self.UserCountWithLocation
		print "Users with Rep. > 1 and location:", self.UserCountRepAndLoc 


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
	with open('Users.csv','w') as f:
		writer = csv.writer(f)
#		f.writerow('Id\tReputation\tLocation')
		parser.parse("Users.xml")
		

	print "Parsed (time: ",time.time()-time1,")"


