import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def setup_webdriver():
    # configure the global webdriver allow us to import it later
    options = Options()
    options.headless = True  # hide GUI
    options.add_argument("--headless")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-dev-shm-usage")
    # # configure Chrome browser to not load images and javascript
    options.add_argument("--blink-settings=imagesEnabled=false")

    # Bring it all together
    # TODO: check this works through docker instance
    # try:

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    # except WebDriverException:
    #     options.binary_location = r'/opt/google/chrome/google-chrome'
    #     driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
    #                               options=options)


def selenium_get_page(url, driver):
    try:
        driver.get(url)
        # The program could wait for an element to load
        # However, as we need a generic solution across all sites, timing seems to be the only option
        driver.implicitly_wait(2)
    except Exception as e:
        print(f"Exception occurred, driver has been killed due to: {e}")
        driver.quit()


def _parse_function_loop(parsed_soup, list_of_functions, url):
    for each in list_of_functions:
        try:
            return each(parsed_soup, url)
        except:
            pass
    raise Exception


def selenium_extract_data(matcher_list_functions, driver):
    try:
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
        output = _parse_function_loop(soup, matcher_list_functions, driver.current_url)
        return output
    except Exception:
        raise Exception


def selenium_clean_up(driver):
    driver.quit()
    print("driver process has finished")
