# Prospector Webscraper

A service that scrapes through a website or a series of websites finding phone numbers
and emails.

## How

The `prospector_webscraper` script has a couple of useful functions that will allow
us to scrape through websites. If you want to get both email and phone details from
a site, you can use either the `mass_webscrape` function for a list of sites or
`single_site_scrape` for one site.

Once the url is passed to these functions, the beautiful soup library parses the
raw html. We can then find objects in the text using beautiful soups built in tools
or parse the rendered html object text directly.

Once the page html is parsed, the script will try to extract the details from the
site using the matcher module. This module has functions that find details
using a variety of different matcher techniques for both email and phone numbers.

In the event of the matcher module not finding the details from the base url it will
check some potential urls where the details might be present, for example:

- example.com/about-us
- example.com/contactus
- example.com/contact

Full list is in the `_url_list` function.

If the matcher module does match it will return a tuple object with the found details,
the url the details were found and the name of the function that found the details.
This is useful for logging and in the event of false positives we know what function
needs to be refined. Example response

```
Phone: ('01768 88738', 'find_by_uk_landline', 'https://www.nobleaccountants.com/')
Email: ('noble@nobleaccountants.co.uk', 'find_by_regex', 'https://www.nobleaccountants.com/')
```

In the event that more matching techniques need to be included, all you have to
do is add the function to the matcher module and then add it to either the
`get_phone` or `get_email` function list variable.

## Fundamental Issues

This is not a perfect solution as some pages use Javascript to load data dynamically
which include contact details. The only way to get that data would be to use a web
browser automation tool like selenium.

As we are using regex to find phone numbers through large quantities of websites,
there is always going to be the possibility that the script produces false positives
regardless of the quality of regex or language used.

As the sites are obtained through Google, this is reliant that the business owner
puts the correct home page.

## Testing

Pytest for testing. Either use the built-in intellij and run or use `pytest` in cli

## Mac Python SSL Issues

One issue you might come into is SSL certificate issues with Python. This is only
an issue with Python 3.6 installed through brew. However, in the event of this issue,
run the `bin/ssl_certificate.py` script to associate Python with an SSL certificate
of your machine.
