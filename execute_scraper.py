import pacer_scrape as pacer_scraper

#Instantiate the PacerScrape class
pacer_scraper_obj = pacer_scraper.PacerScrape()

# [ Step 1 of 9 ] : Hit the first page of PACER training site and Login.
login_page_contents = pacer_scraper_obj.login_pacer()

# [ Step 2 of 9 ] : Validate the Login.
is_login_validate_success = pacer_scraper_obj.validate_login_success(login_page_contents)

if not is_login_validate_success:	#Terminate the program if validation is unsuccessful
	pacer_scraper_obj.terminate_with_error_message()

else:
	print "Login successful"

# [ Step 3 of 9 ] : Parse the contents and get cookie.
pacer_scraper_obj.get_cookie_value(login_page_contents)

# [ Step 4 of 9 ] : Query as per the input criteria.
case_details_page_contents = pacer_scraper_obj.get_case_details_page_contents()

# [ Step 5 of 9 ] : Save the Web page (HTML content) in a folder.
page_path = pacer_scraper_obj.save_webpage_with_case_details(case_details_page_contents)

# [ Step 6 of 9 ] : Print the page path.
print "page_path:\t", page_path

# [ Step 7 of 9 ] : Print the Search Criteria.
#Print the search criteria
search_criteria = pacer_scraper.SearchCriteria()
print "Search Criteria are:"
print "user_type:\t", search_criteria.user_type
print "all_case_ids:\t", search_criteria.all_case_ids
print "case_number:\t", search_criteria.case_number
print "case_status:\t", search_criteria.case_status
print "from_filed_date:\t", search_criteria.from_filed_date
print "to_filed_date:\t", search_criteria.to_filed_date
print "from_last_entry_date:\t", search_criteria.from_last_entry_date
print "to_last_entry_date:\t", search_criteria.to_last_entry_date
print "nature_of_suit:\t", search_criteria.nature_of_suit
print "cause_of_action:\t", search_criteria.cause_of_action
print "last_name:\t", search_criteria.last_name
print "first_name:\t", search_criteria.first_name
print "middle_name:\t", search_criteria.middle_name
print "type:\t", search_criteria.type
print "exact_matches_only:\t", search_criteria.exact_matches_only

# [ Step 8 of 9 ] : Print the case details.
#Get the case revevent information
pacer_scraper_obj.get_case_details(case_details_page_contents)

# [ Step 9 of 9 ] : Logout from the website.
pacer_scraper_obj.logout()
