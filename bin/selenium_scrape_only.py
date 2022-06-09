from src.webscraper.selenium_scrape import setup_webdriver, selenium_get_page, selenium_extract_data, selenium_clean_up

if __name__ == "__main__":
    # we only want the import in the script as we don't want circular imports
    from src.webscraper.matcher import email_finder as ef
    from src.webscraper.matcher import phone_number_finder as pnf

    # The eurocell url is good for testing as the email element is JS protected
    url_to_scrape = "https://www.eurocell.co.uk/branch-finder/thetford"
    # urls_to_scrape = []
    # for url in urls_to_scrape:
    #     get_obj(url)
    #     locate()
    initial_driver = setup_webdriver()
    selenium_get_page(url_to_scrape, initial_driver)
    email_match_func = [
        ef.find_by_mail_to,
        ef.find_by_mail_href,
        ef.find_by_email_regex,
    ]

    number_match_function = [
        pnf.find_from_call_to,
        pnf.find_by_e164_format,
        pnf.find_by_standard_uk_mobile,
        pnf.find_by_tel_href,
        pnf.find_by_uk_landline,
    ]
    print(selenium_extract_data(email_match_func, initial_driver))
    print(selenium_extract_data(number_match_function, initial_driver))
    selenium_clean_up(initial_driver)
