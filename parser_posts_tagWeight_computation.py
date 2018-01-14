#!/usr/bin/python

#Parse the Users.xml file from the StackOverflow Data Dump

import xml.sax
import time
import csv
import pickle

class UserHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.CurrentData = ""
		self.id = ""
		self.typeId = ""
		self.linkedId = "" #this can be an answer or a question
		self.ownerId = ""
		self.ownerName = ""
		self.tags = ""
		self.score = ""
		self.postCount = 0
		self.UserTagsDict = {}#tags used by users
		self.answerTagsDict = {}#to store tags of a question and give them to answers
		self.UserTagWeight = {}#tag weight (or tag score) of a user

		with open("dict.pickle", "rb") as mypickle:
			self.TagWeights = pickle.load(mypickle)#loading dict of tag weights we precomputed
		with open("dictvalidusers.pickle", "rb") as mypickle:#loading list of users with location and reputation>1
			self.validUsers = set([str(user) for user in pickle.load(mypickle)])

	#read data of one user
	#reads id, reputation, location.
	def startElement(self, tag, attributes):
		self.CurrentData = tag
		self.postCount += 1
		if tag == "row":
			self.id = attributes["Id"]
			self.typeId = attributes["PostTypeId"]
			self.score = attributes["Score"]
#			print self.id, self.postCount
	
			#ignore posts with low score
			if int(self.score) < 10:
				user = "None"
			elif "OwnerUserId" in attributes.getNames():			
				self.ownerId = attributes["OwnerUserId"]
				self.ownerName = "See owner ID"
				user = self.ownerId
				
				if user in self.validUsers:
					if self.ownerId not in self.UserTagsDict.keys():
						self.UserTagsDict[user] = {}#Create dict for a user
				else:
					user = "None"
			elif "OwnerDisplayName" in attributes.keys():
				#IN THIS CASE USERS HAVE BEEN ELIMINATED!! NO ID
#				self.ownerName = attributes["OwnerDisplayName"]
#				self.ownerId = "Not specified"
#				user = self.ownerName
				user = "None"
				if self.ownerName not in self.UserTagsDict.keys():
					self.UserTagsDict[user] = {}#Create dict for a user
			else:
				self.ownerName = "Not specified"
				self.ownerId = "Not specified"
				user = "None"
			
			if user is not "None":#skip posts without user id

				if self.typeId == "1":
					if "AcceptedAnswerId" in attributes.getNames():
						self.linkedId = attributes["AcceptedAnswerId"]
					else: self.linkedId = "No accepted answer"
					self.tags = attributes["Tags"]
					tags = self.tags[1:-1].split('><')
					for tag in tags:
#						self.UserTagsDict[user][tag] = self.UserTagsDict[user].get(tag,0)+1
						self.UserTagWeight[user] = self.UserTagWeight.get(user,0)+self.TagWeights.get(tag,0)
					self.answerTagsDict[self.id] = self.tags
				elif self.typeId == "2":
					self.linkedId = attributes["ParentId"]
					if self.linkedId in self.answerTagsDict.keys():#"if this is an answer to an existing question"
						self.tags = self.answerTagsDict[self.linkedId]#get string of tags from parent question
						tags = self.tags[1:-1].split('><')#put them in a list
						for tag in tags:#update the sum of tag uses for a user
#							self.UserTagsDict[user][tag] = self.UserTagsDict[user].get(tag,0)+1
							self.UserTagWeight[user] = self.UserTagWeight.get(user,0)+self.TagWeights.get(tag,0)
	#    (just printing)  print '---------------------'
	#					print 'User:', self.ownerId
	#					for tag in self.UserTagsDict[user].keys():
	#						print tag, self.UserTagsDict[user][tag]
#					else: print "Whoops", self.postCount


				#write to a csv file
	#			if self.postCount < 1000:#write only first users, to debug
#				writer.writerow([(self.id+'\t'+self.typeId+'\t'+self.linkedId+'\t'+self.ownerId+'\t'+self.ownerName+'\t'+self.tags).encode('utf-8')])
		

		

	#for printing on screen after every X elements
	def endElement(self, tag): 
		if self.postCount % 100000 == 0:
			print "Posts:", self.postCount
#			for user,weightA in self.UserTagWeightA.iteritems():
#				print user+'\t'+str(weightA)+'\t'+str(self.UserTagWeightQ.get(user,0))+'\t'+str(weightA+self.UserTagWeightQ.get(user,0))
#			print "Users with Reputation > 1:", self.UserCountValidRep
#			print "Users providing location (either valid or not):", self.UserCountWithLocation
#			print "Users with Rep. > 1 and location:", self.UserCountRepAndLoc 
#		print "Id:", self.id
#		print "Reputation:", self.reputation
#		print "Location:", self.location

	def endDocument(self):
		print "Posts:", self.postCount
		for user,weight in self.UserTagWeight.iteritems():
			writer.writerow([(user+'\t'+str(weight)).encode('utf-8')])


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
	with open('userFinalTagWeight.csv','w') as f:
		writer = csv.writer(f)
#		writer.writerow("ID"+'\t'+"Type ID"+'\t'+"Linked post ID"+'\t'+"Owner ID"+'\t'+"Owner name"+'\t'+"Tags")
		writer.writerow([("userId"+'\t'+"tagWeightA"+'\t'+"tagWeightQ"+'\t'+"tagWeight").encode('utf-8')])
		parser.parse("Posts.xml")
		

	print "Parsed (time: ",time.time()-time1,")"


