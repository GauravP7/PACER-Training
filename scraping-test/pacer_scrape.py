#!/py-virtualenv/ENV/bin/python
import urllib
import urllib2
import re
import cookielib, urllib2
from bs4 import BeautifulSoup

'''
Steps involed in the program for retrieving the data from PACER website:

Step-1 of 10: Hit the login page of the PACER training site.
			  URL: https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout

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

Step-8 of 10: Open each of the links of Case Number from URL in Step-4 and
			  fetch the case information such as Case Number, parties involved,
			  Case filed and terminated dates.

Step-9 of 10: Fetch the data related to the additional info and
			  create the appropriate JSON data structure.

Step-10 of 10: Logout
'''

'''
Summary
Class Name: SearchCriteria
Inherits: None
Description: Class holds the search criteria as mentioned in the Schema.
			 The search criteria has to be sent to the construtor during object creation,
			 for initialization.
Member functions:
		1. print_search_criteria()
'''
class SearchCriteria():
	user_type = ''
	all_case_ids = 0
	case_number = ''
	case_status = ''
	from_filed_date = ''
	to_filed_date = ''
	from_last_entry_date = ''
	to_last_entry_date = ''
	nature_of_suit = ''
	cause_of_action = ''
	last_name = ''
	first_name = ''
	middle_name = ''
	type = ''
	exact_matches_only = 0

	#Default constructor of the class
	def __init__(self, user_type='', all_case_ids=0, case_number='', case_status='',
	from_filed_date='1/1/2007', to_filed_date='10/1/2008', from_last_entry_date='', to_last_entry_date='',
	nature_of_suit='', cause_of_action='', last_name='', first_name='', middle_name='',
	type='', exact_matches_only=0):
		self.user_type = user_type
		self.all_case_ids = all_case_ids
		self.case_number = case_number
		self.case_status = case_status
		self.from_filed_date = from_filed_date
		self.to_filed_date = to_filed_date
		self.from_last_entry_date = from_last_entry_date
		self.to_last_entry_date = to_last_entry_date
		self.nature_of_suit = nature_of_suit
		self.cause_of_action = cause_of_action
		self.last_name = last_name
		self.first_name = first_name
		self.middle_name = middle_name
		self.type = type
		self.exact_matches_only = exact_matches_only

	'''
	Summary
	Method Name: print_search_criteria
	Description: Prints all the search criteria used in for Querying the data from the website
	Arguments: self
	'''
	def print_search_criteria(self):
		print "***************************************************"
		print "Search Criteria are:"
		print "user_type:\t", self.user_type
		print "all_case_ids:\t", self.all_case_ids
		print "case_number:\t", self.case_number
		print "case_status:\t", self.case_status
		print "query_filed_from:\t", self.from_filed_date
		print "query_filed_to:\t", self.to_filed_date
		print "lastentry_from:\t", self.from_last_entry_date
		print "lastentry_to:\t", self.to_last_entry_date
		print "nature_of_suit:\t", self.nature_of_suit
		print "cause_of_action:\t", self.cause_of_action
		print "last_name:\t", self.last_name
		print "first_name:\t", self.first_name
		print "middle_name:\t", self.middle_name
		print "person_type:\t", self.type
		print "exact_matches_only:\t", self.exact_matches_only
		print "***************************************************"

