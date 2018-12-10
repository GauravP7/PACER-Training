import pacer_scrape as pacer_scraper

extractor_obj = pacer_scraper.Extractor()
downloader_obj = pacer_scraper.Downloader()
extractor_type = extractor_obj.set_extractor_type()
parser_obj = pacer_scraper.Parser()

if extractor_type == "DATE_RANGE":
    file_names_object = open('/home/mis/DjangoProject/pacer/extractor/Contents/file_names.txt', 'r')
    for file_name in file_names_object:
        case_details_tuple = parser_obj.parse_case_details_page(file_name.strip('\n'))
        parser_obj.save_case_details(case_details_tuple, file_name)

elif extractor_type == "REFRESH_CASE":
	 print "Please run the downloader.py file to get the docket entry for the case: " + extractor_obj.case_number

elif extractor_type == "PACER_IMPORT_CASE":
    import_case_file_name_object = open('/home/mis/DjangoProject/pacer/extractor/Contents/import_case_file_name.txt', 'r')
    new_case_file_name = import_case_file_name_object.read()

    # [ Step 7 of 8 ] : Save the case details.
    case_details_tuple = parser_obj.parse_case_details_page(new_case_file_name)
    parser_obj.save_case_details(case_details_tuple, new_case_file_name)
