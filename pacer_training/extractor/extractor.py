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

		#Check for DATE_RANGE extractor type
		extractor_object = Extractor()
		downloader_object = Downloader()
		parser_object = Parser()

		if extractor_object.extractor_type == "DATE_RANGE":
			downloader_object.download()
			parser_object.parse()
		elif extractor_object.extractor_type == "FIND_CASE":
			downloader_object.display_pacer_case_id()

		parser_object.parse_url_data()

scraper_object = Scraper()
scraper_object.run()