'''
Summary
Class Name: PacerScrape
Inherits: None
Description: Class is used to scrape the case related data from the PACER training website.
Member functions:
		1. get_cookie_value(opener, encoded_credentials)
		2. get_url_random_numbers(query_page_contents)
		3. login_pacer(username=, password=)
		4. save_webpage_and_get_page_path(page_contents)
		5. save_case_details(opener, case_details_page_contents)
		6. logout(opener)
'''
class PacerScrape():

	'''
	Summary
	Method Name: get_cookie_value
	Description: Used to get the value of the cookie named 'PacerSession' from the HTML page
	Arguments: self, opener, encoded_credentials
	'''
	def get_cookie_value(self, opener, encoded_credentials):
		#Hit this site after logging in
		#in order to get the cookie value
		#https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout

		login_page = 'https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout'
		login_page_request = urllib2.Request(login_page)

		login_page_response = opener.open(login_page_request , encoded_credentials)
		login_page_contents = login_page_response.read()

		login_page_soup = BeautifulSoup(login_page_contents, 'html.parser')
		#Extract cookie value
		script_value = login_page_soup.script.get_text()

		#print script_value
		pacer_session_cookie_value = re.split( 'PacerSession |, |;', re.findall(r'"(.*?)"', script_value)[0])[0]

		return pacer_session_cookie_value

	'''
	Summary
	Method Name:
	Description:
	Arguments:
	'''
	def get_url_random_numbers(self, query_page_contents):

		MINIMUM_FORM_NUMBER_SIZE = 5
		#Extract random numbers
		query_page_soup = BeautifulSoup(query_page_contents, 'html.parser')
		form_action_value = query_page_soup.find('form').get('action')
		action_content = re.findall(r"[0-9]*", form_action_value)

		#Extract only the number part
		for form_number in action_content:
			if form_number.isdigit() and len(form_number) >= MINIMUM_FORM_NUMBER_SIZE:
				required_form_number = form_number

		return required_form_number

	'''
	Summary
	Method Name: login_pacer
	Description: Used to login into the PACER training website and make related function calls
	Arguments: self, username, password
	'''
	def login_pacer(self, username = 'tr1234', password = 'Pass!234'):

		opener = urllib2.build_opener()
		urllib2.install_opener(opener)

		credentials = {'login': username, 'key': password}
		encoded_login_creds = urllib.urlencode(credentials)

		'''
		################################################################################
		Step-1 of 10: Hit the login page of the PACER training site.
					  URL: https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout

		Step-2 of 10: Enter the credentials provided by the training website and login.
					  Username="tr1234", Password="Pass!234"
					  And be redirected to the page with case information.
		################################################################################
		'''

		#Get the session cookie value
		pacer_session_cookie_value = self.get_cookie_value(opener, encoded_login_creds)

		#Add the required headers
		opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')]

		opener.addheaders.append(('Referer','https://dcecf.psc.uscourts.gov/cgi-bin/ShowIndex.pl'))

		opener.addheaders.append(('Cookie', pacer_session_cookie_value ))

		'''
		################################################################################
		Step-3 of 10: Hit the URL: https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl?660038495246212-L_1_0-1
					  to enter the data for querying.

		Step-4 of 10: Enter the values "1/1/2007" and "10/1/2007"
					  in the "Filed Date" column and run the query.

		Step-5 of 10: We will be redirected to the page that contains the case related information.
					  Get the URL of that page.
		################################################################################
		'''

		query_page_url = 'https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl'
		query_page_response = opener.open(query_page_url)
		query_page_contents = query_page_response.read()

		#By here we get the contents of the "Query" page
		required_form_number = self.get_url_random_numbers(query_page_contents)

		#Now we start hitting the content page
		data_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl?" + required_form_number + "-L_1_0-1"

		search_criteria = SearchCriteria()
		search_criteria.print_search_criteria()

		#The parameters to be encoded and sent as a search criteria
		query_parameters = {
			'UserType': search_criteria.user_type,
			'all_case_ids': search_criteria.all_case_ids,
			'case_num': search_criteria.case_number,
			'Qry_filed_from': search_criteria.from_filed_date,
			'Qry_filed_to': search_criteria.to_filed_date,
			'lastentry_from': search_criteria.from_last_entry_date,
			'lastentry_to': search_criteria.to_last_entry_date,
			'last_name': search_criteria.last_name,
			'first_name': search_criteria.first_name,
			'middle_name': search_criteria.middle_name,
			'person_type': search_criteria.type
		}

		query_parameters_encoded = urllib.urlencode(query_parameters)
		query_request = urllib2.Request(data_page_url, query_parameters_encoded)
		query_response = opener.open(query_request)

		case_details_page_contents = query_response.read()

		self.save_webpage_and_get_page_path(case_details_page_contents)

		#Start scraping for case details
		self.save_case_details(opener, case_details_page_contents)

	 	#logout from the website
		#self.logout(opener)


	'''
	Summary
	Method Name: save_webpage_and_get_page_path
	Description: Saves the HTML code of the Webpage containing the Case details
	Arguments: self, page_contents
	'''
	def save_webpage_and_get_page_path(self, page_contents=''):
		'''
		################################################################################

		Step-6 of 10: Hit the URL from Step-5.

		Step-7 of 10: Save the Web page (HTML content) in a folder and display the path of the file.

		################################################################################
		'''
		saved_webpage_file_path = '/home/mis/Training/Contents/'
		saved_webpage_file_name = 'case_details.html'
		page_path = saved_webpage_file_path + saved_webpage_file_name
		file_object = open(page_path, "w+")
		file_object.write(page_contents)
		file_object.close()
		print "page_path:\t", page_path
		print "***************************************************"

	'''
	Summary
	Method Name: save_case_details
	Description: Saves the case details and Additional info as mentioned in the Schema
	Arguments: self, opener, case_details_page_contents
	'''
	def save_case_details(self, opener, case_details_page_contents):
		case_details_page_soup =  BeautifulSoup(case_details_page_contents, 'html.parser')

		table_contents = case_details_page_soup.find_all('tr')[:-3000]

		'''
		################################################################################
		Step-8 of 10: Open each of the links of Case Number from URL in Step-4 and
					  fetch the case information such as Case Number, parties involved,
					  Case filed and terminated dates.
		################################################################################
		'''
		for t_rows in table_contents:
			t_data = t_rows.find_all('td')
			case_details_count = 0

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
						case_filed_date = required_date.split()[1]
						case_closed_date = ''

					print 'case_filed_date:\t', case_filed_date
					print 'case_closed_date:\t', case_closed_date

				else:
					parties_involved = td.text
					print 'parties_involved:\t', parties_involved

				case_details_count += 1

		print "***************************************************"

		'''
		################################################################################
		Step-9 of 10: Fetch the data related to the additional info and
					  create the appropriate JSON data structure.
		################################################################################
		'''
		#Get links of all the cases
		case_details_url_list = case_details_page_soup.select('td a')
		case_details_dict = {}
		case_details_list = []
		additional_info_count = 0

		for case_detail in case_details_url_list:
			base_url = 'https://dcecf.psc.uscourts.gov/cgi'
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

			additional_info_count += 1

			print "Additional info are:\t"
			print "additional_info_json:\t", additonal_info_json
			print "***************************************************"

			if additional_info_count >= 5:
				break

	'''
	Summary
	Method Name: logout
	Description: Logout from the website
	Arguments: self, opener
	'''
	def logout(self, opener):
		'''
		################################################################################
		Step-10 of 10: Logout
		################################################################################
		'''
		logout_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout"
		opener.open(logout_page_url)
		print "Logged out successfully from the website"

#Instantiate the PacerScrape class
pacer_scraper = PacerScrape()

#Call the login_pacer method and begin the execution
pacer_scraper.login_pacer()
