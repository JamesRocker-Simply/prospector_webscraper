import bs4
import requests

from data_manipulation import file_management as fm
from matcher import email_finder as ef
from matcher import phone_number_finder as pnf


def _parse_function_loop(parsed_soup, list_of_functions, url):
    for each in list_of_functions:
        try:
            return each(parsed_soup, url)
        except:
            pass
    raise Exception


def _url_list(base_url):
    return [
        base_url,
        f"{base_url}contact",
        f"{base_url}contactus.html",
        f"{base_url}contact_us",
        f"{base_url}about",
        f"{base_url}about-us",
        f"{base_url}contact-us",
    ]


def get_data(list_of_urls, matcher):
    for url in list_of_urls:
        try:
            # pass these headers to trick the site thinking we are a human
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            data_object = _parse_function_loop(soup, matcher, url)
            return data_object
        except:
            pass


def get_phone(base_url):
    # Wrapper function to call the validation methods in the phone_number_finder module
    number_match_function = [
        pnf.find_from_call_to,
        pnf.find_by_e164_format,
        pnf.find_by_standard_uk_mobile,
        pnf.find_by_tel_href,
        pnf.find_by_uk_landline,
    ]
    list_of_urls = _url_list(base_url)
    data_object = get_data(list_of_urls, number_match_function)

    if data_object is None:
        print(f"Number not found for {base_url}")
        return "", "", ""
    return data_object


def get_email(base_url):
    email_match_func = [
        ef.find_by_email_regex,
        ef.find_by_mail_to,
        ef.find_by_mail_href,
    ]
    list_of_urls = _url_list(base_url)
    data_object = get_data(list_of_urls, email_match_func)

    if data_object is None:
        print(f"Email not found for {base_url}")
        return "", "", ""
    return data_object


def mass_webscrape(list_of_sites):
    for base_url in list_of_sites:
        try:
            trimmed_url = base_url.strip()
            phone = get_phone(trimmed_url)
            email = get_email(trimmed_url)
            output = {
                "base_url": base_url,
                "contact_number": phone[0],
                "number_found_by_func": phone[1],
                "number_found_at_url": phone[2],
                "contact_email": email[0],
                "email_found_by_func": email[1],
                "email_found_at_url": email[2],
            }
            yield output

        except requests.exceptions.RequestException:
            print(
                f"Url {base_url} either does not exist, no longer exists or does not respond"
            )
            continue
        except Exception as e:
            print(e)
            print(
                f"Unsuccessful call to {base_url} response is: {requests.get(base_url)}"
            )
            continue


def single_site_scrape(base_url):
    try:
        phone = get_phone(base_url)
        email = get_email(base_url)
        output = {
            "base_url": base_url,
            "contact_number": phone[0],
            "number_found_by_func": phone[1],
            "number_found_at_url": phone[2],
            "contact_email": email[0],
            "email_found_by_func": email[1],
            "email_found_at_url": email[2],
        }
        return output
    except requests.exceptions.RequestException:
        print(f"{base_url} either does not exist, no longer exists or does not respond")
    except Exception as e:
        print(e)
        print(f"Unsuccessful call to {base_url} response is: {requests.get(base_url)}")


def dry_run(site):
    for each in site:
        output = {
            "base_url": each,
            "contact_number": "07506748262",
            "number_found_by_func": "dry_run",
            "number_found_at_url": each,
            "contact_email": "dummy_email@gmail.com",
            "email_found_by_func": "dry_run",
            "email_found_at_url": each,
        }
        yield output


if __name__ == "__main__":
    # forward slash must be at the end of the site address.
    # single_site_scrape("https://www.landal.co.uk/")
    import time

    start_time = time.time()
    file = "../list_of_sites_testing.xlsx"
    site_list = fm.read_excel_get_url_series(file)
    # for each in mass_webscrape(site_list):
    #     print(each)
    # fm.output_excel_file('dry_output.xlsx', fm.data_dict_to_pandas(mass_webscrape(site_list))) # app production
    fm.output_excel_file('dry_output.xlsx', fm.data_dict_to_pandas(dry_run(site_list)))
    print("--- %s seconds ---" % (time.time() - start_time))
