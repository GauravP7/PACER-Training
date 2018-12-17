#!/py-virtualenv/ENV/bin/python
import os
import urllib
import urllib2
import re
import MySQLdb
import json
import datetime
import find_case
from cookielib import CookieJar
from bs4 import BeautifulSoup

# [ Step 1 of 7 ] : Hit the first page of PACER training site and Login.
#
# [ Step 2 of 7 ] : Validate the Login.
#
# [ Step 3 of 7 ] : Parse the contents and get cookie.
#
# [ Step 4 of 7 ] : Query as per the input criteria.
#
# [ Step 5 of 7 ] : Save the Web page (HTML content) in a folder.
#
# [ Step 6 of 7 ] : Save the case details.
#
# [ Step 7 of 7 ] : Logout from the website.

#Setup the CSO login
IS_CSO_LOGIN = False

#Set Extractor type
EXTRACTOR_TYPE = ""
DATE_RANGE = "DATE_RANGE"
REFRESH_CASE = "REFRESH_CASE"
PACER_IMPORT_CASE = "PACER_IMPORT_CASE"
PARSE_FILE = "PARSE_FILE"
FIND_CASE = "FIND_CASE"

class Extractor():
	"""
		Class holds the search criteria used to query the case details.

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

		#Setup the CSO login
		if IS_CSO_LOGIN == False:
			self.courthouse_link_element = 'dcecf.psc'
		elif IS_CSO_LOGIN == True:
			self.courthouse_link_element = 'ecf-test.cacd'

		#settig up database connection
		self.connection = MySQLdb.connect(
								host= "",
						      	user="root",
						      	password="Code@mispl",
						      	db="pacer_case_details"
						 )
		self.connection_cursor = self.connection.cursor()
		self.connection_cursor.execute("SELECT * FROM extractor ORDER BY id DESC LIMIT 1")

		#Unpack tuples for extractor fields
		extractor_search_criteria = self.connection_cursor.fetchall()

		for search_criteria in extractor_search_criteria:
			(id,
			extractor_type_id,
			is_local_parsing,
			input_pacer_case_id,
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
			exact_matches_only) = search_criteria
			break

		if from_filed_date:
			split_from_filed_date = str(from_filed_date).split('-')
			from_filed_date = split_from_filed_date[1] + '/' +  split_from_filed_date[2] + '/' + split_from_filed_date[0]
		if to_filed_date:
			split_to_filed_date = str(to_filed_date).split('-')
			to_filed_date = split_to_filed_date[1] + '/' +  split_to_filed_date[2] + '/' + split_to_filed_date[0]

		self.extractor_type_id = extractor_type_id
		self.is_local_parsing = is_local_parsing
		self.pacer_case_id = input_pacer_case_id

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

	def __del__(self):
		"""
			Destructor
			Tasks:
				1. Close the database connection
		"""

		self.connection.close()

class Downloader():
	"""
		Class is holds the methods to download the case
		related pages from the PACER training website.
		Member functions:
				 1. set_credentials(self)
				 2. login_pacer(self)
				 3. set_cookie_value(self, login_page_contents)
				 4. validate_login_success(self, login_page_contents)
				 5. get_case_details_page_contents(self)pacer_case_id
				 6. save_all_case_details_page(self, case_details_page_contents)
				 7. get_page_based_on_case_number(self, case_number)
				 8. save_import_case(self, page_contents, case_number)
				 9. save_indivisual_cases(self, case_details_page_contents)
				10. pacer_case_id_exists(self, case_number)
				11. logout(self)
				12. terminate_with_error_message(self)
	"""

	def __init__(self):
		"""
			Default constructor
			Tasks:
			 1. sets up the opener
			 2. Initializes cookie
			 3. Initializes login credentials
			 4. Instantiates the required classes
			 5. Initializes the extractor_type based on input from extractor
			 6. Sets up the database connection and cursor
		"""

		#Initialize the opener
		self.cookie_jar = CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
		#urllib2.install_opener(self.opener)

		#Initialize the cookie_value
		self.pacer_session_cookie_value = ""

		#Initialize the username and password
		self.username = ''
		self.password = ''

		#Set the object for find_case module
		self.find_case_object = find_case.FindCase()

		#Creating the extractor obj
		self.extractor_object = Extractor()

		#Set the extractor type
		self.extractor_type = ""
		if self.extractor_object.extractor_type_id == 1:
			EXTRACTOR_TYPE = DATE_RANGE
		elif self.extractor_object.extractor_type_id == 2:
			EXTRACTOR_TYPE = REFRESH_CASE
		elif self.extractor_object.extractor_type_id == 3:
			EXTRACTOR_TYPE = PACER_IMPORT_CASE
		elif self.extractor_object.extractor_type_id == 4:
			EXTRACTOR_TYPE = PARSE_FILE
		elif self.extractor_object.extractor_type_id == 5:
			EXTRACTOR_TYPE = FIND_CASE
		self.extractor_type = EXTRACTOR_TYPE

		#settig up database connection
		self.connection = MySQLdb.connect(
									host= "",
						      		user="root",
						      		password="Code@mispl",
						      		db="pacer_case_details"
						 )
		self.connection_cursor = self.connection.cursor()

	def set_credentials(self):
		"""
			Used to set the username and password.
			Arguments:
					self
		"""

		credentials_json = open('/home/mis/DjangoProject/pacer_training/extractor/credentials.json')
		credentials_data = json.load(credentials_json)
		if IS_CSO_LOGIN:
			self.username = credentials_data['CSO_LOGIN'][0]['USERNAME']
			self.password = credentials_data['CSO_LOGIN'][0]['PASSWORD']
		else:
			self.username = credentials_data['PACER_LOGIN'][0]['USERNAME']
			self.password = credentials_data['PACER_LOGIN'][0]['PASSWORD']

	def login_cso(self):
		self.set_credentials()
		cso_login_url = "https://train-login.uscourts.gov/csologin/login.jsf?pscCourtId=CACXDC&appurl=https%3A%2F%2Fecf-test.cacd.uscourts.gov%2Fcgi-bin%2Fshowpage.pl%3F16"

		#get viewstate value
		login_page_request = urllib2.Request(cso_login_url)
		login_page_response = self.opener.open(login_page_request)
		login_page_contents = login_page_response.read()
		login_page_soup = BeautifulSoup(login_page_contents, 'html.parser')

		form_tag = login_page_soup.find_all('input', id='j_id1:javax.faces.ViewState:1')
		view_state_value = form_tag[0]['value']

		formdata = {
					"javax.faces.partial.ajax": "true",
					 "Cache-Control":"no-cache",
					 "javax.faces.source": "loginForm:fbtnLogin",
					 "javax.faces.partial.execute": "@all",
					 "javax.faces.partial.render": "pscLoginPanel loginForm redactionConfirmation popupMsgId",
					 "loginForm:fbtnLogin": "loginForm:fbtnLogin",
					 "loginForm": "loginForm",
					"loginForm:loginName" : self.username,
					 "loginForm:password": self.password,
					 "loginForm:clientCode": "",
					 "javax.faces.ViewState": str(view_state_value),
					 }

		encoded_login_credentials = urllib.urlencode(formdata)
		login_page_request = urllib2.Request(cso_login_url)
		login_page_response = self.opener.open(login_page_request , encoded_login_credentials)
		second_page_url = "https://ecf-test.cacd.uscourts.gov/cgi-bin/showpage.pl?16"
		second_page_request = urllib2.Request(second_page_url)
		second_page_response = self.opener.open(second_page_request)
		contents_to_send = second_page_response.read()
		return contents_to_send

	def login_pacer(self):
		"""
			Used to login into the PACER training website and make related function calls.
			Arguments:
					self
			Returns:
					pacer_session_cookie_value
		"""

		if IS_CSO_LOGIN:
			return self.login_cso()
		else:
			self.set_credentials()
			credentials = {'login': self.username, 'key': self.password}
			encoded_login_credentials = urllib.urlencode(credentials)
			login_page = 'https://' + self.extractor_object.courthouse_link_element + '.uscourts.gov/cgi-bin/login.pl?logout'
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
		if not IS_CSO_LOGIN:
			self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')]
			self.opener.addheaders.append(('Referer','https://dcecf.psc.uscourts.gov/cgi-bin/ShowIndex.pl'))
			self.opener.addheaders.append(('Cookie', self.pacer_session_cookie_value ))
		else:
			self.opener.addheaders.append(('Referer', 'https://ecf-test.cacd.uscourts.gov/cgi-bin/iquery.pl'))

	def validate_login_success(self, login_page_contents):
		"""
			Returns True if login is successful. returns False otherwise.
			Arguments:
					self, login_page_contents
		"""

		login_page_soup = BeautifulSoup(login_page_contents, 'html.parser')
		login_page_h3_tags = login_page_soup.find_all('h3')
		for h3_tag in login_page_h3_tags:
			if "U.S. DISTRICT COURT" in str(h3_tag) or "Official Court Electronic Document" in str(h3_tag):
				print "Login successful"
				return True
		self.terminate_with_error_message()

	def get_case_details_page_contents(self):
		"""
			 Hits the query URL and returns the case details page
			 after querying with appropriate search criteria
			 Arguments:
			 		self
			Returns:
					case_details_page_contents

		"""

		cookie_string = ''
		required_form_number = ''

		#Set the cookie value for CSO login
		if self.cookie_jar:
			for cookie in self.cookie_jar:
				cookie_string += cookie.name + "=" + cookie.value +"; "

		self.opener.addheaders.append(("Cookie", cookie_string))

		query_page_url = 'https://' + self.extractor_object.courthouse_link_element + '.uscourts.gov/cgi-bin/iquery.pl'
		query_page_response = self.opener.open(query_page_url)
		query_page_contents = query_page_response.read()
		minimum_size_of_form_number = 5
		pacer_case_id = ''

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
		data_page_url = "https://" + self.extractor_object.courthouse_link_element + ".uscourts.gov/cgi-bin/iquery.pl?" + required_form_number + "-L_1_0-1"

		#The parameters to be encoded and sent as a search criteria
		query_parameters = {
			'UserType': self.extractor_object.user_type,
			'all_case_ids': self.extractor_object.pacer_case_id,
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
		case_details_base_link = 'https://' + self.extractor_object.courthouse_link_element + '.uscourts.gov/cgi-bin/'
		case_count = 0
		is_parsed = 0
		page_path = '/home/mis/DjangoProject/pacer_training/extractor/contents'
		file_name = 'case_details_'+ str(datetime.datetime.now().strftime('%d_%m_%y_%H:%M:%S')).replace(' ', '') +'.html'

		#Save the case details page having all case information
		case_details_file_object = open(page_path + '/' + file_name, 'w')
		case_details_file_object.write(case_details_page_contents)
		case_details_file_object.close()

		#Insert the value of variable page_path into the database
		path_insert_query = """INSERT INTO download_tracker(is_parsed, page_path) VALUES(%s, %s)"""
		self.connection_cursor.execute(path_insert_query, ( is_parsed, page_path + '/' + file_name,))
		self.connection.commit()

	def get_page_based_on_case_number(self, case_number):
		"""
			Used if the extractor type is REFRESH_CASE, to save
			the page containing Docket, path and the additional information
			of the case whose case number is given.
			Arguments:
					self, case_number
		"""

		pacer_case_id = 0
		DEFAULT = 2
		additional_info_base_url = 'https://' + self.extractor_object.courthouse_link_element + '.uscourts.gov/cgi-bin'
		additional_info_json = {}
		required_form_number = ''
		case_number = case_number.strip(' ').strip('\t').strip('\n')
		case_number_matched = re.match(r'^\d{1}:\d{2}\-\w{2}\-\d{5}', case_number)

		#Set the autocommit to true in order to refesh the database,
		#Otherwise the database will fail to fetch the courtcase_id for
		#The newly imported case
		self.connection.autocommit(True)
		case_number = case_number_matched.group(0)
		docket_page_url = "https://" + self.extractor_object.courthouse_link_element + ".uscourts.gov/cgi-bin/DktRpt.pl?"

		case_file_name =  case_number.replace(':', '').replace('-', '_')
		docket_page_path = '/home/mis/DjangoProject/pacer_training/extractor/contents/case/'
		save_docket_page_path = docket_page_path + case_file_name + '_docket.html'
		docket_page = open(save_docket_page_path, 'w')

		#Fetch the pacer_case_id from the database
		#pacer_case_id = self.find_case_object.get_pacer_case_id(case_number, self.opener)
		self.connection_cursor.execute("""SELECT pacer_case_id FROM courtcase WHERE case_number = %s""", (self.extractor_object.case_number ,))
		pacer_case_id_tuple = self.connection_cursor.fetchone()
		for pacer_case_id_value in pacer_case_id_tuple:
			pacer_case_id = pacer_case_id_value

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
		docket_details_page_url = "https://" + self.extractor_object.courthouse_link_element + ".uscourts.gov/cgi-bin/DktRpt.pl?" + required_form_number + "-L_1_0-1"
		docket_query_parameters_encoded = urllib.urlencode(docket_query_parameters)
		docket_query_request = urllib2.Request(docket_details_page_url, docket_query_parameters_encoded)
		docket_page_response = self.opener.open(docket_query_request)
		docket_page_contents = docket_page_response.read()
		docket_page.write(docket_page_contents)
		docket_page.close()

		#Update the JSON in the courtcase_source_data_path
		self.connection_cursor.execute("""SELECT id FROM courtcase WHERE case_number LIKE (%s)""", (case_number,))
		courtcase_id_tuple = self.connection_cursor.fetchone()
		for courtcase_id_value in courtcase_id_tuple:
			courtcase_id = courtcase_id_value
		self.connection.autocommit(False)

		#Append the path of saved Docket file
		self.connection_cursor.execute("""SELECT page_value_json FROM courtcase_source_data_path WHERE courtcase_id LIKE (%s)""", (courtcase_id,))
		page_value_json_tuple = self.connection_cursor.fetchone()
		for page_value_json_field in page_value_json_tuple:
			page_value_json = page_value_json_field
		page_value_json = json.loads(page_value_json)
		save_additional_info_page_path = page_value_json['CASE']
		page_value_json['DOCKET'] = save_docket_page_path
		page_value_json = json.dumps(page_value_json)
		courtcase_source_data_path_update_query = """UPDATE courtcase_source_data_path SET page_value_json = %s WHERE courtcase_id = %s"""
		self.connection_cursor.execute(courtcase_source_data_path_update_query, (page_value_json, courtcase_id,))

		#Change METADATA TO DEFAULT
		courtcase_source_value = DEFAULT
		courtcase_update_query = """UPDATE courtcase SET courtcase_source_value = %s WHERE pacer_case_id = %s"""
		self.connection_cursor.execute(courtcase_update_query, (courtcase_source_value, pacer_case_id,))
		self.connection.commit()

		#Save contents into the addional_info table
		courtcase_details_file_object = open(save_additional_info_page_path, 'r')
		additionol_info_page_contnets_soup = BeautifulSoup(courtcase_details_file_object.read(), 'html.parser')
		additional_info_links = additionol_info_page_contnets_soup.find_all('a', class_='')
		for additional_info in additional_info_links:
			additional_info_name = additional_info.text
			additional_info_link = additional_info_base_url + additional_info['href']
			additional_info_json[additional_info_name] = additional_info_link
		additional_info_json = json.dumps(additional_info_json)
		self.connection_cursor.execute("SELECT id from courtcase WHERE pacer_case_id = %s", (pacer_case_id ,))
		courtcase_id_tuple =  self.connection_cursor.fetchall()
		for courtcase_id_value in courtcase_id_tuple:
			courtcase_id = courtcase_id_value
		additional_info_insert_query = """INSERT INTO additional_info(courtcase_id, additional_info_json)
									VALUES(%s, %s)"""
		self.connection_cursor.execute(additional_info_insert_query, (courtcase_id, additional_info_json,))
		self.connection.commit()

	def save_import_case(self, page_contents, case_number):
		"""
			Used if the extractor type is PACER_IMPORT_CASE, to save the new page.
			Arguments:
					self, page_contents, case_number
			Returns:
					file_name
		"""

		case_number_matched = re.match(r'^\d{1}:\d{2}\-\w{2}\-\d{5}', case_number)
		case_number = case_number_matched.group(0)
	 	file_name = case_number.replace(':','_').replace('-','_') + '.html'
		case_file_object = open('/home/mis/DjangoProject/pacer_training/extractor/contents/case/' + file_name , 'w+')
		case_file_object.write(page_contents)
		return file_name

	def save_indivisual_cases(self, case_details_page_contents):
		"""
			Used to save the HTML of individual cases.
			Arguments:
					self, case_details_page_contents
		"""

		case_details_base_link = 'https://' + self.extractor_object.courthouse_link_element + '.uscourts.gov/cgi-bin/'
		case_links_list = []
		case_number_list = []
		page_value_json = {}
		case_count = 0

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
			if IS_CSO_LOGIN == False:
				pacer_case_id = case_link[-5:]
			else:
				pacer_case_id = case_link[-6:]
			case_number = case_number_list[case_count].strip(r'\s*|\n')
			case_number = re.sub(r'[A-Z]{3}\-?', "", case_number).replace(':', '').replace('-', '_')
			if case_number[-1:] != '_':
		 		file_name = case_number + '.html'
			else:
				#Remove the - form the end
				case_number = case_number[:-1]
		 		file_name = case_number + '.html'

			case_file_object = open('/home/mis/DjangoProject/pacer_training/extractor/contents/case/' + file_name , 'w+')
			case_file_object.write(case_details_page_response.read())
			case_count += 1
			case_file_object.close()

			#Save into the courtcase_source_data_path table
			courtcase_id = self.connection_cursor.execute("SELECT id from courtcase WHERE pacer_case_id = %s", (pacer_case_id,))
			page_value_json['CASE'] = '/home/mis/DjangoProject/pacer_training/extractor/contents/case/' + str(file_name)
			page_value_json = json.dumps(page_value_json)
			self.connection_cursor.execute("SELECT id from courtcase WHERE pacer_case_id = %s", (pacer_case_id,))
			courtcase_id =  self.connection_cursor.fetchall()
			courtcase_source_data_path_insert_query = """INSERT INTO courtcase_source_data_path(courtcase_id, page_value_json)
										VALUES(%s, %s)"""
			self.connection_cursor.execute(courtcase_source_data_path_insert_query, (courtcase_id, page_value_json,))
			self.connection.commit()
			page_value_json = {}

	def pacer_case_id_exists(self, case_number):
		"""
			Used to check if the pacer_case_id exists for a given case_number.
			Arguments:
					self, case_number
			Returns:
					True - if pacer_case_id exists,
					False - otherwise.
		"""

		pacser_case_id = self.find_case_object.get_pacer_case_id(case_number, self.opener)
		self.connection_cursor.execute("""SELECT pacer_case_id from courtcase WHERE case_number = %s""", (case_number, ))
		existing_pacer_case_id = self.connection_cursor.fetchone()

		if existing_pacer_case_id:
			return True
		else:
			return False

	def download(self, case_details_page_contents):
		self.case_details_list = []
		self.save_all_case_details_page(case_details_page_contents)
		parser_object = Parser()
		parser_object.display_page_cost(case_details_page_contents)
		EXTRACTOR_TYPE = PARSE_FILE

	def display_pacer_case_id(self):
		"""
			Used to find the pacer_case_id.
			This method is defined here because the
			find_case moduldownload(e makes use of the opener.
			Arguments:
					self
			Returns:
					pacer_case_id - Searched using the case_number
		"""

		pacer_case_id = self.find_case_object.get_pacer_case_id(self.extractor_object.case_number, self.opener)
		print "The PACER case ID is:\t", pacer_case_id
		print "The PACER case Number is:\t", self.extractor_object.case_number
		return

	def parse_url_data(self, case_details_page_contents):

		EXTRACTOR_TYPE = self.extractor_type
		self.parser_object = Parser()

		#REFRESH_CASE without DATE_RANGE
		if self.extractor_object.case_number != '' and EXTRACTOR_TYPE == REFRESH_CASE:
			self.get_page_based_on_case_number(self.extractor_object.case_number)
		if EXTRACTOR_TYPE == FIND_CASE:
			self.display_pacer_case_id()
		if EXTRACTOR_TYPE == PACER_IMPORT_CASE:
			is_pacer_case_id_exists = self.pacer_case_id_exists(self.extractor_object.case_number)
			if not is_pacer_case_id_exists:
				print "The case " + self.extractor_object.case_number + " does not exist. Importing it..."
				new_case_file_name = self.save_import_case(case_details_page_contents, self.extractor_object.case_number)
				case_details_tuple = self.parser_object.parse_case_details_page(new_case_file_name)
				self.parser_object.save_case_details(case_details_tuple, new_case_file_name)
				EXTRACTOR_TYPE = "REFRESH_CASE"
				self.get_page_based_on_case_number(self.extractor_object.case_number)
			else:
				self.get_page_based_on_case_number(self.extractor_object.case_number)

	def logout(self):
		"""
			Logout from the website
			Arguments:
					self, openerconnection
		"""

		logout_page_url = "https://" + self.extractor_object.courthouse_link_element + ".uscourts.gov/cgi-bin/login.pl?logout"
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

		self.connection.close()

class Parser():
	"""
		Class is holds the methods to scrape the case
		related data from the PACER training website.
		Member functions:
				1. display_page_cost(self, case_details_page_contents)
				2. parse_case_details_page(self, file_name)
				3. save_case_details(self,  case_details_tuple, file_name)
				4. get_metadata_page(self)
				5. save_metadata_page_contents(self, case_details_tuple_list)
				6. get_local_parse_filename(self, case_number)
				7. parse_local_docket_page(self, file_to_parse)
		Inherits:
				None
	"""

	def __init__(self):
		"""
			Default constructor
			Tasks:
			 1. Creating the Extractor Object
			 2. Setting up the database connection and cursor
		"""

		self.extractor_object = Extractor()
		self.downloader_object = Downloader()

		#settig up database connection
		self.connection = MySQLdb.connect(
								host= "",
						      	user="root",
						      	password="Code@mispl",
						      	db="pacer_case_details"
						  )
		self.connection_cursor = self.connection.cursor()

	def display_page_cost(self, case_details_page_contents):
		"""
			Used to display the cost of the parsed page
			Arguments:
					self, case_details_page_contents
		"""

		soup_for_cost = BeautifulSoup(case_details_page_contents, 'html.parser')
		required_tags = soup_for_cost.find_all('font', color='DARKBLUE', size='-1')

		if required_tags:
			cost = required_tags[::-1][0].text
		else:
			cost = None
		print "The querying cost for this page:\t$", cost

	def parse_case_details_page(self, file_name):
		"""
			Parse the saved case pages
			Arguments:
					self, file_name
			Returns:
					required_case_details
		"""

		additional_info_json = {}
		additional_info_base_url = 'https://' + self.extractor_object.courthouse_link_element + '.uscourts.gov/cgi-bin'
		parties_involved = ''

		#Parse for case details
		case_file = open('/home/mis/DjangoProject/pacer_training/extractor/contents/case/' + file_name, 'r')
		contents = BeautifulSoup(case_file, 'html.parser')
		center_tag =  contents.find_all('center')
		case_details = re.split('Date filed: |Date terminated: |Date of last filing: | All Defendants ', center_tag[0].text)
		case_number = case_details[0]

		case_number_regex_str = r'(?P<upto_five_digits>^\d{1}:\d{2}\-[a-z]{2}\-\d{5})\-([A-Z]{3}\-?)*(?P<last_digit>\d{1})?'
		case_number_regex = re.compile(case_number_regex_str)

		#Check for special cases where the text 'All Defendants are missing'
		if len(case_number) > 25:
			parties_involved = re.sub(case_number_regex, "", case_number)
			case_number = re.sub(parties_involved, "", case_number)
		else:
			parties_involved = case_details[1]
		case_number = case_number.strip(r'\s*|\n')

		#Remove the last four character like -RJA
		case_number_matched = re.match(case_number_regex, case_number)
		if case_number_matched:
			case_number_group_dict = case_number_matched.groupdict()

			if case_number_group_dict['last_digit']:
				case_number = str(case_number_group_dict['upto_five_digits']) + '-' + str(case_number_group_dict['last_digit'])
			else:
				case_number = str(case_number_group_dict['upto_five_digits'])

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
		if self.extractor_object.is_local_parsing:
			pacer_case_id = self.extractor_object.pacer_case_id
		else:
			if IS_CSO_LOGIN == False:
				pacer_case_id = additional_info_link[-5:]
			else:
				pacer_case_id = additional_info_link[-6:]

		#Perform tuple packing
		required_case_details_tuple = (case_number, parties_involved,
								case_filed_date, case_closed_date,
								pacer_case_id, additional_info_json)
		return required_case_details_tuple

	def save_case_details(self, case_details_tuple, file_name):
		"""
			Save the parsed case details for PACER_IMPORT_CASE
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
		if case_filed_date:
			split_case_filed_date = case_filed_date.split('/')
			case_filed_date = split_case_filed_date[2] + '/' +  split_case_filed_date[0] + '/' + split_case_filed_date[1]
		if case_closed_date:
			split_case_closed_date = case_closed_date.split('/')
			case_closed_date = split_case_closed_date[2] + '/' +  split_case_closed_date[0] + '/' + split_case_closed_date[1]

		#Check for the pacer_case_id
		self.connection_cursor.execute("""SELECT pacer_case_id from courtcase
										  WHERE pacer_case_id = %s""",
										  (pacer_case_id,))
		existing_pacer_case_id = self.connection_cursor.fetchone()

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
		self.connection.commit()

		#Save contents into the addional_info table
		self.connection_cursor.execute("SELECT id from courtcase ORDER BY id DESC LIMIT 1")
		courtcase_id =  self.connection_cursor.fetchall()
		additional_info_insert_query = """INSERT INTO additional_info(courtcase_id, additional_info_json)
									VALUES(%s, %s)"""
		self.connection_cursor.execute(additional_info_insert_query, (courtcase_id, additional_info_json,))
		self.connection.commit()

		#Save into the courtcase_source_data_path table
		page_value_json['CASE'] = '/home/mis/DjangoProject/pacer_training/extractor/contents/case/' + file_name
		page_value_json = json.dumps(page_value_json)
		self.connection_cursor.execute("SELECT id from courtcase ORDER BY id DESC LIMIT 1")
		courtcase_id =  self.connection_cursor.fetchall()
		courtcase_source_data_path_insert_query = """INSERT INTO courtcase_source_data_path(courtcase_id, page_value_json)
									VALUES(%s, %s)"""
		self.connection_cursor.execute(courtcase_source_data_path_insert_query, (courtcase_id, page_value_json,))
		self.connection.commit()

	def get_metadata_page(self):
		"""
			Used when the extractor type is PARSE_FILE.
			Parses the HTML file containing the search results.
			Returns:
					case_details_tuple_list - contains tuples of indivisual cases
		"""

		case_details_tuple_list = []
		metadata_page_query = "SELECT is_parsed FROM download_tracker ORDER BY id DESC LIMIT 1"
		self.connection_cursor.execute(metadata_page_query)
		is_parsed = self.connection_cursor.fetchone()

		if is_parsed[0] == 0:
			#Parse the page and Insert into the DB
			metadata_page_query = "SELECT page_path FROM download_tracker ORDER BY id DESC LIMIT 1"
			self.connection_cursor.execute(metadata_page_query)
			page_path = self.connection_cursor.fetchone()
			metadata_file_name = page_path[0]
			metadata_page_file_object = open(metadata_file_name, 'r')

			#Parse the file containing the search results
			metadata_file_soup = BeautifulSoup(metadata_page_file_object, 'html.parser')
			table_contents = metadata_file_soup.find_all('tr')
			length = len(table_contents) # - (len(table_contents) - 1)
			for case_details_index in range(length):
				all_td_tags = table_contents[case_details_index].find_all('td')
				if len(all_td_tags) > 2:
					case_number = all_td_tags[0].a.text
					if IS_CSO_LOGIN == False:
						pacer_case_id = all_td_tags[0].a['href'][-5:]
					else:
						pacer_case_id = all_td_tags[0].a['href'][-6:]

					parties_involved = all_td_tags[1].text
					required_dates = all_td_tags[2].text
					required_dates_split = required_dates.split()
					case_filed_date = required_dates_split[1]
					if len(required_dates_split) > 3:
						case_closed_date = required_dates_split[3]
					else:
						case_closed_date = None

					#Truncate unwanted characters from case_number
					case_number_matched = re.match(r'(?P<upto_five_digits>^\d{1}:\d{2}\-[a-z]{2}\-\d{5})\-([A-Z]{3}\-?)*(?P<last_digit>\d{1})?', case_number)
					if case_number_matched:
						case_number_group_dict = case_number_matched.groupdict()
						if case_number_group_dict['last_digit']:
							case_number = str(case_number_group_dict['upto_five_digits']) + '-' + str(case_number_group_dict['last_digit'])
						else:
							case_number = str(case_number_group_dict['upto_five_digits'])
					case_details_tuple = (case_number, pacer_case_id, parties_involved, case_filed_date, case_closed_date)
					case_details_tuple_list.append(case_details_tuple)
				else:
					continue
			is_parsed_update_query = """UPDATE download_tracker SET is_parsed = %s WHERE page_path = %s"""
			self.connection_cursor.execute(is_parsed_update_query, (1, metadata_file_name,))
			self.connection.commit()
			return case_details_tuple_list
		else:
			print "The file is already parsed"
			return None

	def save_metadata_page_contents(self, case_details_tuple_list):
		"""
			Used to save the case details form the Search results file.
			Arguments:
					case_details_tuple_list
		"""

		METADATA = 1
		courtcase_source_value = METADATA
		case_details_insert_query = """INSERT INTO courtcase(download_tracker_id, courtcase_source_value, pacer_case_id, case_number,
									   parties_involved, case_filed_date, case_closed_date)
									   VALUES(%s, %s, %s, %s, %s, %s, %s)"""
		self.connection_cursor.execute("SELECT id from download_tracker ORDER BY id DESC LIMIT 1")
		download_tracker_id = self.connection_cursor.fetchall()
		for case_details_tuple in case_details_tuple_list:
			(case_number, pacer_case_id, parties_involved, case_filed_date, case_closed_date) = case_details_tuple
			self.connection_cursor.execute("""SELECT pacer_case_id from courtcase
											  WHERE pacer_case_id = %s""", (pacer_case_id,))
			existing_pacer_case_id = self.connection_cursor.fetchone()

			#Check if existing pacer_case_id matches with the pacer_case_id of the case in hand
			if existing_pacer_case_id:
				is_equal_pacer_case_id = True
			else:
				is_equal_pacer_case_id = False

			#Inset case details that are not already existing
			if not is_equal_pacer_case_id:
				if case_filed_date:
					case_filed_date_split = case_filed_date.split('/')
					case_filed_date = case_filed_date_split[2] + '/' +  case_filed_date_split[0] + '/' + case_filed_date_split[1]
				if case_closed_date:
					split_case_closed_date = case_closed_date.split('/')
					case_closed_date = split_case_closed_date[2] + '/' +  split_case_closed_date[0] + '/' + split_case_closed_date[1]
				self.connection_cursor.execute(case_details_insert_query, (download_tracker_id,
											courtcase_source_value, pacer_case_id, case_number, parties_involved,
											case_filed_date, case_closed_date,))
				self.connection.commit()

	def get_local_parse_filename(self, case_number):
		"""
			Used to get the filename of the file
			which is to be parsed locally.
			Arguments:
					case_number
			Returns:
					file_to_parse
		"""

		file_find_path = '/home/mis/DjangoProject/pacer_training/extractor/contents/case'
		case_number = case_number.replace(':', '').replace('-', '_')
		file_to_parse = case_number + '.html'
		return file_to_parse

	def parse_local_docket_page(self, file_to_parse):
		"""
			Used to get the filename of the docket file
			which is to be parsed locally.
			Arguments:
					file_to_parse
		"""

		DEFAULT = 2
		pacer_case_id = self.extractor_object.pacer_case_id
		self.connection.autocommit(False)
		file_find_path = '/home/mis/DjangoProject/pacer_training/extractor/contents/case'
		docket_file = file_to_parse.strip('.hmtl') + '_docket' + '.html'
		save_docket_page_path = file_find_path + '/' + docket_file
		docket_file_object = open(save_docket_page_path, 'r')

		#Update the JSON in the courtcase_source_data_path
		self.connection_cursor.execute("""SELECT id FROM courtcase WHERE pacer_case_id = %s""", (pacer_case_id,))
		courtcase_id_tuple = self.connection_cursor.fetchone()
		for courtcase_id_value in courtcase_id_tuple:
			courtcase_id = courtcase_id_value
		self.connection.autocommit(False)

		#Append the path of saved Docket file
		self.connection_cursor.execute("""SELECT page_value_json FROM courtcase_source_data_path WHERE courtcase_id LIKE (%s)""", (courtcase_id,))
		page_value_json_tuple = self.connection_cursor.fetchone()
		for page_value_json_content in page_value_json_tuple:
			page_value_json = page_value_json_content
		page_value_json = json.loads(page_value_json)
		save_additional_info_page_path = page_value_json['CASE']
		page_value_json['DOCKET'] = save_docket_page_path
		page_value_json = json.dumps(page_value_json)
		courtcase_source_data_path_update_query = """UPDATE courtcase_source_data_path SET page_value_json = %s WHERE courtcase_id = %s"""
		self.connection_cursor.execute(courtcase_source_data_path_update_query, (page_value_json, courtcase_id,))

		#Change METADATA TO DEFAULT
		courtcase_source_value = DEFAULT
		courtcase_update_query = """UPDATE courtcase SET courtcase_source_value = %s WHERE pacer_case_id = %s"""
		self.connection_cursor.execute(courtcase_update_query, (courtcase_source_value, pacer_case_id,))
		self.connection.commit()

	def parse(self, case_details_page_contents):
		case_details_list = self.get_metadata_page()
		self.save_metadata_page_contents(case_details_list)
		EXTRACTOR_TYPE = REFRESH_CASE

	def local_parse(self):

		file_to_parse = self.get_local_parse_filename(self.extractor_object.case_number)

		# [ Step 7 of 8 ] : Save the case details.
		case_details_tuple = self.parse_case_details_page(file_to_parse)
		self.save_case_details(case_details_tuple, file_to_parse)

		#Save docket page
		self.parse_local_docket_page(file_to_parse)

	def __del__(self):
		"""
			Destructor
			Tasks:
				1. Close the database connection
		"""

		self.connection.close()
