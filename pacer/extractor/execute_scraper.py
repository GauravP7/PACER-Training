import pacer_scrape as pacer_scraper

downloader_obj = pacer_scraper.Downloader()
parser_obj = pacer_scraper.Parser()

# [ Step 1 of 9 ] : Hit the first page of PACER training site and Login.
login_page_contents = downloader_obj.login_pacer()

# [ Step 2 of 9 ] : Validate the Login.
is_login_validate_success = downloader_obj.validate_login_success(login_page_contents)

# [ Step 3 of 9 ] : Parse the contents and get cookie.
downloader_obj.set_cookie_value(login_page_contents)

# [ Step 4 of 9 ] : Query as per the input criteria.
case_details_page_contents = downloader_obj.get_case_details_page_contents()

# [ Step 5 of 9 ] : Save the Web page (HTML content) in a folder.
file_names_list = downloader_obj.save_all_case_details_page(case_details_page_contents)

# [ Step 6 of 9 ] : Display cost of the page.
parser_obj.get_page_cost(case_details_page_contents)

# [ Step 7 of 9 ] : Save the Search Criteria.
#extractor = pacer_scraper.Extractor()
#extractor.save_search_criteria()

# [ Step 8 of 9 ] : Save the case details.
for file_name in file_names_list:
	case_details_tuple = parser_obj.parse_case_details_page(file_name)
	parser_obj.save_case_details(case_details_tuple, file_name)

# [ Step 9 of 9 ] : Logout from the website.
downloader_obj.logout()
