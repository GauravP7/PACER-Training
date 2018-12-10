import urllib
import urllib2
from bs4 import BeautifulSoup

class FindCase():

    def get_pacer_case_id(self, case_number, opener):
        find_case_url = "https://dcecf.psc.uscourts.gov/cgi-bin/possible_case_numbers.pl?" + case_number
        find_case_xml_response = opener.open(find_case_url)
        find_case_xml_contents = find_case_xml_response.read()
        find_case_soup = BeautifulSoup(find_case_xml_contents, 'html.parser')
        case_tag = find_case_soup.find('case')
        return case_tag['id']
