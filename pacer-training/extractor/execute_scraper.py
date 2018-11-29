import pacer_scrape as pacer_scraper
import MySQLdb
from mysql.connector import MySQLConnection, Error

pacer_scraper_obj = pacer_scraper.PacerScrape()

# [ Step 1 of 9 ] : Hit the first page of PACER training site and Login.
login_page_contents = pacer_scraper_obj.login_pacer()

# [ Step 2 of 9 ] : Validate the Login.
is_login_validate_success = pacer_scraper_obj.validate_login_success(login_page_contents)

#Terminate the program if validation is unsuccessful
if not is_login_validate_success:
	pacer_scraper_obj.terminate_with_error_message()
else:
	print "Login successful"

# [ Step 3 of 9 ] : Parse the contents and get cookie.
pacer_scraper_obj.get_cookie_value(login_page_contents)

# [ Step 4 of 9 ] : Query as per the input criteria.
case_details_page_contents = pacer_scraper_obj.get_case_details_page_contents()

# [ Step 5 of 9 ] : Save the Web page (HTML content) in a folder.
page_path = pacer_scraper_obj.save_webpage_with_case_details(case_details_page_contents)

#settig up database connection
database_connection = MySQLdb.connect(host= "",
										user="root",
										password="Code@mispl",
										db="pacer_case_details")
connection_cursor = database_connection.cursor()
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
search_criteria = pacer_scraper.SearchCriteria()
try:
	from_filed_date = search_criteria.from_filed_date if search_criteria.from_filed_date != '' else None
	to_filed_date = search_criteria.to_filed_date if search_criteria.to_filed_date != '' else None
	from_last_entry_date = search_criteria.from_last_entry_date if search_criteria.from_last_entry_date != '' else None
	to_last_entry_date = search_criteria.to_last_entry_date if search_criteria.to_last_entry_date != '' else None
	split_from_filed_date = from_filed_date.split('/')
	from_filed_date = split_from_filed_date[2] + '/' + split_from_filed_date[0] + '/' +split_from_filed_date[1]
	split_to_filed_date = to_filed_date.split('/')
	to_filed_date = split_to_filed_date[2] + '/' + split_to_filed_date[0] + '/' +split_to_filed_date[1]
	search_criteria_insert_query = """INSERT INTO search_criteria(case_number, case_status, from_field_date,
		to_field_date, from_last_entry_date, to_last_entry_date, nature_of_suit, cause_of_action,
		last_name, first_name, middle_name, type, exact_matches_only)
		VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	connection_cursor.execute(search_criteria_insert_query, (search_criteria.case_number, search_criteria.case_status,
						from_filed_date , to_filed_date,from_last_entry_date, to_last_entry_date,
						search_criteria.nature_of_suit, search_criteria.cause_of_action,
						search_criteria.last_name, search_criteria.first_name, search_criteria.middle_name,
						search_criteria.type, search_criteria.exact_matches_only,))
	print "Details are successfully added into search_criteria Table"
	database_connection.commit()
except:
		print "Failed to insert data into search_criteria Table"
		database_connection.rollback()

# [ Step 8 of 9 ] : Print the case details.
case_details_list = pacer_scraper_obj.get_case_details(case_details_page_contents)

#Extract indivisual tuples from the list and
#Unpack all the tuples
case_numbers_list = []
for case_details in case_details_list:
	required_fields = case_details
	case_number = required_fields[0]
	parties_involed = required_fields[1]
	case_filed_date = required_fields[2]
	case_closed_date = required_fields[3]
	additional_info_json = required_fields[4]

	#Check for redundencies before inserting into the list
	if not case_number in case_numbers_list:
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
			connection_cursor.execute("SELECT page_content_id from page_content ORDER BY page_content_id DESC LIMIT 1")
			page_content_id = connection_cursor.fetchall()
			case_details_insert_query = """INSERT INTO case_details(page_content_id, case_number, parties_involved,
										case_filed_date, case_closed_date)
										VALUES(%s, %s, %s, %s, %s)"""
			connection_cursor.execute(case_details_insert_query,
									(page_content_id, case_number, parties_involed,
									case_filed_date, case_closed_date,))
			database_connection.commit()

			#print "Details are successfully added into case_details Table"
			case_numbers_list.append(case_number)
		except:
			print "Failed to insert data into case_details Table"
			database_connection.rollback()

		#Save addional info into the table
		try:
			connection_cursor.execute("SELECT case_id from case_details ORDER BY case_id DESC LIMIT 1")
			case_id =  connection_cursor.fetchall()
			additional_info_insert_query = """INSERT INTO additional_info(case_id, additional_info_json)
										VALUES(%s, %s)"""
			connection_cursor.execute(additional_info_insert_query, (case_id, additional_info_json,))
			database_connection.commit()
		except:
			print "Failed to insert data into additional_info Table"
			database_connection.rollback()
database_connection.close()

# [ Step 9 of 9 ] : Logout from the website.
pacer_scraper_obj.logout()

