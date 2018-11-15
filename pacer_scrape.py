#! /path/to/ENV/bin/python

'''
Steps involed in the program for retrieving the data from PACER website:

Step-1: Hit the login page of the PACER training site.
		URL: https://dcecf.psc.uscourts.gov/cgi-bin/login.pl

Step-2: Enter the credentials provided by the training website and login.
		Username="tr1234", Password="Pass!234"
		And be redirected to the page with case information.

Step-3: Hit the URL: https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl
		to enter the data for querying. 

Step-4: Enter the values "1/1/2007" and "10/1/2007" 
		in the "Filed Date" column and run the query.		

Step-4: We will be redirected to the page that contains the case realted information.
		Get the URL of that page.

Step-5: Hit the URL from Step-4.

Step-6: Save the Web page (HTML content) in a folder and display the path of the file.

Step-7: Open each of the links of Case Number from URL in Step-4 and 
		fetch the case information such as Case Number, parties involved, 
		Case filed and terminated dates.
		
Step-8: Fetch the data related to the additional info and 
		create the appropriate JSON data structure.
		
Step-9: Logout
'''

import time
import urllib
import base64
import urllib2, cookielib
	
def login_into_pacer():
	
	username = 'tr1234'
	password = 'Pass!234'
	
	authentication_url = "https://dcecf.psc.uscourts.gov/cgi-bin/login.pl"
		
	values = { 'login': username, 'key': password }
	
	data = urllib.urlencode(values)
	
	req = urllib2.Request(authentication_url, data)
	
	response = urllib2.urlopen(req)
	result = response.read()
	
	
	print result	
	#print(result)
	print "Login Successful"
	print "\n***************************************************************\n"

	
def open_query_page():
	query_url = "https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl"
	
	query_resp = urllib2.urlopen(query_url)
	
	print query_resp.read()
	print "\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"

	
#Step-1 and 2 Hit the login Page and enter credentials
login_into_pacer()

#Step-3 Hit the query page
open_query_page()
