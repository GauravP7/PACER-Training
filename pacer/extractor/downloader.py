import pacer_scrape as pacer_scraper

extractor_obj = pacer_scraper.Extractor()
downloader_obj = pacer_scraper.Downloader()

extractor_type = extractor_obj.set_extractor_type()

# [ Step 1 of 8 ] : Hit the first page of PACER training site and Login.
login_page_contents = downloader_obj.login_pacer()

# [ Step 2 of 8 ] : Validate the Login.
downloader_obj.validate_login_success(login_page_contents)

# [ Step 3 of 8 ] : Parse the contents and get cookie.
downloader_obj.set_cookie_value(login_page_contents)

# [ Step 4 of 8 ] : Query as per the input criteria.
case_details_page_contents = downloader_obj.get_case_details_page_contents()

if extractor_type == "DATE_RANGE":

    # [ Step 5 of 8 ] : Save the Web page (HTML content) in a folder.
    file_names_list = downloader_obj.save_all_case_details_page(case_details_page_contents)
    file_names_object = open('/home/mis/DjangoProject/pacer/extractor/Contents/file_names.txt', 'w')
    for file_name in file_names_list:
        file_names_object.write(file_name + '\n')

elif extractor_type == "REFRESH_CASE":
    # [ Step 5 of 8 ] : Save the Web page (HTML content) in a folder.
    downloader_obj.get_page_based_on_case_number(extractor_obj.case_number)

elif extractor_type == "PACER_IMPORT_CASE":
    # [ Step 5 of 8 ] : Save the Web page (HTML content) in a folder.
    new_case_file_name = downloader_obj.save_new_case(case_details_page_contents, extractor_obj.case_number)
    file_names_object = open('/home/mis/DjangoProject/pacer/extractor/Contents/import_case_file_name.txt', 'w')
    file_names_object.write(new_case_file_name)
