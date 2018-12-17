import extractor_base as pacer_scrape
import find_case

class Scraper():
	"""
		Class Holds the methods to set up the execution
		point and flow of the program.
		Member functions:
				 1. run(self)
	"""

		# self.find_case_object = find_case.FindCase()
		# self.extractor_type = self.extractor_object.set_extractor_type()

	def run(self):
		"""
			Runs the extractor.
			Arguments:
					self
		"""

		extractor_object = pacer_scrape.Extractor()
		downloader_object = pacer_scrape.Downloader()
		parser_object = pacer_scrape.Parser()

		if not extractor_object.is_local_parsing:

			# [ Step 1 of 8 ] : Hit the first page of PACER training site and Login.
			login_page_contents = downloader_object.login_pacer()

			# [ Step 2 of 8 ] : Validate the Login.
			downloader_object.validate_login_success(login_page_contents)

			# [ Step 3 of 8 ] : Parse the contents and get cookie.
			downloader_object.set_cookie_value(login_page_contents)

			# [ Step 4 of 8 ] : Query as per the input criteria.
			case_details_page_contents = downloader_object.get_case_details_page_contents()

		#Set the extractor type
		if downloader_object.extractor_type == "DATE_RANGE":

			# [ Step 5 of 8 ] : Save the Web page (HTML content) in a folder.
			downloader_object.download(case_details_page_contents)
			parser_object.parse(case_details_page_contents)
			downloader_object.save_indivisual_cases(case_details_page_contents)

		parser_object.parse_url_data()

		if not extractor_object.is_local_parsing:

			# [ Step 8 of 8 ] : Logout from the website.
			downloader_object.logout()

scraper_object = Scraper()
scraper_object.run()
