__author__ = "Tatikella Abhishek" 
# handle -  abhishek944

import scrapy
import os
import string
import requests
import pdfkit

class CFContestSpider(scrapy.Spider):

	name = "ContestSpider"		# spider name
	start_urls = []				# required contest url
	dir_name = ""				# required directory name
	tmp = ""
	alpha = ""


	# Call ContestLink and CreateDirectory

	def __init__ (self , arg = None):
		self.ContestLink()
		self.CreateDirectory()



	# Create directory where contest info is stored

	def CreateDirectory(self):
		self.dir_name = input("\nCONTEST NAME : ")									# ContestName
		if not os.path.exists(self.dir_name):
			print ("\nThank You !\n")
			os.makedirs(self.dir_name)
			pass
		else:
			print ("Directory with given name already exists , Provide another !")	# INVALID NAME		
			self.CreateDirectory()



	# Paste required ContestLink - Eg: http://codeforces.com/contest/772

	def ContestLink(self):
		Clink = input("\nCONTEST LINK : ")								# LINK
		try:													
			site_ping = requests.head(Clink)							# Requests Link
			if site_ping.status_code < 400:								# Pasted Link is OK
				self.start_urls.append(Clink)
				for i in range(3):
					print ("\nStarted Downloading ...\n")
		except Exception:												# Exception caught for invalid links
			print ("Given Link is INVALID , Provide another !")
			print ("CAUTION : Make sure that link contains 'http://'")
			self.ContestLink()



	"""
		-> Parser for scraper
		-> Creates Contest folder
	 	-> Creates Problem folders for each problem in Contest folder
	 	-> Creates program files for each problem , Eg : A.cpp , B.cpp ...
	 """

	def parse(self , response):


		# Scraping Starts

		k = len(response.xpath(".//table[@class='problems']//tr").extract())
		a = []
		b = []
		c = []

		for i in range(1,k,1):
			a.append(response.xpath(".//table[@class='problems']//tr[" + str(i+1) + "]/td[@class='id']/a/text()").extract_first())
			b.append(response.xpath(".//table[@class='problems']//tr[" + str(i+1) + "]/td[2]/div/div[@style='float: left;']/a/text()").extract_first());
			c.append(response.xpath(".//table[@class='problems']//tr[" + str(i+1) + "]/td[2]/div/div[@style='float: left;']/a/@href").extract_first());

		# SCRAPING ENDS	



		probs = list(string.ascii_uppercase)											# for uppercase letters


		os.chdir(self.dir_name)															# change to cwd to given directory name
		self.tmp = os.getcwd()															# get path



		# Downloads complete problemset to current directory in pdf format

		print ("\n Downloading complete problemset pdf ...\n")
		pdfkit.from_url(str(self.start_urls[0] + "/problems") , "problemset.pdf")
		print ("\n Done !\n")

		# OK DONE



		# Creates Problem folders with respective program files , Eg : problemA , problemB

		for i in range(1, k , 1):
			os.chdir(self.tmp)
			s = "problem" + str(probs[i - 1])
			print ("\n Downloading problem {} ...\n".format(probs[i - 1]))
			os.makedirs(s)
			os.chdir(s)
			open(str(str(probs[i - 1]) + ".cpp") , "w")

		# OK DONE



		""" 
		Optional : (IF YOU WANT TO PRINT)
			#a -> Problem Alphabet
			#b -> Problem Names
			#c -> Problem Links
		"""

		a = [i.strip(' \n\t\r') for i in a]
		b = [i.strip(' \n\t\r') for i in b]
		c = [i.strip(' \n\t\r') for i in c]



		# For each problem callback function Problem Contents for inputs and outputs

		for i in range(1 , k , 1):
			self.alpha = i - 1
			next_page = str('http://codeforces.com' + c[i - 1])
			if next_page:
				yield scrapy.Request(response.urljoin(next_page) , callback=self.ProblemContents)
			else:
				print ("SOME ERROR OCCURED ! SORRY !!")




	"""
		-> Creates inputs and Expected outputs
		-> For problemA , Eg : input1A , output1A , input2A , output2A etc
		-> For each problem one output.txt file is created for Actual outputs
		-> That can be checked with output1A , output1B etc during contest  
	"""

	def ProblemContents(self ,response):
		p = str(response.url)[-1]							# Problem Alphabet


		os.chdir(self.tmp)
		os.chdir("problem" + p)
		f = open("output.txt" , "w")						# output.txt file is created
		f.close()



		# Input and Output files are created

		probs = list(string.ascii_uppercase)

		k = len(response.xpath(".//div[@class='sample-test']/div"))
		for i in range(1 , k+1 , 1):
			s = response.xpath(".//div[@class='sample-test']/div[" + str(i) + "]/pre/text()").extract()
			os.chdir(self.tmp)
			os.chdir("problem" + p)
			if i%2!=0:										# INPUT	
				f = open("input" + str(int(i/2) + 1) + p + ".txt" , "w")
			else: 											# OUTPUT
				f = open("output" + str(int(i/2)) + p + ".txt" , "w")
			for j in s:
				f.write(j+"\n")
			f.close()

		# OK DONE
