# **UKLawScraper**
------
UKLawScraper is a module, allows you to retrieve judgments and decisions information from 2003 onwards, from Find case law in a friendly, Pythonic way without having to solve CAPTCHAs.

## Installation
-----
UKLawScraper can be installed with pip. To install using pip, simply run:
```python
pip install UKLawScraper
```
This package has 3 main modules:
* CaseInfoScraper
* CaseHeaderScraper
* FullTextScraper
* Save_to_json

### 1- CaseInfoScraper
---
This module contains 2 functions. These functions scrape Link, Name of the Case, judgment-listing__court, judgment-listing__neutralcitation and Datetime for a page or multipages.
Funcrions:
* scrape_judgments
* scrape_all_judgments_info

### 2- CaseHeaderScraper
---
This module has 3 functions. First module give us just page's urls that use in second and third functions. (So you have to run **scrape_judgment_urls** first) then, second function gives us direct download case's PDFs and the last one, scrape case header info :)
Functions:
* scrape_judgment_urls
* judgment_Dlink
* scrape_header_info

### 3- FullTextScraper
---
This module has 3 function. It gets output of scrape_header_info and scrape all text of each cases.
Functions:
* load_json
* scrape_full_text
* OutputScraper

### Save in JSON format
----
This scraper has one more function to save data in a stable format named **SaveToJson**

#### More information in github repository page in [UKLawScraper](https://github.com/mrjoneidi/UKLawScraper)
----

