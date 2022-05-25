import pandas as pd
import requests
import bs4
from matcher import phone_number_finder as pnf
from matcher import email_finder as ef


def _parse_function_loop(parsed_soup, list_of_functions, url):
    contact_data = None
    for each in list_of_functions:
        if contact_data is None:
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


def get_phone(base_url):
    # Wrapper function to call the validation methods in the phone_number_finder module
    number_match_function = [
        pnf.find_from_call_to,
        pnf.find_by_e164_format,
        pnf.find_by_standard_uk_mobile,
        pnf.find_by_tel_href,
        pnf.find_by_uk_landline,
    ]
    number_found = None
    list_of_urls = _url_list(base_url)
    for url in list_of_urls:
        if number_found is None:
            try:
                # pass these headers to trick the site thinking we are a human
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                number_found = _parse_function_loop(soup, number_match_function, url)
                return number_found
            except:
                pass

    if number_found is None:
        print("Number not found")
        return "", "missing", base_url


def get_email(base_url):
    email_match_func = [ef.find_by_regex, ef.find_by_mail_to, ef.find_by_mail_href]
    email_found = None
    for url in _url_list(base_url):
        if email_found is None:
            try:
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                email_found = _parse_function_loop(soup, email_match_func, url)
                return email_found
            except:
                pass

    if email_found is None:
        print("Email not found")
        return "", "missing", base_url


def mass_webscrape(list_of_sites):
    for base_url in list_of_sites:
        try:
            phone = get_phone(base_url)
            email = get_email(base_url)
            print(f"Base Url: {base_url}\nPhone: {phone}\nEmail: {email}\n")
        #     probably needs to be a generator object to keep looping
        except requests.exceptions.RequestException:
            print(
                f"Url {base_url} either does not exist, no longer exists or does not respond"
            )
            # continue
        except Exception as e:
            print(e)
            print(
                f"Unsuccessful call to {base_url} response is: {requests.get(base_url)}"
            )
            # continue


def single_site_scrape(base_url):
    try:
        phone = get_phone(base_url)
        email = get_email(base_url)
        print(f"Base Url: {base_url}\nPhone: {phone}\nEmail: {email}\n")
        return base_url, phone, email
    except requests.exceptions.RequestException:
        print(f"{base_url} either does not exist, no longer exists or does not respond")
    except Exception as e:
        print(e)
        print(f"Unsuccessful call to {base_url} response is: {requests.get(base_url)}")


"""
Test cases
https://babahabuandco.co.uk/
https://afe-plumbing-services.business.site/ # True negative on no email
https://lbplumbingandheating.com/
http://londoncitybuilders.com/ 
https://lvassociates.co.uk/ # True negative on email address
http://www.pentwynbuild.com/
https://www.innovatedb.com/
https://chatteringbuilders.com/ # False negative on the email. Email is Javascript protected
https://fgsaccountancy.co.uk/
http://www.bdaccountants.co.uk/
http://www.plumbdreamemergencyplumberpeckham.co.uk/ # True negative of email
https://grantbuilders.co.uk/
https://www.cehill.co.uk/
https://www.barnes-itsolutions.co.uk/
https://www.trinityconstruction.co.uk/
https://www.mini-diggers-hire.co.uk/
http://www.verticalbuildersltd.co.uk/
http://www.cbsinfo.co.uk/
https://grantbuilders.co.uk/
https://gwbhorticulture.co.uk/
https://www.eurocell.co.uk/branch-finder/thetford # False negative on email loaded in through Javascript
http://robanbuilders.co.uk/
https://www.langleysbuildingservicesltd.co.uk/
http://www.easterndrainageservices.co.uk/index.html
https://astaradvisory.co.uk/
https://www.bennettsbuilding.co.uk/
http://pasnell.co.uk/
https://brownsofraskelf.co.uk/
https://www.nobleaccountants.com/ # updated regex for specific area codes 
"""
if __name__ == "__main__":
    # forward slash must be at the end of the site address.
    single_site_scrape("https://www.nobleaccountants.com/")
