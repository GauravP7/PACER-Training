#!/py-virtualenv/ENV/bin/python

import pdb
import time
import urllib
import urllib2
import re
from cookielib import CookieJar
from bs4 import BeautifulSoup

'''
Steps involed in the program for retrieving the data from PACER website:

Step-1 of 10: Hit the query page of the PACER training site.
			  URL: https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl

Step-2 of 10: Enter the credentials provided by the training website and login.
			  Username="tr1234", Password="Pass!234"
			  And be redirected to the page with case information.

Step-3 of 10: Hit the URL: https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl?660038495246212-L_1_0-1
			  to enter the data for querying. 

Step-4 of 10: Enter the values "1/1/2007" and "10/1/2007" 
			  in the "Filed Date" column and run the query.		

Step-5 of 10: We will be redirected to the page that contains the case related information.
			  Get the URL of that page.

Step-6 of 10: Hit the URL from Step-5.

Step-7 of 10: Save the Web page (HTML content) in a folder and display the path of the file.
import re
Step-8 of 10: Open each of the links of Case Number from URL in Step-4 and 
			  fetch the case information such as Case Number, parties involved, 
			  Case filed and terminated dates.
		
Step-9 of 10: Fetch the data related to the additional info and 
			  create the appropriate JSON data structure.
		
Step-10 of 10: Logout
'''

#Get html data for scraping

	
def login_into_pacer():

	authentication_url = "https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl"

	username = 'tr1234'
	password = 'Pass!234'
	
	cj = CookieJar()
	
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	
	# input-type values from the html Login form
	login_credentials = { 'login': username, 'key': password }
	
	login_data = urllib.urlencode(login_credentials)
		
	login_response = opener.open(authentication_url, login_data)
	
	login_page_content =  login_response.read()
	
	#Extract the unique random number from the form
	#First find the form tag and find the action element
	soup = BeautifulSoup(login_page_content, 'html.parser')
	
	#print(soup.prettify())
	
	form_action_value = soup.find('form').get('action')
	
	action_content = re.findall(r"[0-9]*", form_action_value)

	#Extract only the number part
	for i in action_content:
		if i.isdigit() and len(i) >=5:
			required_form_number = i	
	
	
	#By here we get the contents of the "Query" page
	#Now we start hitting the content page
	data_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl?" + required_form_number + "-L_1_0-1"
	
	#print "URL:\t" + data_page_url 
	
	query_parameters = { 
						 'UserType': '', 'all_case_ids': '0', 'case_num': '',
						 'Qry_filed_from' : '1/1/2007', 'Qry_filed_to' : '10/1/2008',
						 'lastentry_from': '', 'lastentry_to': '', 'last_name': '',
						 'first_name': '', 'middle_name': '', 'person_type': ''
						}

	query_parameters_url_encoded = urllib.urlencode(query_parameters)
	
	contents = opener.open(data_page_url, query_parameters_url_encoded).read()

	print contents


	
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
