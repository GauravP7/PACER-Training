from extractor_base import Extractor, Downloader, Parser
import find_case

class Scraper():
	"""
		Class Holds the methods to set up the execution
		point and flow of the program.
		Member functions:
				 1. run(self)
	"""

	def run(self):
		"""
			Runs the extractor.
			Arguments:
					self
		"""

		extractor_object = Extractor()

		#Check for DATE_RANGE extractor type
		if extractor_object.extractor_type == "DATE_RANGE":
			downloader_object = Downloader()
			parser_object = Parser()

			#The HTML of the page containing the metadata
			#of the cases as well as the files containing
			#the individual cases are downloaded in the foler
			#and the cost of the downloaded file is displayed
			downloader_object.download()

			#The HTML file containing the metadata of the
			#cases and the files containing the individual
			#case details are parsed and saved into the database
			parser_object.parse()
		elif extractor_object.extractor_type == "FIND_CASE":
			downloader_object = Downloader()
			downloader_object.display_pacer_case_id()
			return

		parser_object = Parser()
		parser_object.parse_url_data()

scraper_object = Scraper()
scraper_object.run()
