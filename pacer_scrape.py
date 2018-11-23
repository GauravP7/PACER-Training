#!/py-virtualenv/ENV/bin/python
import sys
import urllib
import urllib2
import re
import cookielib
from bs4 import BeautifulSoup

# [ Step 1 of 7 ]	:	Hit the first page of PACER training site to set the cookie.
#  						URL: https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout
#
# [ Step 2 of 7 ]	:	Login to training website.
#  						Get the appropriate cookie value from the page we get after login.
#
# [ Step 3 of 7 ]	:	Validate the login.
#
# [ Step 4 of 7 ]	:	Query as per the input criteria.
#
# [ Step 5 of 7 ]	:	Save the Web page (HTML content) in a folder.
#
# [ Step 6 of 7 ]	:	Save the case details.
#
# [ Step 7 of 7 ]	:	Logout from the website.

class SearchCriteria():
	"""
		Class holds the search criteria as mentioned in the Schema.

		Inherits:
				None

		Member functions:
				1. print_search_criteria()
	"""

	def __init__(self):
		self.user_type = ''
		self.all_case_ids = 0
		self.case_number = ''
		self.case_status = ''
		self.from_filed_date = '1/1/2007'
		self.to_filed_date = '1/1/2008'
		self.from_last_entry_date = ''
		self.to_last_entry_date = ''
		self.nature_of_suit = ''
		self.cause_of_action = ''
		self.last_name = ''
		self.first_name = ''
		self.middle_name = ''
		self.type = ''
		self.exact_matches_only = 0


	def print_search_criteria(self):
		"""
			Prints all the search criteria used in for Querying the data from the website

			Arguments:
					self
		"""

		print "***************************************************"
		print "Search Criteria are:"
		print "user_type:\t", self.user_type
		print "all_case_ids:\t", self.all_case_ids
		print "case_number:\t", self.case_number
		print "case_status:\t", self.case_status
		print "from_filed_date:\t", self.from_filed_date
		print "to_filed_date:\t", self.to_filed_date
		print "from_last_entry_date:\t", self.from_last_entry_date
		print "to_last_entry_date:\t", self.to_last_entry_date
		print "nature_of_suit:\t", self.nature_of_suit
		print "cause_of_action:\t", self.cause_of_action
		print "last_name:\t", self.last_name
		print "first_name:\t", self.first_name
		print "middle_name:\t", self.middle_name
		print "type:\t", self.type
		print "exact_matches_only:\t", self.exact_matches_only
		print "***************************************************"


