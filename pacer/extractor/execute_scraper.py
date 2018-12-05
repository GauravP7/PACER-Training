import pacer_scrape as pacer_scraper

class Scraper():

	def __init__(self):
		self.downloader_obj = pacer_scraper.Downloader()
		self.parser_obj = pacer_scraper.Parser()
		self.extractor_obj = pacer_scraper.Extractor()

		self.extractor_type = ''

	def set_extractor_type(self):
		if self.extractor_obj.case_number == '':
			self.extractor_type = "DATE_RANGE"
		else:
			self.extractor_type = "REFRESH_CASE"

	def run(self):

		# [ Step 1 of 8 ] : Hit the first page of PACER training site and Login.
		login_page_contents = self.downloader_obj.login_pacer()

		# [ Step 2 of 8 ] : Validate the Login.
		is_login_validate_success = self.downloader_obj.validate_login_success(login_page_contents)

		# [ Step 3 of 8 ] : Parse the contents and get cookie.
		self.downloader_obj.set_cookie_value(login_page_contents)

		self.set_extractor_type()

		# [ Step 4 of 8 ] : Query as per the input criteria.
		case_details_page_contents = self.downloader_obj.get_case_details_page_contents()

		#Set the extractor type
		if self.extractor_type == "DATE_RANGE":

			# [ Step 5 of 8 ] : Save the Web page (HTML content) in a folder.
			file_names_list = self.downloader_obj.save_all_case_details_page(case_details_page_contents)

			# [ Step 6 of 8 ] : Display cost of the page.
			self.parser_obj.display_page_cost(case_details_page_contents)

			# [ Step 7 of 8 ] : Save the case details.
			for file_name in file_names_list:
				case_details_tuple = self.parser_obj.parse_case_details_page(file_name)
				self.parser_obj.save_case_details(case_details_tuple, file_name)

		elif self.extractor_type == "REFRESH_CASE":
			 self.downloader_obj.get_page_based_on_case_number(self.extractor_obj.case_number)

		# [ Step 8 of 8 ] : Logout from the website.
		self.downloader_obj.logout()


scraper_object = Scraper()
scraper_object.run()
