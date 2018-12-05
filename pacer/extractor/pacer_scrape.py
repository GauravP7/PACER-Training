#!/py-virtualenv/ENV/bin/python
import os
import urllib
import urllib2
import re
import MySQLdb
import json
import datetime
from bs4 import BeautifulSoup

# [ Step 1 of 8 ] : Hit the first page of PACER training site and Login.
#
# [ Step 2 of 8 ] : Validate the Login.
#
# [ Step 3 of 8 ] : Parse the contents and get cookie.
#
# [ Step 4 of 8 ] : Query as per the input criteria.
#
# [ Step 5 of 8 ] : Save the Web page (HTML content) in a folder.
#
# [ Step 6 of 8 ] : Save the Search Criteria.
#
# [ Step 7 of 8 ] : Save the case details.
#
# [ Step 8 of 8 ] : Logout from the website.

class Extractor():
	"""
		Class holds the search criteria as mentioned in the Schema.
		Inherits:
				None
	"""

	def __init__(self):

		#settig up database connection
		self.database_connection = MySQLdb.connect(host= "",
						      user="root",
						      password="Code@mispl",
						      db="pacer_case_details")
		self.connection_cursor = self.database_connection.cursor()
		self.connection_cursor.execute("SELECT * FROM extractor ORDER BY id DESC LIMIT 1")
		extractor_search_criteria = self.connection_cursor.fetchall()
		(id,
		case_number,
		case_status,
		from_filed_date,
		to_filed_date,
		from_last_entry_date,
		to_last_entry_date,
		nature_of_suit,
		cause_of_action,
		last_name,
		first_name,
		middle_name,
		type,
		exact_matches_only) = extractor_search_criteria[0]

		if from_filed_date is not None:
			split_from_filed_date = str(from_filed_date).split('-')
			from_filed_date = split_from_filed_date[1] + '/' +  split_from_filed_date[2] + '/' + split_from_filed_date[0]

		if to_filed_date is not None:
			split_to_filed_date = str(to_filed_date).split('-')
			to_filed_date = split_to_filed_date[1] + '/' +  split_to_filed_date[2] + '/' + split_to_filed_date[0]

		#Initialize the search criteria
		self.user_type = ''
		self.all_case_ids = 0
		self.case_number = case_number if case_number != '' else ''
		self.case_status = case_status
		self.from_filed_date = from_filed_date if from_filed_date != None else ''
		self.to_filed_date = to_filed_date if to_filed_date != None else ''
		self.from_last_entry_date = from_last_entry_date if from_last_entry_date != None else ''
		self.to_last_entry_date = to_last_entry_date if from_last_entry_date != None else ''
		self.nature_of_suit = nature_of_suit if nature_of_suit != '' else ''
		self.cause_of_action = cause_of_action if cause_of_action != '' else ''
		self.last_name = last_name if last_name != '' else ''
		self.first_name = first_name if first_name != '' else ''
		self.middle_name = middle_name if first_name != '' else ''
		self.type = type
		self.exact_matches_only = 0

	def save_search_criteria(self):
		"""
			Used to save the different search criteria used for querying.
			Arguments:
					self
		"""

		from_filed_date = self.from_filed_date if self.from_filed_date != '' else None
		to_filed_date = self.to_filed_date if self.to_filed_date != '' else None
		from_last_entry_date = self.from_last_entry_date if self.from_last_entry_date != '' else None
		to_last_entry_date = self.to_last_entry_date if self.to_last_entry_date != '' else None

		#Split the date to save in dd/mm/yyyy format
		#Because MySQL accepts only dd/mm/yyyy format
		#It fails to save the date if it is in any other format
		split_from_filed_date = self.from_filed_date.split('-')
		from_filed_date = split_from_filed_date[2] + '/' + split_from_filed_date[0] + '/' +split_from_filed_date[1]
		split_to_filed_date = self.to_filed_date.split('-')
		to_filed_date = split_to_filed_date[2] + '/' + split_to_filed_date[0] + '/' +split_to_filed_date[1]

		#Insert the case details into the database
		extractor_insert_query = """INSERT INTO extractor(case_number, case_status, from_field_date,
			to_field_date, from_last_entry_date, to_last_entry_date, nature_of_suit, cause_of_action,
			last_name, first_name, middle_name, type, exact_matches_only)
			VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
		self.connection_cursor.execute(extractor_insert_query, (self.case_number, self.case_status,
							from_filed_date , to_filed_date, from_last_entry_date, to_last_entry_date,
							self.nature_of_suit, self.cause_of_action,
							self.last_name, self.first_name, self.middle_name,
							self.type, self.exact_matches_only,))
		self.database_connection.commit()

	def __del__(self):
		"""
			Destructor
			Tasks:
				1. Close the database connection
		"""
		self.database_connection.close()

class Downloader():
	"""
		Class is used to download the case related pages from the PACER training website.
		Inherits:
				None
		Member functions:
				1. login_pacer(self)
				2. set_cookie_value(self, login_page_contents)
				3. validate_login_success(self, login_page_contents)
				4. get_case_details_page_contents(self)
				5. save_all_case_details_page(self, case_details_page_contents)
				6. logout(self)self.
				7. terminate_with_error_message(self)
	"""

	def __init__(self):
		"""
			Default constructor
			Tasks:
			 1. sets up the opener
			 2. Initializes login credentials
			 3. Initializes cookie
			 4. Setting up the database connection and cursor
		"""

		#Initialize the opener
		self.opener = urllib2.build_opener()
		urllib2.install_opener(self.opener)

		#Initialize the cookie_value
		self.pacer_session_cookie_value = ""

		#Initializes the login credentials
		self.username = 'tr1234'
		self.password = 'Pass!234'

		#settig up database connection
		self.database_connection = MySQLdb.connect(host= "",
						      user="root",
						      password="Code@mispl",
						      db="pacer_case_details")
		self.connection_cursor = self.database_connection.cursor()

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

	def set_cookie_value(self, login_page_contents):
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
				print "Login successful"
				return True

		return self.terminate_with_error_message()

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
		"""
			Saves the pages related to case details along with the pages
			containing additional information
			 Arguments:
			 		self, case_details_page_contents
			Returns:
					file_names_list
		"""

		case_links_list = []
		case_number_list = []
		file_names_list = []
		case_details_base_link = 'https://dcecf.psc.uscourts.gov/cgi-bin/'
		case_count = 0
		page_path = '/home/mis/DjangoProject/pacer/extractor/Contents'
		file_name = 'case_details.html'

		#Save the case details page having all case information
		case_details_file_object = open(page_path + '/' + file_name, 'w')
		case_details_file_object.write(case_details_page_contents)
		case_details_file_object.close()

		#Insert the value of variable page_path into the database
		path_insert_query = """INSERT INTO download_tracker(page_path) VALUES(%s)"""
		self.connection_cursor.execute(path_insert_query, (page_path,))
		self.database_connection.commit()

		#Collect all the links
		case_details_soup = BeautifulSoup(case_details_page_contents, 'html.parser')
		case_links = case_details_soup.find_all('a', class_='')
		for case_link in case_links:
			if case_link:
				case_links_list.append(case_link['href'])
				case_number_list.append(case_link.text)
			else:
				pass

		#open each link and save each page
		for case_link in case_links_list:
			case_details_page_response = self.opener.open( case_details_base_link + case_link )
			case_number = case_number_list[case_count].replace(':', '').replace('-', '_')
			file_name = case_number + '.html'
			file_names_list.append(file_name)
			case_file_object = open('/home/mis/DjangoProject/pacer/extractor/Contents/case/' + file_name , 'w+')
			case_file_object.write(case_details_page_response.read())
			case_count += 1
			case_file_object.close()
		print "Saved the files of all the case details"
		return file_names_list

	def logout(self):
		"""
			Logout from the website
			Arguments:
					self, openerdatabase_connection
		"""

		logout_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout"
		logout_response = self.opener.open(logout_page_url)
		logout_page_contents = logout_response.read()
		print "Logout Successful"

	def terminate_with_error_message(self):
		"""
			Terminate the program with upon unsuccessful login
			Arguments:
					self
		"""

		print "The program is terminated since the login was unsuccessful."
		print "Please check the credentials or your internet connection and try again"
		exit(0)

	def __del__(self):
		"""
			Destructor
			Tasks:
				1. Close the database connection
		"""
		self.database_connection.close()

class Parser():
	"""
		Class is used to scrape the case related data from the PACER training website.
		Inherits:
				None
		Member functions:
				1. parse_case_details_page(self, file_name)
				2. save_case_details(self)
	"""

	def __init__(self):
		"""
			Default constructor
			Tasks:
			 1. Setting up the database connection and cursor
		"""

		#settig up database connection
		self.database_connection = MySQLdb.connect(host= "",
						      user="root",
						      password="Code@mispl",
						      db="pacer_case_details")
		self.connection_cursor = self.database_connection.cursor()

	def parse_case_details_page(self, file_name):
		"""
			Parse the saved case pages
			Arguments:
					self, file_name
			Returns:
					required_case_details
		"""

		additional_info_json = {}
		additional_info_base_url = 'https://dcecf.psc.uscourts.gov/cgi-bin'
		parties_involved = ''

		#Parse for case details
		case_file = open('/home/mis/DjangoProject/pacer/extractor/Contents/case/' + file_name, 'r')
		contents = BeautifulSoup(case_file, 'html.parser')
		center_tag =  contents.find_all('center')
		case_details = re.split('Date filed: |Date terminated: |Date of last filing: | All Defendants ', center_tag[0].text)
		case_number = case_details[0]

		#Check for special cases where the text 'All Defendants are missing'
		if len(case_number) > 22: #The usual length of a case number
			parties_involved = case_number[18:]
			case_number = case_number[0:13]
		else:
			parties_involved = case_details[1]

		if len(case_number) > 13:
			case_number = case_number[:-4]
		case_filed_date = case_details[2]

		#Validate for cases without close date
		if len(case_details) > 3:
			case_closed_date = case_details[3]
		else:
			case_closed_date = ''

		#Add the created date and last updated date
		created_date = datetime.date.today().strftime('%Y/%m/%d')
		last_updated_date = created_date

		#Parse the additional info
		additional_info_links = contents.find_all('a', class_='')
		for additional_info in additional_info_links:
			additional_info_name = additional_info.text
			additional_info_link = additional_info_base_url + additional_info['href']
			additional_info_json[additional_info_name] = additional_info_link
		additional_info_json = json.dumps(additional_info_json)

		#Parse the pacer_case_id
		pacer_case_id = additional_info_link[-5:]

		#Perform tuple packing
		required_case_details = (case_number, parties_involved,
								case_filed_date, case_closed_date,
								pacer_case_id, additional_info_json,
								created_date, last_updated_date)
		return required_case_details

	def save_case_details(self, case_details_tuple, file_name):
		"""
			Save the parsed case details
			Arguments:
					self, case_details_tuple, file_name
		"""

		(case_number, parties_involved,
		case_filed_date, case_closed_date,
		pacer_case_id, additional_info_json,
		created_date, last_updated_date) = case_details_tuple
		page_value_json = {}

		#Save details into the database
		case_filed_date = case_filed_date.strip('\n')
		case_closed_date = case_filed_date.strip('\n')
		case_filed_date = case_filed_date if case_filed_date != '' else None
		case_closed_date = case_closed_date if case_closed_date != '' else None
		if case_filed_date is not None:
			split_case_filed_date = case_filed_date.split('/')
			case_filed_date = split_case_filed_date[2] + '/' +  split_case_filed_date[0] + '/' + split_case_filed_date[1]
		if case_closed_date is not None:
			split_case_closed_date = case_closed_date.split('/')
			case_closed_date = split_case_closed_date[2] + '/' +  split_case_closed_date[0] + '/' + split_case_closed_date[1]

		#Get Last updated date
		self.connection_cursor.execute("""SELECT pacer_case_id from courtcase
										  WHERE case_number = %s""",
										  (case_number,))
		existing_pacer_case_id = self.connection_cursor.fetchone()

		#Check if existing pacer_case_id matches with the pacer_case_id of the case in hand
		if existing_pacer_case_id:
			if existing_pacer_case_id[0]:
				if pacer_case_id == existing_pacer_case_id:
					is_equal_pacer_case_id = True
				elif pacer_case_id != existing_pacer_case_id:
					is_equal_pacer_case_id = False
		else:
			is_equal_pacer_case_id = False

		#Inset case details that are not already existing
		if not is_equal_pacer_case_id:
			#Save case related info into the table
			self.connection_cursor.execute("SELECT id from download_tracker ORDER BY id DESC LIMIT 1")
			download_tracker_id = self.connection_cursor.fetchall()
			courtcase_insert_query = """INSERT INTO courtcase(download_tracker_id, pacer_case_id, case_number,
										   parties_involved, case_filed_date, case_closed_date)
										   VALUES(%s, %s, %s, %s, %s, %s)"""
			self.connection_cursor.execute(courtcase_insert_query,
									(download_tracker_id, pacer_case_id, case_number, parties_involved,
									case_filed_date, case_closed_date,))
			self.database_connection.commit()

			#Save addional info into the table
			self.connection_cursor.execute("SELECT id from courtcase ORDER BY id DESC LIMIT 1")
			courtcase_id =  self.connection_cursor.fetchall()
			additional_info_insert_query = """INSERT INTO additional_info(courtcase_id, additional_info_json)
										VALUES(%s, %s)"""
			self.connection_cursor.execute(additional_info_insert_query, (courtcase_id, additional_info_json,))
			self.database_connection.commit()

			#Save into the courtcase_source_data_path table
			page_value_json['CASE'] = '/home/mis/DjangoProject/pacer/extractor/contents/case/' + file_name
			page_value_json = json.dumps(page_value_json)
			self.connection_cursor.execute("SELECT id from courtcase ORDER BY id DESC LIMIT 1")
			courtcase_id =  self.connection_cursor.fetchall()
			courtcase_source_data_path_insert_query = """INSERT INTO courtcase_source_data_path(courtcase_id, page_value_json)
										VALUES(%s, %s)"""
			self.connection_cursor.execute(courtcase_source_data_path_insert_query, (courtcase_id, page_value_json,))
			self.database_connection.commit()
		else:
			print "This entry already exists"
			return

	def __del__(self):
		"""
			Destructor
			Tasks:
				1. Close the database connection
		"""
		self.database_connection.close()
