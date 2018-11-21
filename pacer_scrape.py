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

def get_cookie_value(opener, encoded_credentials):
	#Hit this site after logging in
	#in order to get the cookie value
	#https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout

	login_page = 'https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout'
	login_page_request = urllib2.Request(login_page)

	login_page_response = opener.open(login_page_request , encoded_credentials)
	login_page_contents = login_page_response.read()

	soup = BeautifulSoup(login_page_contents, 'html.parser')
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

	opener = urllib2.build_opener()
	urllib2.install_opener(opener)

	creds = {'login': username, 'key': password}
	encoded_login_creds = urllib.urlencode(creds)

	pacer_session_cookie_value = get_cookie_value(opener, encoded_login_creds)

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
	get_case_details(opener, case_details_page_contents)


def save_webpage_and_get_page_path(page_contents=''):
	file_path = '/home/mis/Training/Contents/'
	file_name = 'case_details.html'
	file_object = open(file_path + file_name, "w+")
	file_object.write(page_contents)
	file_object.close()

def get_case_details(opener, case_details_page_contents):
	soup =  BeautifulSoup(case_details_page_contents, 'html.parser')

	table_contents = soup.find_all('tr')

	for t_rows in table_contents:
		t_data = t_rows.find_all('td')

		for td in t_data:
			if '-' in td.text:
				case_number = td.text
				print 'case_number:\t', case_number

			elif 'filed' in td.text:
				required_date = td.text
				try:
					case_filed_date = required_date.split()[1]
					case_closed_date = required_date.split()[3]
				except:
					case_filed_date = ''
					case_closed_date = ''

				print 'case_filed_date', case_filed_date
				print 'case_closed_date', case_closed_date

			else:
				parties_involved = td.text
				print 'parties_involved:\t', parties_involved
		#break

	#Get links of all the cases
	case_details_url_list = soup.select('td a')
	case_details_dict = {}
	case_details_list = []
	case_count = 0

	for case_detail in case_details_url_list:
		base_url = 'https://dcecf.psc.uscourts.gov/cgi-bin'
		current_case_url = case_detail['href'] #Get the link of a particular case
		current_case_response = opener.open(base_url + '/' + current_case_url)
		current_case_contents = current_case_response.read()

	    #Generate additional info
		case_contents_soup = BeautifulSoup(current_case_contents, 'html.parser')
		additional_info_links_list = case_contents_soup.select('td a')
		additonal_info_json = {}

		for additional_info in additional_info_links_list:

			additional_info_name = additional_info.text
			additional_info_link = additional_info['href']
			additonal_info_json[additional_info_name] = additional_info_link

			case_count += 1


		print "additional_info_json:\t", additonal_info_json

		#break



login_pacer()
