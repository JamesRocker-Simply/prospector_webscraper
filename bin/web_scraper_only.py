from src.webscraper.selenium_scrape import setup_webdriver, selenium_clean_up
from src.webscraper.webscraper import mass_webscrape

from src.webscraper.data_manipulation import file_management as fm

if __name__ == "__main__":
    # forward slash must be at the end of the site address.
    import time

    start_time = time.time()
    selenium_driver = setup_webdriver()
    try:
        # output = single_site_scrape("https://babahabuandco.co.uk/", driver)
        # print(output)
        file = "../list_of_sites.xlsx"
        site_list = fm.read_excel_get_url_series(file)
        fm.output_excel_file(
            "output.xlsx",
            fm.data_dict_to_pandas(mass_webscrape(site_list, selenium_driver)),
        )  # app production
        # fm.output_excel_file('../dry_output.xlsx', fm.data_dict_to_pandas(dry_run(site_list)))
        selenium_clean_up(selenium_driver)
    except FileNotFoundError:
        print("file not found")
        selenium_clean_up(selenium_driver)
    print("--- %s seconds ---" % (time.time() - start_time))
