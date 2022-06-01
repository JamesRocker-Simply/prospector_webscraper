# Prospector Webscraper

A service that scrapes through a website or a series of websites finding phone numbers
and emails.

## How

The `webscraper` script has a couple of useful functions that will allow users
to scrape through single or multiple websites. If you want to get both email and
phone details from a site, you can use either the `mass_webscrape` function for
a list of sites or `single_site_scrape` for one site.

Once the url is passed to these functions, we use the beautiful soup library to 
parses the raw html. We can then find objects in the text using the library built
in tools or parse the rendered html object text directly.

Once the page html is parsed, the script will try to extract the details from the
site using the `matcher` module. This module has functions that find details
using a variety of different techniques to find both email and phone numbers.

In the event of the `matcher` module not finding the details from the base url
it will check some potential urls where the details might be present, for example:

- example.com/about-us
- example.com/contactus
- example.com/contact

Full list is in the `_url_list` function.

If the `matcher` module does match it will return a json payload with the found details,
the url the details were found and the name of the function that found the details.
This is useful for logging and in the event of false positives we know what function
needs to be refined. Example response

```json
{
    "contact_email": "mail@dummy.co.uk",
    "contact_number": "0999 999 9999",
    "email_found_at_url": "https://www.dummy.co.uk/contact-us",
    "email_found_by_func": "find_by_email_regex",
    "number_found_at_url": "https://www.dummy.co.uk/contact",
    "number_found_by_func": "find_by_standard_uk_mobile"
}
```

In the event that more matching techniques need to be included, all you have to
do is add the function to the matcher module and then add it to either the
`get_phone` or `get_email` function list variable.

## App

There is an app to house the UI and API. The API has a single intended endpoint of
`api/single_submission` with a base_url parameter. This will query a single base url
and respond with a json object. You can also do this through the UI

For the multi-site search there is page to upload Excel files. This will accept a column
with `url` and search for everything in that column. Once the multi search has completed,
the dataframe will be displayed in the page and the results can be downloaded once.

## How to use

### Docker

`docker compose up --build`

### Locally

1. Build your virtual environment with `python3.7 -m venv ./venv && source venv/bin/activate`
   or `source venv/bin/activate` if you already have a virtual environment setup
2. Install the requirements with `pip install -r requirements.txt`
3. Run what you need. For example, if you are testing the flask app, use `python3 src/app.py`.
   You can also use intellij and run script files individually.

## Testing

Pytest for testing. Either use the built-in intellij and run or use `pytest` in cli

## Fundamental Issues

This is not a perfect solution as some pages use Javascript to load data dynamically
which include contact details. The only way to get that data would be to use a web
browser automation tool like selenium.

As we are using regex to find phone numbers through large quantities of websites,
there is always going to be the possibility that the script produces false positives
regardless of the quality of regex or language used.

As the sites are obtained through Google, this is reliant that the business owner
puts their site home page. This is not common but out of my 30 sites tested 2 were
either to the wrong page or directed to a subpage.

## Mac Python SSL Issues

One issue you might come into is SSL certificate issues with Python. This is only
an issue with Python 3.6 installed through brew. However, in the event of this issue,
run the `bin/ssl_certificate.py` script to associate Python with an SSL certificate
of your machine.

## For the future

1. We might want to consider connecting the application up with the snowflake instance
   and enable some form of caching some websites aren't repeatedly queried.
2. We might want to use selenium to search pages that are protected by Javascript.
3. We might want to look into a more complex library [scrapy](https://scrapy.org/)
   which I'm not familiar with but has some useful webspider functions, IP masking,
   asynchronous scraping which would allow for much faster multi scraping
4. We probably want some form of caching, so we don't look at websites where we
   already have data
