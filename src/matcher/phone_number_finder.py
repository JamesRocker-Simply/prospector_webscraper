"""
The problem with search for phone numbers is that it produces false positives.
The more regex we add, the more likely we will pick up things that aren't phone numbers

For the outputs we have the phone number, the function that found it and the url it was found at
"""

import re
import inspect
import bs4


def find_by_data_field(soup: bs4.BeautifulSoup, url):
    # Finding a div with data-field of phone, get just the numbers
    # Then find numbers with the format 07{+9 other digits}, +447{+9 other digits} or 07{+3 digits} {+5 digits}
    phone_data_field = soup.find("div", {"data-field": "phone"})
    just_number = re.sub("\D", "", phone_data_field.text)
    found_number = re.findall(r"(07\d{9}|447\d{9}|07\d{3}[ \t]\d{6})$", just_number)[0]
    return found_number, inspect.stack()[0][3], url


def find_from_call_to(soup: bs4.BeautifulSoup, url):
    # find numbers that are contained in a hyperlink of 'callto' to auto call them
    for a in soup.find_all("a", href=True):
        if "callto:" in a["href"]:
            clean_string = a["href"].replace("callto", "")
            return clean_string, inspect.stack()[0][3], url
    # found_phone_number = soup.select("a[href*=callto]")[0].text # old version
    # return found_phone_number, 1, inspect.stack()[0][3], url
    raise Exception


def find_by_e164_format(soup: bs4.BeautifulSoup):
    # find numbers with the standard e164 format
    found_phone_number = re.findall("^\+[1-9]\d{1,14}$", soup.text)[0].text
    return found_phone_number, inspect.stack()[0][3]


def find_by_tel_href(soup: bs4.BeautifulSoup, url):
    # find numbers that are contained in a hyperlink or 'tel:' to auto call them
    for a in soup.find_all("a", href=True):
        if "tel:" in a["href"]:
            clean_string = a["href"].replace("tel:", "")
            return clean_string, inspect.stack()[0][3], url
    # Exception because it's expected to break
    # This allows encapsulating try statement to catch it then move on
    raise Exception


def find_by_standard_uk_mobile(soup: bs4.BeautifulSoup, url):
    # Find mobile numbers with the format 07{9 other digits}, +447{9 other digits}, 07{3 digits} {5 digits}
    # or 0{+3 digits} {3 digits} {4 digits}
    found_phone_number = re.findall(
        r"\s+(07\d{9}|\+447\d{9}|07\d{3}[ \t]\d{6})\s|"
        r"(07\d{9}|447\d{9}|07\d{3}[ \t]\d{6}|0\d{3}[ \t]\d{3}[ \t]\d{4})",
        soup.text,
    )[0]
    if isinstance(found_phone_number[0], str) and found_phone_number[0] != "":
        return found_phone_number[0], inspect.stack()[0][3], url
    else:
        return found_phone_number[-1], inspect.stack()[0][3], url


def find_by_uk_landline(soup: bs4.BeautifulSoup, url):
    # Find landline numbers with the format 0{+9-10 digits} or 0{+4 digits} {+6 digits}, 0{4 digits} {3 digits} {3
    # digits} or (0){4 digits} {3 digits} {3 digits}
    # Landlines can't start with 00 and must comply with area codes
    # https://en.wikipedia.org/wiki/Telephone_numbers_in_the_United_Kingdom#Format
    found_phone_number = re.findall(
        r"(0[1-9]\d{7,9}|0+[1-9]\d{3}[ \t]\d{5,6}|0[1-9]\d{3}[ \t]\d{3}[ \t]\d{3}|\((0)\)\[1-9]d{3}[ \t]\d{3}[ \t]\d{3})",
        soup.text,
    )

    if isinstance(found_phone_number[0], str) and found_phone_number[0] != "":
        return found_phone_number[0], inspect.stack()[0][3], url
    else:
        # if multiple objects are found
        return found_phone_number[0][0], inspect.stack()[0][3], url


def match_by_us_format(soup: bs4.BeautifulSoup, url):
    """
    Find numbers with the following formats. We might need this later if we apply this to the US
    123-456-7890
    (123) 456-7890
    123 456 7890
    123.456.7890
    +91 (123) 456-7890
    :param url:
    :param soup:
    :return:
    """
    found_phone_number = re.findall(
        r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$", soup.text
    )[0].text
    return found_phone_number, inspect.stack()[0][3], url
