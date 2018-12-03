import pacer_scrape as pacer_scraper
import MySQLdb
import os
import json
from mysql.connector import MySQLConnection, Error

downloader_obj = pacer_scraper.Downloader()
parser_obj = pacer_scraper.Parser()

# [ Step 1 of 9 ] : Hit the first page of PACER training site and Login.
login_page_contents = downloader_obj.login_pacer()

# [ Step 2 of 9 ] : Validate the Login.
is_login_validate_success = downloader_obj.validate_login_success(login_page_contents)

#Terminate the program if validation is unsuccessful
if not is_login_validate_success:
	downloader_obj.terminate_with_error_message()
else:
	print "Login successful"

# [ Step 3 of 9 ] : Parse the contents and get cookie.
downloader_obj.get_cookie_value(login_page_contents)

# [ Step 4 of 9 ] : Query as per the input criteria.
case_details_page_contents = downloader_obj.get_case_details_page_contents()

# [ Step 5 of 9 ] : Save the Web page (HTML content) in a folder.
number_of_cases = downloader_obj.save_all_case_details_page(case_details_page_contents)

page_path = os.getcwd() + '/contents'
#settig up database connection
database_connection = MySQLdb.connect(host= "",
				      user="root",
				      password="Code@mispl",
				      db="pacer_case_details")
connection_cursor = database_connection.cursor()

#Insert the value of variable page_path into the database
try:
	path_insert_query = """INSERT INTO page_content(page_path) VALUES(%s)"""
	connection_cursor.execute(path_insert_query, (page_path,))
	print "Details are successfully added into page_content Table"
	database_connection.commit()
except:
	print "Failed to insert data into page_content Table"
	database_connection.rollback()

# [ Step 6 of 9 ] : Print the page path.
print "page_path:\t", page_path

# [ Step 7 of 9 ] : Print the Search Criteria.
#Save the search criteria
extractor = pacer_scraper.Extractor()
try:
	from_filed_date = extractor.from_filed_date if extractor.from_filed_date != '' else None
	to_filed_date = extractor.to_filed_date if extractor.to_filed_date != '' else None
	from_last_entry_date = extractor.from_last_entry_date if extractor.from_last_entry_date != '' else None
	to_last_entry_date = extractor.to_last_entry_date if extractor.to_last_entry_date != '' else None
	split_from_filed_date = from_filed_date.split('/')
	from_filed_date = split_from_filed_date[2] + '/' + split_from_filed_date[0] + '/' +split_from_filed_date[1]
	split_to_filed_date = to_filed_date.split('/')
	to_filed_date = split_to_filed_date[2] + '/' + split_to_filed_date[0] + '/' +split_to_filed_date[1]
	extractor_insert_query = """INSERT INTO extractor(case_number, case_status, from_field_date,
		to_field_date, from_last_entry_date, to_last_entry_date, nature_of_suit, cause_of_action,
		last_name, first_name, middle_name, type, exact_matches_only)
		VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	connection_cursor.execute(extractor_insert_query, (extractor.case_number, extractor.case_status,
						from_filed_date , to_filed_date,from_last_entry_date, to_last_entry_date,
						extractor.nature_of_suit, extractor.cause_of_action,
						extractor.last_name, extractor.first_name, extractor.middle_name,
						extractor.type, extractor.exact_matches_only,))
	print "Details are successfully added into extractor Table"
	database_connection.commit()
except:
		print "Failed to insert data into extractor Table"
		database_connection.rollback()

# [ Step 8 of 9 ] : Print the case details.
for case_count in range(1, number_of_cases):
	case_details_tuple = parser_obj.parse_case_details_page('case_' + str(case_count))
	case_number = case_details_tuple[0]
	parties_involed = case_details_tuple[1]
	case_filed_date = case_details_tuple[2].strip('\n')
	case_closed_date = case_details_tuple[3].strip('\n')
	additional_info_json = case_details_tuple[4]

	#Save details into the database
	case_filed_date = case_filed_date if case_filed_date != '' else None
	case_closed_date = case_closed_date if case_closed_date != '' else None
	if case_filed_date is not None:
		split_case_filed_date = case_filed_date.split('/')
		case_filed_date = split_case_filed_date[2] + '/' +  split_case_filed_date[0] + '/' + split_case_filed_date[1]
	if case_closed_date is not None:
		split_case_closed_date = case_closed_date.split('/')
		case_closed_date = split_case_closed_date[2] + '/' +  split_case_closed_date[0] + '/' + split_case_closed_date[1]

	#Save case related info into the table
	try:
		connection_cursor.execute("SELECT id from page_content ORDER BY id DESC LIMIT 1")
		page_content_id = connection_cursor.fetchall()
		case_details_insert_query = """INSERT INTO case_details(page_content_id, case_number, parties_involved,
									case_filed_date, case_closed_date)
									VALUES(%s, %s, %s, %s, %s)"""
		connection_cursor.execute(case_details_insert_query,
								(page_content_id, case_number, parties_involed,
								case_filed_date, case_closed_date,))
		database_connection.commit()
	except:
		print "Failed to insert data into case_details Table"
		database_connection.rollback()

	#Save addional info into the table
	try:
		connection_cursor.execute("SELECT id from case_details ORDER BY id DESC LIMIT 1")
		case_details_id =  connection_cursor.fetchall()
		additional_info_insert_query = """INSERT INTO additional_info(case_details_id, additional_info_json)
									VALUES(%s, %s)"""
		connection_cursor.execute(additional_info_insert_query, (case_details_id, additional_info_json,))
		database_connection.commit()
	except:
		print "Failed to insert data into additional_info Table"
		database_connection.rollback()

	#Save into the page_source_path table
	page_value_json = {}
	page_value_json['CASE' + str(case_count)] = os.getcwd() + '/contents/case/case_' + str(case_count)  + '.html'
	page_value_json = json.dumps(page_value_json)
	try:
		connection_cursor.execute("SELECT id from case_details ORDER BY id DESC LIMIT 1")
		case_details_id =  connection_cursor.fetchall()
		page_source_path_insert_query = """INSERT INTO page_source_path(case_details_id, page_value_json)
									VALUES(%s, %s)"""
		connection_cursor.execute(page_source_path_insert_query, (case_details_id, page_value_json,))
		database_connection.commit()
	except:
		print "Failed to insert data into page_source_path Table"
		database_connection.rollback()

database_connection.close()

# [ Step 9 of 9 ] : Logout from the website.
downloader_obj.logout()
