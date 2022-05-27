import os
import sys

import bs4

# allows us to run pytest through intellij or through cli
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.matcher import phone_number_finder

url = "test_url"


def test_find_by_uk_landline_brackets():
    with open(f"{SCRIPT_DIR}/test_html_objects/base_landline_test.html") as fp:
        soup = bs4.BeautifulSoup(fp, "html.parser")
    expected_response = "(0)1999 999 999", "find_by_uk_landline", url
    assert phone_number_finder.find_by_uk_landline(soup, url) == expected_response


def test_find_by_uk_landline_five_six():
    with open(f"{SCRIPT_DIR}/test_html_objects/base_landline_test.html") as fp:
        new_text = fp.read().replace("(0)1999 999 999", "01999 999999")
    soup = bs4.BeautifulSoup(new_text, "html.parser")
    expected_response = "01999 999999", "find_by_uk_landline", url
    assert phone_number_finder.find_by_uk_landline(soup, url) == expected_response


def test_find_by_uk_landline_five_double_three():
    with open(f"{SCRIPT_DIR}/test_html_objects/base_landline_test.html") as fp:
        new_text = fp.read().replace("(0)1999 999 999", "01999 999 999")
    soup = bs4.BeautifulSoup(new_text, "html.parser")
    expected_response = "01999 999 999", "find_by_uk_landline", url
    assert phone_number_finder.find_by_uk_landline(soup, url) == expected_response


def test_find_by_tel_href():
    with open(f"{SCRIPT_DIR}/test_html_objects/base_landline_test.html") as fp:
        new_text = fp.read().replace(
            "(0)1999 999 999", '<a href="tel:01999 999999">Call us!</a>'
        )
    soup = bs4.BeautifulSoup(new_text, "html.parser")
    expected_response = "01999 999999", "find_by_tel_href", url
    assert phone_number_finder.find_by_tel_href(soup, url) == expected_response


def test_find_by_uk_landline():
    with open(f"{SCRIPT_DIR}/test_html_objects/base_landline_test.html") as fp:
        new_text = fp.read().replace("(0)1999 999 999", " 01999 999999 ")
    soup = bs4.BeautifulSoup(new_text, "html.parser")
    expected_response = "01999 999999", "find_by_uk_landline", url
    assert phone_number_finder.find_by_uk_landline(soup, url) == expected_response
