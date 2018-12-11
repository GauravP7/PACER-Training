import pacer_scrape as pacer_scraper
import find_case as find_case_object
import find_case

class Scraper():

	def __init__(self):
		self.downloader_object = pacer_scraper.Downloader()
		self.parser_object = pacer_scraper.Parser()
		self.extractor_object = pacer_scraper.Extractor()
		self.find_case_object = find_case.FindCase()
		self.extractor_type = self.extractor_object.set_extractor_type()

	def run(self):

		if not self.extractor_object.is_local_parsing:
			# [ Step 1 of 8 ] : Hit the first page of PACER training site and Login.
			login_page_contents = self.downloader_object.login_pacer()

			# [ Step 2 of 8 ] : Validate the Login.
			self.downloader_object.validate_login_success(login_page_contents)

			# [ Step 3 of 8 ] : Parse the contents and get cookie.
			self.downloader_object.set_cookie_value(login_page_contents)

			# [ Step 4 of 8 ] : Query as per the input criteria.
			case_details_page_contents = self.downloader_object.get_case_details_page_contents()

		#Set the extractor type
		while True:
			if self.extractor_type == "DATE_RANGE":

				# [ Step 5 of 8 ] : Save the Web page (HTML content) in a folder.
				#Save the HTML file containing all the case details
				self.downloader_object.save_all_case_details_page(case_details_page_contents)

				# [ Step 6 of 8 ] : Display cost of the page.
				self.parser_object.display_page_cost(case_details_page_contents)
				self.extractor_type = "PARSE_FILE"
				continue

			elif self.extractor_type == "PARSE_FILE":
				case_details_list = self.parser_object.get_metadata_page()
				if case_details_list == None:
					break
				self.parser_object.save_metadata_page_contents(case_details_list)
				self.extractor_type = "REFRESH_CASE"
				continue

			elif self.extractor_type == "FIND_CASE":
				pacer_case_id = self.downloader_object.find_pacer_case_id()
				print "The PACER case ID is:\t", pacer_case_id
				break

			elif self.extractor_type == "REFRESH_CASE":
				if self.extractor_object.case_number == '':
					self.downloader_object.save_indivisual_cases(case_details_page_contents)
				elif self.extractor_object.case_number != '':
					self.downloader_object.get_page_based_on_case_number(self.extractor_object.case_number)
				break

			elif self.extractor_type == "PACER_IMPORT_CASE":

				#check for local parsing
				if self.extractor_object.is_local_parsing:
					file_to_parse = self.parser_object.fetch_local_parse_filename(self.extractor_object.case_number)

					# [ Step 7 of 8 ] : Save the case details.
					case_details_tuple = self.parser_object.parse_case_details_page(file_to_parse)
					self.parser_object.save_case_details(case_details_tuple, file_to_parse)

					#Save docket page
					self.parser_object.parse_local_docket_page(file_to_parse)
				else:
					is_exists_pacer_case_id = self.downloader_object.pacer_case_id_exists(self.extractor_object.case_number)

					if not is_exists_pacer_case_id:
						print "The case " + self.extractor_object.case_number + " does not exist. Importing it..."

						# [ Step 5 of 8 ] : Save the Web page (HTML content) in a folder.
						new_case_file_name = self.downloader_object.save_import_case(case_details_page_contents, self.extractor_object.case_number)

						# [ Step 7 of 8 ] : Save the case details.
						case_details_tuple = self.parser_object.parse_case_details_page(new_case_file_name)
						self.parser_object.save_case_details(case_details_tuple, new_case_file_name)
						self.extractor_type = "REFRESH_CASE"
						continue
					else:
						#REFRESH_CASE if the case already exists
						self.extractor_type = "REFRESH_CASE"
				break

		if not self.extractor_object.is_local_parsing:

			# [ Step 8 of 8 ] : Logout from the website.
			self.downloader_object.logout()

scraper_object = Scraper()
scraper_object.run()
