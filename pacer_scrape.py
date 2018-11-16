#!/py-virtualenv/ENV/bin/python

import time
import urllib
import base64
import urllib2

'''
Steps involed in the program for retrieving the data from PACER website:

Step-1 of 10: Hit the query page of the PACER training site.
			  URL: https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl

Step-2 of 10: Enter the credentials provided by the training website and login.
			  Username="tr1234", Password="Pass!234"
			  And be redirected to the page with case information.

Step-3 of 10: Hit the URL: https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl
			  to enter the data for querying. 

Step-4 of 10: Enter the values "1/1/2007" and "10/1/2007" 
			  in the "Filed Date" column and run the query.		

Step-5 of 10: We will be redirected to the page that contains the case related information.
			  Get the URL of that page.

Step-6 of 10: Hit the URL from Step-5.

Step-7 of 10: Save the Web page (HTML content) in a folder and display the path of the file.

Step-8 of 10: Open each of the links of Case Number from URL in Step-4 and 
			  fetch the case information such as Case Number, parties involved, 
			  Case filed and terminated dates.
		
Step-9 of 10: Fetch the data related to the additional info and 
			  create the appropriate JSON data structure.
		
Step-10 of 10: Logout
'''
	
def login_into_pacer():
	
	username = 'tr1234'
	password = 'Pass!234'
	
	Qry_filed_from = '1/1/2007'
	Qry_filed_to = '10/1/2008'
	
	authentication_url = "https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl"
		
	login_credentials = { 'login': username, 'key': password }
	
	login_data = urllib.urlencode(login_credentials)
	
	request = urllib2.Request(authentication_url, login_data)
	
	login_response = urllib2.urlopen(request)
	cookie = login_response.headers.get('Set-Cookie')
	
	#Enter the data to be queried and make new request
	
	query_request = urllib2.Request(authentication_url, urllib.urlencode( { Qry_filed_from : '1/1/2007', Qry_filed_to : '10/1/2008' } ))
	
	query_request.add_header('cookie', cookie)
	
	query_response = urllib2.urlopen(query_request)
		
	login_result = login_response.read()
	
	#Qry_filed_from Qry_filed_to
	
	print(login_result)
	print "Login Successful"
	print "\n***************************************************************\n"

	
def open_query_page():
	query_url = "https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl"
	
	query_request = urllib2.Request(query_url)
	query_resp = urllib2.urlopen(query_request)
	
	print query_resp.read()
	print "\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"

	
#Step-1 and 2 of 9: Hit the query page of the PACER training site.
#					URL: https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl

login_into_pacer()

#Step-3 of 9: Hit the URL: https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl
#			  to enter the data for querying. 
#open_query_page()
