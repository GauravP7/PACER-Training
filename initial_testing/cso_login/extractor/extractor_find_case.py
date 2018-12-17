import urllib
import urllib2
from bs4 import BeautifulSoup
import pacer_scrape as pacer_scrape

class FindCase():
    """
		Class holds the methods to find the case based on case number.
		Member functions:
				 1. get_pacer_case_id(self, case_number, opener)
	"""

    def __init__(self):
        self.extractor_object = pacer_scrape.Extractor()

    def get_pacer_case_id(self, case_number, opener):
        find_case_url = "https://" + pacer_scrape.courthouse_link_element + ".uscourts.gov/cgi-bin/possible_case_numbers.pl?" + case_number
        find_case_xml_response = opener.open(find_case_url)
        find_case_xml_contents = find_case_xml_response.read()
        find_case_soup = BeautifulSoup(find_case_xml_contents, 'html.parser')
        case_tag = find_case_soup.find('case')
        return case_tag['id']
