![PyPI](https://img.shields.io/pypi/v/steamcrawl?label=pypi%20package)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Repo Size](https://img.shields.io/github/repo-size/Hungreeee/steamcrawl.svg)](https://github.com/Hungreeee/steamcrawl/)
[![GitHub follow](https://img.shields.io/github/followers/Hungreeee.svg?style=social&label=Follow&maxAge=2592000)](https://github.com/Hungreeee?tab=followers)

# steamcrawl

This is still a work in progress. Some functionality are available but not quite fully tested. The final version will be release as v1.0.0.

A package that helps extract Steam store and community market data as pandas DataFrame for better readability and usability. The package makes queries to different Steam API, clean and extract the important variables from the JSON object result and return a pandas Dataframe. 

With the Steam request limit, you can make 200 requests every 5 minutes. If you exceed the limit, Steam can give you a cooldown of (possibly) a few 1,2 minutes to 6 hours (depending on the API). Please make an appropriate number of requests at a given time. It is recommended to close any Steam web and application to limit the requests you are sending.

## Installation and setup

The following libraries are used in the package. Thus, the requirement of their installation must be met:

- pandas==1.5.1
- requests==2.29.0
- selenium-wire==5.1.0

You can download the package from PyPI using pip:

```python
pip install steamcrawl
```

Before starting, you need to obtain the value of the cookie `steamLoginSecure`. This can be done by opening DevTools (Ctrl + Shift + I) on steamcommunity.com, Application (on the task bar), Cookies:

The package requires this value to be passed in order to return the data using the information related to you (for example currency). Please be aware that it is absolutely safe to put your `steamLoginSecure` into the program. The package does not attempt to record/send to another source any of your information; even with your `steamLoginSecure` value, there is nothing valuable another user can extract (for e.g make trades, credit card info, etc.) because Steam does not allow any important decisions being made throughout the API.

## Documentation

The documentation is available at the [GitHub Wiki](https://github.com/Hungreeee/steamcrawl/wiki).

## Example 

Initialize the Request class with your `steamLoginSecure` as string:

```python
from steamcrawl import Request
import pandas as pd

request = Request('your steamLoginSecure here')
```

**Get your market trade history:**

```python
data_frame = request.get_market_history(count = 10)
data_frame.to_csv('example.csv')
```

The obtained result is (this is only part of the result):

![example1](https://github.com/Hungreeee/steamcrawl/assets/46376260/110a98ca-d782-4e3c-aec1-e505cde27efd)

**Get buy/sell orders of an item:**

```python
data_frame = get_buysell_orders(item_name = "USP-S | Printstream (Field-Tested)", appid="730")
# appid 730 indicates Counter-Strike: Global Offensive game. 
# Obtain the appid for a game using get_all_appid().
data_frame.to_csv('example.csv')
```

The obtained result is (this is again only part of the result). 

![example2](https://github.com/Hungreeee/steamcrawl/assets/46376260/1879c84a-edcb-4c03-9f6a-b004dee69920)

A small note is, please do not be alerted by the popping up browser for this request, this is only the behavior of the seleniumwire package used for this function.

## Contributions:

This project is created and managed by only one user Hungreeee. Therefore, errors are entirely possible to occur anywhere in the program. If you found any bug you would like to report, please open a new Issue.

If you would like to suggest changes to current features or new features implementation, please also open a new Issue and I will check it out as soon as I can. 

## Legal

This project is in no way affiliated with, authorized, maintained, sponsored or endorsed by Valve or any of its affiliates or subsidiaries. This is an independent and unofficial project created by Hungreeee. Use it at your own risk.
