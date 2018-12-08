#!/py-virtualenv/ENV/bin/python
import os
import urllib
import urllib2
import re
import MySQLdb
import json
import datetime
import find_case
from bs4 import BeautifulSoup

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
# [ Step 6 of 9 ] : Display cost of the page.
#
# [ Step 8 of 9 ] : Save the case details.
#
# [ Step 9 of 9 ] : Logout from the website.

class Extractor():
	"""
		Class holds the search criteria used to query the case details.
		Member functions:
				1. save_search_criteria(self)
		Inherits:
				None
	"""

	def __init__(self):
		"""
			Default constructor
			Tasks:
			 1. Setting up the database connection and cursor
			 2. Initialize the search criteria, reading from the database
		"""
		#settig up database connection
		self.database_connection = MySQLdb.connect(host= "",
						      user="root",
						      password="Code@mispl",
						      db="pacer_case_details")
		self.connection_cursor = self.database_connection.cursor()
		self.connection_cursor.execute("SELECT * FROM extractor ORDER BY id DESC LIMIT 1")
		extractor_search_criteria = self.connection_cursor.fetchall()
		(id,
		extractor_type_id,
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
		self.extractor_type_id = extractor_type_id
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
			Used to save the different search criteria used for querying courtcase.
			Arguments:
					self
		"""

		from_filed_date = self.from_filed_date if self.from_filed_date != '' else None
		to_filed_date = self.to_filed_date if self.to_filed_date != '' else None
		from_last_entry_date = self.from_last_entry_date if self.from_last_entry_date != '' else None
		to_last_entry_date = self.to_last_entry_date if self.to_last_entry_date != '' else None

		#Split the date to save in dd/mm/yyyy format
		#Since MySQL accepts only this format
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
		Member functions:
				 1. set_credentials(self)
				 2. login_pacer(self)
				 3. set_cookie_value(self, login_page_contents)
				 4. validate_login_success(self, login_page_contents)
				 5. get_case_details_page_contents(self)
				 6. save_all_case_details_page(self, case_details_page_contents)
				 7. get_page_based_on_case_number(self, case_number)
				 8. import_case_new(self, case_number)
				 9. logout(self)
				10. terminate_with_error_message(self)
		Inherits:
				None
	"""

	def __init__(self):
		"""
			Default constructor
			Tasks:
			 1. sets up the opener
			 2. Initializes login credentials
			 3. Initializes cookie
			 4. Sets up the database connection and cursor
		"""

		#Initialize the opener
		self.opener = urllib2.build_opener()
		urllib2.install_opener(self.opener)

		#Initialize the cookie_value
		self.pacer_session_cookie_value = ""

		#Initialize the username and password
		self.username = ''
		self.password = ''

		#Set the object for find_case module
		self.find_case_object = find_case.FindCase()

		#Creating the extractor obj
		self.extractor_object = Extractor()

		#settig up database connection
		self.database_connection = MySQLdb.connect(host= "",
						      user="root",
						      password="Code@mispl",
						      db="pacer_case_details")
		self.connection_cursor = self.database_connection.cursor()

	def set_credentials(self):
		"""
			Used to set the username and password.
			Arguments:
					self
		"""

		with open('/home/mis/DjangoProject/pacer/extractor/credentials.json') as credentials_json:
			credentials_data = json.load(credentials_json)
			self.username = credentials_data['username']
			self.password = credentials_data['password']

	def login_pacer(self):
		"""
			Used to login into the PACER training website and make related function calls.
			Arguments:
					self
			Returns:
					pacer_session_cookie_value
		"""

		self.set_credentials()
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
https://github.com/gaurav-uc/pacer-training/blob/0e1247d0c883e22d614900abcbc1b3b0330cacf6/pacer/extractor/pacer_scrape.py#L283
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
		if self.extractor_object.case_number != '':
			pacer_case_id = self.find_case_object.get_pacer_case_id(self.extractor_object.case_number, self.opener)
		else:
			pacer_case_id = ''
			
		#The parameters to be encoded and sent as a search criteria
		query_parameters = {
			'UserType': self.extractor_object.user_type,
			'all_case_ids': pacer_case_id,
			'case_num': self.extractor_object.case_number,
			'Qry_filed_from': self.extractor_object.from_filed_date,
			'Qry_filed_to': self.extractor_object.to_filed_date,
			'lastentry_from': self.extractor_object.from_last_entry_date,
			'lastentry_to': self.extractor_object.to_last_entry_date,
			'last_name': self.extractor_object.last_name,
			'first_name': self.extractor_object.first_name,
			'middle_name': self.extractor_object.middle_name,
			'person_type': self.extractor_object.type
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
		file_name = 'case_details '+ str(datetime.datetime.now().strftime('%d-%m-%y  %H:%M:%S')) +'.html'

		#Save the case details page having all case information
		case_details_file_object = open(page_path + '/' + file_name, 'w')
		case_details_file_object.write(case_details_page_contents)
		case_details_file_object.close()

		#Insert the value of variable page_path into the database
		path_insert_query = """INSERT INTO download_tracker(page_path) VALUES(%s)"""
		self.connection_cursor.execute(path_insert_query, (page_path + '/' + file_name,))
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

	def get_page_based_on_case_number(self, case_number):
		"""
			Used if the extractor type is REFRESH_CASE, to save th page containing Docket.
			Arguments:
					self, case_number
		"""

		case_number = case_number.strip(' ').strip('\t').strip('\n')
		case_number_matched = re.match(r'^\d:\d+\-[a-z]+\-\d{5}', case_number)
		case_number = case_number_matched.group(0)	
		pacer_case_id = 0

		docket_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/DktRpt.pl?"
		case_file_name =  case_number.replace(':', '').replace('-', '_')
		docket_page_path = '/home/mis/DjangoProject/pacer/extractor/Contents/case/'
		save_docket_page_path = docket_page_path + case_file_name + '_docket.html'
		docket_page = open(save_docket_page_path, 'w')

		#Fetch the pacer_case_id using the find_case module
		pacer_case_id = self.find_case_object.get_pacer_case_id( case_number, self.opener)

		#Get the unique numbers
		docket_page_response = self.opener.open(docket_page_url)
		docket_page_contents = docket_page_response.read()
		minimum_size_of_form_number = 5

		#Extract random numbers
		docket_page_soup = BeautifulSoup(docket_page_contents, 'html.parser')
		form_action_value = docket_page_soup.find('form').get('action')
		action_content = re.findall(r"[0-9]*", form_action_value)

		# Extract only the number part
		for form_number in action_content:
			if form_number.isdigit() and len(form_number) >= minimum_size_of_form_number:
				required_form_number = form_number
				break

		#The parameters to be encoded and sent as a search criteria
		docket_query_parameters = {
			'view_comb_doc_text': '',
			'all_case_ids': pacer_case_id,
			'case_num': case_number,
			'date_range_type': 'Filed',
			'date_from': '',
			'date_to': '',
			'documents_numbered_from_': '',
			'documents_numbered_to_': '',
			'list_of_parties_and_counsel': 'on',
			'terminated_parties': 'on',
			'output_format': 'html',
			'PreResetField': '',
			'PreResetFields': '',
			'sort1': 'oldest date first'
		}
		docket_details_page_url = "https://dcecf.psc.uscourts.gov/cgi-bin/DktRpt.pl?" + required_form_number + "-L_1_0-1"
		docket_query_parameters_encoded = urllib.urlencode(docket_query_parameters)
		docket_query_request = urllib2.Request(docket_details_page_url, docket_query_parameters_encoded)
		docket_page_response = self.opener.open(docket_query_request)
		docket_page_contents = docket_page_response.read()
		docket_page.write(docket_page_contents)
		docket_page.close()

		#Update the JSON in the courtcase_source_data_path
		self.connection_cursor.execute("""SELECT id FROM courtcase WHERE case_number LIKE (%s)""", (case_number,))
		courtcase_id = self.connection_cursor.fetchone()[0]

		#Append the path of saved Docket file
		self.connection_cursor.execute("""SELECT page_value_json FROM courtcase_source_data_path WHERE courtcase_id = %s""", (courtcase_id,))
		page_value_json = self.connection_cursor.fetchone()[0]
		page_value_json = json.loads(page_value_json)
		page_value_json['DOCKET'] = save_docket_page_path
		page_value_json = json.dumps(page_value_json)
		courtcase_source_data_path_update_query = """UPDATE courtcase_source_data_path SET page_value_json = %s WHERE courtcase_id = %s"""
		self.connection_cursor.execute(courtcase_source_data_path_update_query, (page_value_json, courtcase_id,))

		#Change METADATA TO DEFAULT
		courtcase_update_query = """UPDATE courtcase SET courtcase_source_value = %s WHERE pacer_case_id = %s"""
		self.connection_cursor.execute(courtcase_update_query, (2, pacer_case_id,))
		self.database_connection.commit()
		print "Refeshed the case ", case_number

	def save_new_case(self, page_contents, case_number):
	 	file_name = case_number.replace(':','_').replace('-','_') + '.html'
		case_file_object = open('/home/mis/DjangoProject/pacer/extractor/Contents/case/' + file_name , 'w+')
		case_file_object.write(page_contents)

		return file_name

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
		Member functions:
				1. display_page_cost(self, case_details_page_contents)
				2. parse_case_details_page(self, file_name)
				3. save_case_details(self,  case_details_tuple, file_name)
		Inherits:
				None
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

	def display_page_cost(self, case_details_page_contents):
		"""
			Used to display the cost of the parsed page
			Arguments:
					self, case_details_page_contents
		"""

		soup_for_cost = BeautifulSoup(case_details_page_contents, 'html.parser')
		required_tags = soup_for_cost.find_all('font', color='DARKBLUE', size='-1')
		cost = required_tags[::-1][0].text
		print "This querying cost for this page:\t$", cost

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

		#Remove the last four character like -RJA
		case_number_matched = re.match(r'^\d:\d+\-[a-z]+\-\d{5}', case_number)
		case_number = case_number_matched.group(0)
		parties_involved = case_details[1]
		case_filed_date = case_details[2]

		#Validate for cases without close date
		if len(case_details) > 3:
			case_closed_date = case_details[3]
		else:
			case_closed_date = ''

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
								pacer_case_id, additional_info_json)
		return required_case_details

	def save_case_details(self, case_details_tuple, file_name):
		"""
			Save the parsed case details
			Arguments:
					self, case_details_tuple, file_name
		"""

		(case_number, parties_involved,
		case_filed_date, case_closed_date,
		pacer_case_id, additional_info_json) = case_details_tuple
		METADATA = 1
		DEFAULT = 2
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
										  WHERE pacer_case_id = %s""",
										  (pacer_case_id,))
		existing_pacer_case_id = self.connection_cursor.fetchone()

		#Check if existing pacer_case_id matches with the pacer_case_id of the case in hand
		if existing_pacer_case_id:
			is_equal_pacer_case_id = True
		else:
			is_equal_pacer_case_id = False

		#Inset case details that are not already existing
		if not is_equal_pacer_case_id:
			self.connection_cursor.execute("SELECT id from download_tracker ORDER BY id DESC LIMIT 1")
			download_tracker_id = self.connection_cursor.fetchall()
			courtcase_insert_query = """INSERT INTO courtcase(download_tracker_id, courtcase_source_value, pacer_case_id, case_number,
										   parties_involved, case_filed_date, case_closed_date)
										   VALUES(%s, %s, %s, %s, %s, %s, %s)"""
			courtcase_source_value = METADATA
			self.connection_cursor.execute(courtcase_insert_query,
									(download_tracker_id, courtcase_source_value, pacer_case_id,
									case_number, parties_involved,
									case_filed_date, case_closed_date,))
			self.database_connection.commit()

			#Save contents into the addional_info table
			self.connection_cursor.execute("SELECT id from courtcase ORDER BY id DESC LIMIT 1")
			courtcase_id =  self.connection_cursor.fetchall()
			additional_info_insert_query = """INSERT INTO additional_info(courtcase_id, additional_info_json)
										VALUES(%s, %s)"""
			self.connection_cursor.execute(additional_info_insert_query, (courtcase_id, additional_info_json,))
			self.database_connection.commit()

			#Save into the courtcase_source_data_path table
			page_value_json['CASE'] = '/home/mis/DjangoProject/pacer/extractor/Contents/case/' + file_name
			page_value_json = json.dumps(page_value_json)
			self.connection_cursor.execute("SELECT id from courtcase ORDER BY id DESC LIMIT 1")
			courtcase_id =  self.connection_cursor.fetchall()
			courtcase_source_data_path_insert_query = """INSERT INTO courtcase_source_data_path(courtcase_id, page_value_json)
										VALUES(%s, %s)"""
			self.connection_cursor.execute(courtcase_source_data_path_insert_query, (courtcase_id, page_value_json,))
			self.database_connection.commit()
		else:
			pass

	def __del__(self):
		"""
			Destructor
			Tasks:
				1. Close the database connection
		"""
		self.database_connection.close()
