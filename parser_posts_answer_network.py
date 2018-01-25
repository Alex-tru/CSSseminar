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
		self.netMatrix = {}#entries are countries netmatrix[answeringCountry][askingCountry]
		self.answerTagsDict = {}#to store tags of a question and give them to answers
		self.Q_locations = {}
		self.validQ_Id = set([])

		with open("listExperts.pickle", "rb") as mypickle:
			self.experts = set(pickle.load(mypickle))#loading set of expert users
	
		#dict with {validUsers : location}
		with open("dictValidUserLocation.pickle", "rb") as mypickle:
			self.loc_valid_usrs = pickle.load(mypickle)
		self.valid_users = set(self.loc_valid_usrs.keys())

		#Initialize headers (row and column) of the matrix for each country as dictionaries with countries as keys
		self.locations = set(self.loc_valid_usrs.values())
		n_locs = len(self.locations)		
		for i in xrange(n_locs):
			this_loc = self.locations.pop()
			self.netMatrix[this_loc] = {}
			mylocs = set(self.loc_valid_usrs.values())
			for j in xrange(n_locs):
				self.netMatrix[this_loc][mylocs.pop()] = 0


		print self.loc_valid_usrs[1310719]

	#read data of one user
	#reads id, reputation, score
	def startElement(self, tag, attributes):
		self.CurrentData = tag
		self.postCount += 1
		if tag == "row":
			self.id = attributes["Id"]
			self.typeId = attributes["PostTypeId"]
			self.score = attributes["Score"]
#			print self.id, self.postCount
	
			#ignore posts with low score
#			if int(self.score) < 10:
#				user = "None"
			if "OwnerUserId" in attributes.getNames():			
				self.ownerId = attributes["OwnerUserId"]
				user = int(self.ownerId)
				
				#if post is a question from a valid user
				if self.typeId == "1": 
					if user in self.valid_users:
						#registering the location of the question (with the user:loc dict)
						self.Q_locations[self.id] = self.loc_valid_usrs[user]
						self.validQ_Id.add(self.id)					

				#if it is an answer, we process it only if it is from an expert (and the question was from a valid user so that we can know where it comes from))
				elif user in self.experts:
#					print "was in experts"
					self.linkedId = attributes.get("ParentId","-1")
					if self.linkedId in self.validQ_Id:
						#+1 to number of answers by answecountry to question country
						self.netMatrix[self.loc_valid_usrs[user]][self.Q_locations[self.linkedId]] += 1

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
			print self.netMatrix["United States"]
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
		with open("networkAnswers.pickle", "wb") as mypickle:
			pickle.dump(self.netMatrix, mypickle)
		netKeys = self.netMatrix.keys()
		writer.writerow([("\t"+"\t".join(netKeys)).encode('utf-8')])#column names
		for answeringCountry in self.netMatrix:#countries in rows: answering
			writer.writerow([(answeringCountry+"\t".join([str(self.netMatrix[answeringCountry][askingC]) for askingC in netKeys])).encode('utf-8')])


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
	with open('answerNetworkMatrix.csv','w') as f:
		writer = csv.writer(f)
#		writer.writerow("ID"+'\t'+"Type ID"+'\t'+"Linked post ID"+'\t'+"Owner ID"+'\t'+"Owner name"+'\t'+"Tags")
		parser.parse("Posts.xml")
		

	print "Parsed (time: ",time.time()-time1,")"


