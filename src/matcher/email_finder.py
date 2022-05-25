import re
import inspect


def find_by_regex(soup, url):
    found_email = re.findall(
        r"([a-zA-Z\d._-]+@[a-zA-Z\d._-]+\.[a-zA-Z\d_-]+)", soup.text
    )
    return found_email[-1], inspect.stack()[0][3], url


def find_by_mail_to(soup, url):
    return soup.select("a[href*=mailto]")[-1].text, inspect.stack()[0][3], url


def find_by_mail_href(soup, url):
    for a in soup.find_all("a", href=True):
        # print(a["href"])
        if "https://mail." in a["href"]:
            clean_string = a["href"].replace("callto", "")
            return clean_string, 1, inspect.stack()[0][3], url
    # return soup.select("a[href*=mailto]")[-1].text, inspect.stack()[0][3], url
    raise Exception
