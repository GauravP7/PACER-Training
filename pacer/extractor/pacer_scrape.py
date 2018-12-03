#!/py-virtualenv/ENV/bin/python
import sys
import urllib
import urllib2
import re
from bs4 import BeautifulSoup
import json

# [ Step 1 of 9 ] : Hit the first page of PACER training site and Login.
#
# [ Step 2 of 9 ] : Validate the Login.
#
# [ Step 3 of 9 ] : Parse the contents and get cookie.
#
# [ Step 4 of 9 ] : Query as per the input criteria.
#
# [ Step 5 of 9 ] : Save the Web page (HTML content) in a folder.
#
# [ Step 6 of 9 ] : Print the page path.
#
# [ Step 7 of 9 ] : Print the Search Criteria.
#
# [ Step 8 of 9 ] : Print the case details.
#
# [ Step 9 of 9 ] : Logout from the website.

class Extractor():
	"""
		Class holds the search criteria as mentioned in the Schema.
		Inherits:
				None
	"""

	def __init__(self):

		#Initialize the search criteria
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

class Downloader():
	"""
		Class is used to scrape the case related data from the PACER training website.
		Inherits:
				None
		Member functions:
				1. login_pacer(self)
				2. get_cookie_value(self, login_page_contents)
				3. validate_login_success(self, login_page_contents)
				4. get_case_details_page_contents(self)
				5. save_webpage_with_case_details(self, page_contents)
				6. parse_case_details(self, case_details_page_contents)
				7. logout(self)
				8. terminate_with_error_message(self)
	"""

	def __init__(self):
		"""
			Default constructor
			Tasks:
			 1. sets up the opener
			 2. Initializes login credentials
			 3. Initializes cookie
		"""

		self.opener = urllib2.build_opener()
		urllib2.install_opener(self.opener)

		#Initialize the cookie_value
		self.pacer_session_cookie_value = ""

		#Initializes the login credentials
		self.username = 'tr1234'
		self.password = 'Pass!234'

	def login_pacer(self):
		"""
			Used to login into the PACER training website and make related function calls.
			Arguments:
					self
			Returns:
					pacer_session_cookie_value
		"""

		credentials = {'login': self.username, 'key': self.password}
		encoded_login_credentials = urllib.urlencode(credentials)
		login_page = 'https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout'
		login_page_request = urllib2.Request(login_page)
		login_page_response = self.opener.open(login_page_request , encoded_login_credentials)
		login_page_contents = login_page_response.read()
		return login_page_contents

	def get_cookie_value(self, login_page_contents):
		"""
			Used to get the cookie value.
			Arguments:
					self, login_page_contents
		"""
		login_page_soup = BeautifulSoup(login_page_contents, 'html.parser')

		#The 'html.parser' is unnecessay since it is Default to BeautifulSoup.
		#However, it is better to use it to avoid the WARNING.
		#Extract cookie value
		script_value = login_page_soup.script.get_text()

		#Example
		#Input: "PacerSession=JjRYJFwy9L7sFOycTEI3I18YOhazqPx7OEdgtw235ClZlnQMrTdgivMC6FQ5iHAUhfu0xECTDmcCrrjzH4CFqBKq4RhbvKzrG7lcFpNL72OwB76QicEUFSIKY3DSoEiz;"
		#Output: JjRYJFwy9L7sFOycTEI3I18YOhazqPx7OEdgtw235ClZlnQMrTdgivMC6FQ5iHAUhfu0xECTDmcCrrjzH4CFqBKq4RhbvKzrG7lcFpNL72OwB76QicEUFSIKY3DSoEiz
		self.pacer_session_cookie_value = re.split( 'PacerSession |, |;', re.findall(r'"(.*?)"', script_value)[0])[0]

		#Add the required headers to the opener
		self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')]
		self.opener.addheaders.append(('Referer','https://dcecf.psc.uscourts.gov/cgi-bin/ShowIndex.pl'))
		self.opener.addheaders.append(('Cookie', self.pacer_session_cookie_value ))

	def validate_login_success(self, login_page_contents):
		"""
			Returns True if login is successful. returns False otherwise.
			Arguments:
					self, login_page_contents
		"""

		login_page_soup = BeautifulSoup(login_page_contents, 'html.parser')
		login_page_h3_tags = login_page_soup.find_all('h3')

		for h3_tag in login_page_h3_tags:
			if "U.S. DISTRICT COURT" in str(h3_tag):
				return True

		return False

	def get_case_details_page_contents(self):
		"""
			 Hits the query URL and returns the case details page
			 after querying with appropriate search criteria
			 Arguments:
			 		self
			Returns:
					case_details_page_contents

		"""

		query_page_url = 'https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl'
		query_page_response = self.opener.open(query_page_url)
		query_page_contents = query_page_response.read()
		minimum_size_of_form_number = 5

		#Extract random numbers
		query_page_soup = BeautifulSoup(query_page_contents, 'html.parser')
		form_action_value = query_page_soup.find('form').get('action')
		action_content = re.findall(r"[0-9]*", form_action_value)

		# Extract only the number part
		for form_number in action_content:
			if form_number.isdigit() and len(form_number) >= minimum_size_of_form_number:
				required_form_number = form_number
				break

		#Now we start hitting the content page
		data_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl?" + required_form_number + "-L_1_0-1"
		extractor_object = Extractor()

		#The parameters to be encoded and sent as a search criteria
		query_parameters = {
			'UserType': extractor_object.user_type,
			'all_case_ids': extractor_object.all_case_ids,
			'case_num': extractor_object.case_number,
			'Qry_filed_from': extractor_object.from_filed_date,
			'Qry_filed_to': extractor_object.to_filed_date,
			'lastentry_from': extractor_object.from_last_entry_date,
			'lastentry_to': extractor_object.to_last_entry_date,
			'last_name': extractor_object.last_name,
			'first_name': extractor_object.first_name,
			'middle_name': extractor_object.middle_name,
			'person_type': extractor_object.type
		}

		query_parameters_encoded = urllib.urlencode(query_parameters)
		query_request = urllib2.Request(data_page_url, query_parameters_encoded)
		query_response = self.opener.open(query_request)
		case_details_page_contents = query_response.read()
		return case_details_page_contents

	def save_all_case_details_page(self, case_details_page_contents):
		case_details_soup = BeautifulSoup(case_details_page_contents, 'html.parser')
		case_links = case_details_soup.find_all('a', class_='')[:10]
		case_links_list = []
		for case_link in case_links:
			if case_link:
				case_links_list.append(case_link['href'])
			else:
				pass
		case_details_base_link = 'https://dcecf.psc.uscourts.gov/cgi-bin/'

		#open each link and save each page
		case_count = 1
		for case_link in case_links_list:
			case_details_page_response = self.opener.open( case_details_base_link + case_link )
			case_name = 'case_' + str(case_count)
			case_file_object = open('/home/mis/DjangoProject/pacer/extractor/Contents/case/' + case_name + '.html', 'w+')
			case_file_object.write(case_details_page_response.read())
			case_count += 1
			case_file_object.close()
		return case_count

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
		exit(0)

class Parser():

	def parse_case_details_page(self, file_name):

		#Parse for case details
		additional_info_json = {}
		additional_info_base_url = 'https://dcecf.psc.uscourts.gov/cgi-bin'
		case_file = open('/home/mis/DjangoProject/pacer/extractor/Contents/case/' + file_name + '.html', 'r')
		contents = BeautifulSoup(case_file, 'html.parser')
		center_tag =  contents.find_all('center')
		case_details = re.split('Date filed: |Date terminated: |Date of last filing: | All Defendants ', center_tag[0].text)
		case_number = case_details[0]
		parties_involved = case_details[1]
		case_filed_date = case_details[2]
		if len(case_details) > 3:
			case_closed_date = case_details[3]
		else:
			case_closed_date = ''
		additional_info_links = contents.find_all('a', class_='')
		for additional_info in additional_info_links:
			additional_info_name = additional_info.text
			additional_info_link = additional_info_base_url + additional_info['href']
			additional_info_json[additional_info_name] = additional_info_link
		additional_info_json = json.dumps(additional_info_json)

		#Perform tuple packing
		required_case_details = (case_number, parties_involved, case_filed_date, case_closed_date, additional_info_json)
		return required_case_details
