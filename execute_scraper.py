import pacer_scrape as pacer_scraper


#Instantiate the PacerScrape class
pacer_scraper_obj = pacer_scraper.PacerScrape()

# [ Step 2 of 7 ]	:	Login to training website.
#  						Get the appropriate cookie value from the page we get after login.
cookie_value = pacer_scraper_obj.login_pacer()	#Fetch the cookie  value for validating login

# [ Step 3 of 7 ]	:	Validate the login.
is_login_validate_success = pacer_scraper_obj.validate_login_success(cookie_value)

if not is_login_validate_success:	#Terminate the program if validation is unsuccessful
	pacer_scraper_obj.terminate_with_error_message()

# [ Step 4 of 7 ]	:	Query as per the input criteria.
case_details_page_contents = pacer_scraper_obj.get_case_details_page_contents()

# [ Step 5 of 7 ]	:	Save the Web page (HTML content) in a folder.
page_path = pacer_scraper_obj.save_webpage_with_case_details(case_details_page_contents)

# [ Step 6 of 7 ]	:	Save the case details.
pacer_scraper_obj.save_case_details(case_details_page_contents)

# [ Step 7 of 7 ]	:	Logout from the website.
pacer_scraper_obj.logout()
