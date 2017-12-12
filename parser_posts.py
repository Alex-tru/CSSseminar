#!/usr/bin/python

#Parse the Users.xml file from the StackOverflow Data Dump

import xml.sax
import time
import csv

class UserHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.CurrentData = ""
		self.id = ""
		self.typeId = ""
		self.linkedId = "" #this can be an answer or a question
		self.ownerId = ""
		self.ownerName = ""
		self.tags = ""
		self.postCount = 0
	
	#read data of one user
	#reads id, reputation, location.
	def startElement(self, tag, attributes):
		self.CurrentData = tag
		self.postCount += 1
		if tag == "row":
			self.id = attributes["Id"]
			self.typeId = attributes["PostTypeId"]
#			print self.id, self.postCount
			if "OwnerUserId" in attributes.getNames():				
				self.ownerId = attributes["OwnerUserId"]
				self.ownerName = "See owner ID"
			elif "OwnerDisplayName" in attributes.getNames():
				self.ownerName = attributes["OwnerDisplayName"]
				self.ownerId = "Not specified"
			else:
				self.ownerName = "Not specified"
				self.ownerId = "Not specified"		
			
			if self.typeId == "1":
				if "AcceptedAnswerId" in attributes.getNames():
					self.linkedId = attributes["AcceptedAnswerId"]
				else: self.linkedId = "No accepted answer"
				self.tags = attributes["Tags"]				
			elif self.typeId == "2": 
				self.linkedId = attributes["ParentId"]
				self.tags = "N/A"
			


		#write to a csv file
#		if self.postCount < 1000:#write only first users, to debug
		writer.writerow([(self.id+'\t'+self.typeId+'\t'+self.linkedId+'\t'+self.ownerId+'\t'+self.ownerName+'\t'+self.tags).encode('utf-8')])

	#for printing on screen after every X elements
	def endElement(self, tag): 
		if self.postCount % 1000000 == 0:
			print "Posts:", self.postCount
#			print "Users with Reputation > 1:", self.UserCountValidRep
#			print "Users providing location (either valid or not):", self.UserCountWithLocation
#			print "Users with Rep. > 1 and location:", self.UserCountRepAndLoc 
#		print "Id:", self.id
#		print "Reputation:", self.reputation
#		print "Location:", self.location

	def endDocument(self):
		print "Posts:", self.postCount


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
	with open('Posts.csv','w') as f:
		writer = csv.writer(f)
		writer.writerow("ID"+'\t'+"Type ID"+'\t'+"Linked post ID"+'\t'+"Owner ID"+'\t'+"Owner name"+'\t'+"Tags")
		parser.parse("Posts.xml")
		

	print "Parsed (time: ",time.time()-time1,")"


