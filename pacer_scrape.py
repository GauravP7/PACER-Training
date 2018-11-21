#!/py-virtualenv/ENV/bin/python
import os
import urllib
import urllib2
import re
import cookielib, urllib2
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
def get_cookie_value(encoded_credentials):
	#Hit the third page link
	#Hit this site after logging in
	#in order to get the cookie value
	#https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout

	third_page = 'https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout'
	third_page_request = urllib2.Request(third_page)

	third_page_response = urllib2.urlopen(third_page_request , encoded_credentials)
	third_page_contents = third_page_response.read()

	soup = BeautifulSoup(third_page_contents, 'html.parser')
	#Extract cookie value
	script_value = soup.script.get_text()

	#print script_value
	pacer_session_cookie_value = re.split( 'PacerSession |, |;', re.findall(r'"(.*?)"', script_value)[0])[0]

	return pacer_session_cookie_value

def get_url_random_numbers(query_page_contents):
	#Extract random numbers
	soup = BeautifulSoup(query_page_contents, 'html.parser')
	form_action_value = soup.find('form').get('action')
	action_content = re.findall(r"[0-9]*", form_action_value)
	#Extract only the number part
	for i in action_content:
		if i.isdigit() and len(i) >= 5:
			required_form_number = i

	return required_form_number

def login_pacer(username = 'tr1234', password = 'Pass!234'):

	#Set the cookie jar and build_opener
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)

	#Hit the first page link
	first_page = 'https://www.pacer.gov/announcements/general/train.html'
	first_page_request = urllib2.Request(first_page)
	first_page_response = urllib2.urlopen(first_page_request)

	#Hit the second page link
	second_page= 'https://dcecf.psc.uscourts.gov/cgi-bin/ShowIndex.pl'
	second_page_request = urllib2.Request(second_page)
	second_page_response = urllib2.urlopen(second_page_request)

	creds = {'login': username, 'key': password}
	encoded_login_creds = urllib.urlencode(creds)

	pacer_session_cookie_value = get_cookie_value(encoded_login_creds)

	opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')]

	opener.addheaders.append(('Referer','https://dcecf.psc.uscourts.gov/cgi-bin/ShowIndex.pl'))

	opener.addheaders.append(('Cookie', pacer_session_cookie_value ))

	query_page_url = 'https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl'
	query_page_response = opener.open(query_page_url)
	query_page_contents = query_page_response.read()

	#By here we get the contents of the "Query" page
	required_form_number = get_url_random_numbers(query_page_contents)

	#Now we start hitting the content page
	data_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl?" + required_form_number + "-L_1_0-1"

	query_parameters = {
	'UserType':'',
	'all_case_ids':0,
	'case_num':'',
	'Qry_filed_from':'1/1/2007',
	'Qry_filed_to':'10/1/2008',
	'lastentry_from':'',
	'lastentry_to':'',
	'last_name':'',
	'first_name':'',
	'middle_name':'',
	'person_type':''
	}

	query_parameters_encoded = urllib.urlencode(query_parameters)
	query_request = urllib2.Request(data_page_url, query_parameters_encoded)
	query_response = opener.open(query_request)

	case_details_page_contents = query_response.read()
	#print query_response.read()
	save_webpage_and_get_page_path(case_details_page_contents)

	#start scraping for case case_details
	get_case_details(case_details_page_contents)


def save_webpage_and_get_page_path(page_contents=''):
	file_path = '/home/mis/Training/Contents/'
	file_name = 'case_details.html'
	file_object = open(file_path + file_name, "w+")
	file_object.write(page_contents)
	file_object.close()

def get_case_details(case_details_page_contents):
	soup =  BeautifulSoup(case_details_page_contents, 'html.parser')
	tr_tags = soup.find_all('tr')

	print tr_tags


login_pacer()
