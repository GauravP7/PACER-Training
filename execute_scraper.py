import pacer_scrape as pacer_scraper

#Instantiate the PacerScrape class
pacer_scraper_obj = pacer_scraper.PacerScrape()

# [ Step 1 of 8 ] : Hit the first page of PACER training site and Login.
login_page_contents = pacer_scraper_obj.login_pacer()

# [ Step 2 of 8 ] : Validate the Login.
is_login_validate_success = pacer_scraper_obj.validate_login_success(login_page_contents)

if not is_login_validate_success:	#Terminate the program if validation is unsuccessful
	pacer_scraper_obj.terminate_with_error_message()

else:
	print "Login successful"

# [ Step 3 of 8 ] : Parse the contents and get cookie.
cookie_value = pacer_scraper_obj.get_cookie_value(login_page_contents)

# [ Step 4 of 8 ] : Query as per the input criteria.
case_details_page_contents = pacer_scraper_obj.get_case_details_page_contents()

# [ Step 5 of 8 ] : Save the Web page (HTML content) in a folder.
page_path = pacer_scraper_obj.save_webpage_with_case_details(case_details_page_contents)

# [ Step 6 of 8 ] : Print the page path.
print "page_path:\t", page_path

# [ Step 7 of 8 ] : Print the case details.
pacer_scraper_obj.parse_case_details(case_details_page_contents)

case_details_file_object = open("parsed_case_details.txt", "r")
case_detail_contents = case_details_file_object.read()

print "The case details are:"

print case_detail_contents

# [ Step 8 of 8 ] : Logout from the website.
pacer_scraper_obj.logout()