class PacerScrape():
	"""
		Class is used to scrape the case related data from the PACER training website.

		Inherits:
				None

		Member functions:
				1.  login_pacer(self)
				2.  validate_login_success(self, pacer_session_cookie_value)
				3.	get_case_details_page_contents(self)
				4.	save_webpage_with_case_details(self, page_contents)
				5.	save_webpage_with_case_details(self, page_contents)
				6.	save_case_details(self, case_details_page_contents)
				7.	logout(self)
				8.	terminate_with_error_message(self)
	"""

	def __init__(self):
		"""
			Default constructor for setting up the opener
		"""
		self.opener = urllib2.build_opener()
		urllib2.install_opener(self.opener)

	def login_pacer(self):
		"""
			Used to login into the PACER training website and make related function calls.

			Arguments:
					self, username, password

			Returns:
					pacer_session_cookie_value
		"""

		username = 'tr1234'
		password = 'Pass!234'

		credentials = {'login': username, 'key': password}
		encoded_login_credentials = urllib.urlencode(credentials)

		login_page = 'https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout'

		pacer_session_cookie_value = ""

		# [ Step 1 of 7 ]	:	Hit the cookie page of the PACER training site.
		#  						URL: https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout
		try:
			login_page_request = urllib2.Request(login_page)

			login_page_response = self.opener.open(login_page_request , encoded_login_credentials)
			login_page_contents = login_page_response.read()

			login_page_soup = BeautifulSoup(login_page_contents, 'html.parser')

			#The 'html.parser' is unnecessay since it is Default to BeautifulSoup.
			#However, it is better to use it to avoid the WARNING.

			#Extract cookie value
			script_value = login_page_soup.script.get_text()

			#print script_value
			pacer_session_cookie_value = re.split( 'PacerSession |, |;', re.findall(r'"(.*?)"', script_value)[0])[0]

		except:
			print sys._getframe().f_code.co_name
			self.terminate_with_error_message()

		#Add the required headers
		self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')]

		self.opener.addheaders.append(('Referer','https://dcecf.psc.uscourts.gov/cgi-bin/ShowIndex.pl'))

		self.opener.addheaders.append(('Cookie', pacer_session_cookie_value ))

		return pacer_session_cookie_value

	def validate_login_success(self, pacer_session_cookie_value):
		"""
			Returns True if login is successful. returns False otherwise.

			Arguments:
					self, username, password
		"""

		if pacer_session_cookie_value is None or pacer_session_cookie_value == '':
			return False

		return True

	def get_case_details_page_contents(self):
		"""
			 Hits the query URL and returns the case details page
			 after querying with appropriate search criteria

			 Arguments:
			 		self, username, password

			Returns:
					case_details_page_contents

		"""

		query_page_url = 'https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl'
		query_page_response = self.opener.open(query_page_url)
		query_page_contents = query_page_response.read()

		#By here we get the contents of the "Query" page
		MINIMUM_FORM_NUMBER_SIZE = 5
		#Extract random numbers
		query_page_soup = BeautifulSoup(query_page_contents, 'html.parser')
		form_action_value = query_page_soup.find('form').get('action')
		action_content = re.findall(r"[0-9]*", form_action_value)

		# Extract only the number part
		for form_number in action_content:
			if form_number.isdigit() and len(form_number) >= MINIMUM_FORM_NUMBER_SIZE:
				required_form_number = form_number

		#Now we start hitting the content page
		data_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl?" + required_form_number + "-L_1_0-1"

		search_criteria = SearchCriteria()

		#Print the search criteria
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
		query_response = self.opener.open(query_request)

		case_details_page_contents = query_response.read()

		return case_details_page_contents

	def save_webpage_with_case_details(self, page_contents):
		"""
			Saves the HTML code of the Webpage containing the Case details

			Arguments:
					self, page_contents

			Returns:
					page_path
		"""

		saved_webpage_file_path = '/home/mis/Training/Contents/'
		saved_webpage_file_name = 'case_details.html'
		page_path = saved_webpage_file_path + saved_webpage_file_name
		file_object = open(page_path, "w+")
		file_object.write(page_contents)
		file_object.close()
		print "page_path:\t", page_path
		print "***************************************************"

		return page_path

	def save_case_details(self, case_details_page_contents):
		"""
			Saves the case details and Additional info as mentioned in the Schema

			Arguments:
					self, opener, case_details_page_contents
		"""

		try:
			case_details_page_soup =  BeautifulSoup(case_details_page_contents, 'html.parser')

			table_contents = case_details_page_soup.find_all('tr')[:-4570]

			#The last 6 rows contain the irrelevant information
			#Hence they are discarded

			for t_rows in table_contents:
				t_data = t_rows.find_all('td')
				case_details_count = 0

				for td in t_data:
					if '-' in td.text:
						case_number = td.text
						print "case_number:\t", case_number

					elif 'filed' in td.text:
						required_date = td.text
						try:
							case_filed_date = required_date.split()[1]
							case_closed_date = required_date.split()[3]
						except:	#Hnadling exceptions for cases without closed date
							case_closed_date = ''

						print "case_filed_date:\t", case_filed_date
						print "case_closed_date:\t", case_closed_date
						case_details_count += 1
						print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

					else:
						parties_involved = td.text
						print "parties_involved:\t", parties_involved

			print "***************************************************"

			#Get links of all the cases
			case_details_url_list = case_details_page_soup.select('td a')
			case_details_dict = {}
			case_details_list = []
			additional_info_count = 0

			for case_detail in case_details_url_list:
				base_url = 'https://dcecf.psc.uscourts.gov/cgi-bin'
				current_case_url = case_detail['href'] #Get the link of a particular case
				current_case_response = self.opener.open(base_url + '/' + current_case_url)
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

				if additional_info_count >= 1:
					break

		except:
			print "Error occured when saving case details"
			print "Failed to save some or all of the case details"

	def logout(self):
		"""
			Logout from the website

			Arguments:
					self, opener
		"""

		logout_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout"
		logout_response = self.opener.open(logout_page_url)
		logout_page_contents = logout_response.read()

	def terminate_with_error_message(self):
		"""
			Terminate the program with upon unsuccessful login

			Arguments:
					self
		"""

		print "The program is terminated since the login was unsuccessful."
		print "Please check the credentials or your internet connection and try again"
		exit()
