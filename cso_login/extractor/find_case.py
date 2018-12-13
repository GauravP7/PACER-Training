import urllib
import urllib2
from bs4 import BeautifulSoup
import pacer_scrape as pacer_scrape
class FindCase():

    def __init__(self):
        self.extractor_object = pacer_scrape.Extractor()

    def get_pacer_case_id(self, case_number, opener):
        find_case_url = "https://" + self.extractor_object.courthouse_link_element + ".uscourts.gov/cgi-bin/possible_case_numbers.pl?" + case_number
        find_case_xml_response = opener.open(find_case_url)
        find_case_xml_contents = find_case_xml_response.read()
        find_case_soup = BeautifulSoup(find_case_xml_contents, 'html.parser')
        case_tag = find_case_soup.find('case')
        return case_tag['id']
