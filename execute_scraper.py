import pacer_scrape as pacer_scraper


#Instantiate the PacerScrape class
pacer_scraper_obj = pacer_scraper.PacerScrape()

#Get the get_opener
opener = pacer_scraper_obj.get_opener()

#####################################################################################################
#Step-1 of 8: Hit the cookie page of the PACER training site.                                       #
#			 URL: https://dcecf.psc.uscourts.gov/cgi-bin/login.pl?logout 							#
#####################################################################################################
encoded_login_credentials = pacer_scraper_obj.login_pacer(opener)

#####################################################################################################
#Step-2 of 8: Login by entering the credentials provided by the training website.                   #
#			 Get the appropriate cookie value from the page we get after login.                     #
#####################################################################################################
cookie_value = pacer_scraper_obj.get_cookie_value(opener, encoded_login_credentials)

#####################################################################################################
#Step 3 of 8: Append the cookie value to the opener header.                                         #
#####################################################################################################
pacer_scraper_obj.append_opener_header(opener, cookie_value)

#####################################################################################################
#Step-4 of 8: Validate PACER login by checking appropriate fields.                                  #
#####################################################################################################
is_login_validate_success = pacer_scraper_obj.validate_login_success(cookie_value)

#Terminate the program if validation is unsuccessful
if not is_login_validate_success:
	pacer_scraper_obj.terminate_with_error_message()

#####################################################################################################
#Step-5 of 8: Hit the URL: https://dcecf.psc.uscourts.gov/cgi-bin/iquery.pl							#
#			  and enter the data for querying.                                                      #
#####################################################################################################
case_details_page_contents = pacer_scraper_obj.hit_query_page(opener)

#####################################################################################################
#Step-6 of 8: Save the Web page (HTML content) in a folder and save it's the path.                  #
#####################################################################################################
page_path = pacer_scraper_obj.save_webpage_and_get_page_path(case_details_page_contents)

#####################################################################################################
#Step-7 of 8: Save single case information including the additional information of that case.       #
#####################################################################################################
pacer_scraper_obj.save_case_details(opener, case_details_page_contents)

#####################################################################################################
#Step-8 of 8: Logout from the website.																#
#####################################################################################################
pacer_scraper_obj.logout(opener)
