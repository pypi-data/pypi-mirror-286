# SPGMI CIQ Python Library

This library provides functions to authenticate users, retrieve financial data, and fetch market data. It supports three main services: Authentication, Financial Services, and Market Data Services.

## Features

#### 1. Authentication Services:

- Authenticate users with username and password.
- Generate an access token for authenticating services.
- Use refresh tokens to obtain new access tokens without re-authenticating.

#### 2. Financial Services:

- Retrieve point-in-time and historical income statements.
- Fetch current and historical balance sheet data.
- Access point-in-time and historical cash flow statements.
- Retrieve financial data based on specified mnemonics for specific metrics.

#### 3. Market Data Services:

- Fetch point-in-time and time-series pricing data for financial instruments.
- Obtain point-in-time and time-series dividend data.
- Retrieve point-in-time and time-series market metrics for specified identifiers.

#### 4. Proxy Support:

- Ability to use proxy objects for enhanced network communication.

#### 5. Data Format:

- Functions return data in the form of pandas DataFrames, facilitating easy data manipulation and analysis.


## Installation:

Thank you for your interest in our library on PYPI. Please be aware that the version of the library available here is a placeholder/dummy version intended for demonstration purposes only.

Unfortunately, we do not provide an actual Python SDK library for direct integration through PYPI.org. If you have specific inquiries or require further assistance regarding our library, services or potential solutions, please contact our support center at:
[S&P Global Support Center](https://www.support.marketplace.spglobal.com/en/delivery-resources#sec6)


Our team will be happy to assist you and provide guidance based on your needs.

## Basic Usage
Here's a brief example of how to use this package:

```sh
from IPython.core.display_functions import display
from spgmi_api_sdk.authentication.services import SDKAuthenticateServices
from spgmi_api_sdk.financials.services import SDKFinancialServices
from spgmi_api_sdk.marketdata.services import SDKMarketDataServices

#Required Instances
auth_services = SDKAuthenticateServices()
financial_services = SDKFinancialServices()
marketdata_services = SDKMarketDataServices()
```
## Authentication
### get_token()
```sh
username = "--username--"    #Replace with actual username
password = "--password--"    #Replace with actual password
token_response = auth_services.get_token(username, password)
bearer_token = token_response.get("access_token")
```
### get_refresh_token()
```sh
refresh_token_response=auth_services.get_refresh_token("--refresh_token--")
refresh_bearer_token = refresh_token_response.get("access_token")
```
## Fetching Financial Data
Use the following methods from the SDKFinancialServices class to fetch financial data:

Note: All these functions of the financial services will accept identifiers with a maximum of 10.

### 1. get_income_statement_pit
Fetches income statement data for a given point in time.
```sh
response = financial_services.get_income_statement_pit(token=bearer_token, identifiers=["I_US5949181045","2588173","EG1320"],properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
display(response.data)
```

### 2. get_income_statement_historical
Fetches historical income statement data.
```sh
response = financial_services.get_income_statement_historical(token=bearer_token, identifiers=["GV012141","MSFT:NasdaqGS"], properties={"periodType":"IQ_FQ-4"})
display(response.data)
```

### 3. get_balance_sheet_pit
Fetches balance sheet data for a given point in time.
```sh
response = financial_services.get_balance_sheet_pit(token=bearer_token, identifiers=["RX309198","MMM:"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
display(response.data)
```
### 4. get_balance_sheet_historical
Fetches historical balance sheet data.
```sh
response = financial_services.get_balance_sheet_historical(token=bearer_token, identifiers=["I_US5949181045","2588173"], properties={"periodType":"IQ_FQ-2"})
display(response.data)
```

### 5. get_cash_flow_pit
Fetches cash flow data for a given point in time.
```sh
response = financial_services.get_cash_flow_pit(token=bearer_token, identifiers=["2588173","EG1320"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
display(response.data)
```

### 6. get_cash_flow_historical
Fetches historical cash flow data.
```sh
response = financial_services.get_cash_flow_historical(token=bearer_token, identifiers=["MSFT:NasdaqGS","DB649496569"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
display(response.data)
```

### 7. get_financials_pit
Fetches financial data (income statement, balance sheet, cash flow) for a given point in time based on specified mnemonics. This function will accept a maximum of 10 mnemonics.
```sh
response = financial_services.get_financials_pit(token=bearer_token, identifiers=["I_US5949181045","2588173","EG1320","CSP_594918104","IQT2630413","GV012141","MSFT:NasdaqGS","DB649496569","RX309198"], mnemonics=["IQ_CASH_INVEST_NAME_AP"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
display(response.data)
```
### 8. get_financials_historical
Fetches historical financial data based on specified mnemonics. This function will accept a maximum of 10 mnemonics.
```sh
response = financial_services.get_financials_historical(token=bearer_token, identifiers=["I_US5949181045","2588173","EG1320","CSP_594918104","IQT2630413","GV012141","MSFT:NasdaqGS","DB649496569","RX309198"], mnemonics=["IQ_CASH_INVEST_NAME_AP"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
display(response.data)
```

## Fetching MarketData
Use the following methods from the SDKMarketDataServices class to fetch market data:

Note: All these functions of the MarketData services will accept identifiers with a maximum of 10.

### 1. get_pricing_info_pit
Fetches pricing information for a given point in time.
```sh
response = marketdata_services.get_pricing_info_pit(token=bearer_token, identifiers=["I_US5949181045","2588173","EG1320","CSP_594918104","IQT2630413"], properties={}) 
display(response.data)
```

### 2. get_pricing_info_time_series
Fetches historical pricing information over a specified time period. 
```sh
response = marketdata_services.get_pricing_info_time_series(token=bearer_token, identifiers=["CSP_594918104","IQT2630413","GV012141","MSFT:NasdaqGS","DB649496569","RX309198","MMM:"], properties={}) 
display(response.data)
```

### 3. get_dividend_pit_info
Fetches dividend information for a given point in time. 
```sh
response = marketdata_services.get_dividend_pit_info(token=bearer_token, identifiers=["CSP_594918104","IQT2630413","GV012141","MSFT:NasdaqGS"], properties={}) 
display(response.data)
```

### 4. get_dividend_info_time_series
Fetches historical dividend information over a specified time period 
```sh
response = marketdata_services.get_dividend_info_time_series(token=bearer_token, identifiers=["GV012141","MSFT:NasdaqGS","DB649496569","RX309198","MMM:"], properties={}) 
display(response.data)
```

### 5. get_market_info_pit
Fetches market information for a given point in time. 
```sh
response = marketdata_services.get_market_info_pit(token=bearer_token, identifiers=["IQT2630413","GV012141","MSFT:NasdaqGS","DB649496569","RX309198"], properties={}) 
display(response.data)
```
### 6. get_market_info_time_series
Fetches historical market information over a specified time period.
```sh 
response = marketdata_services.get_market_info_time_series(token=bearer_token, identifiers=["AAPL:"], properties={}) 
display(response.data)
```
## Best Practice
```sh
# Best Practice: Secure Credential Management in Jupyter or DataBricks Notebooks
# Store and Retrieve Credentials from a .env File

import os
from dotenv import load_dotenv

# Ensure the .env file is placed in the notebook directory
load_dotenv('py.env')  # Replace 'py.env' with your .env file name if different

# Retrieve API credentials securely
api_username = os.getenv('SDKUSERNAME')  # replace with actual variable which is defined in .env file
api_password = os.getenv('SDKPASSWORD')

# Optional: Check if credentials are correctly retrieved from .env file
# print(api_username)

# Now you can use 'api_username' and 'api_password' in your code securely
# username = api_username    
# password = api_password
```
## Proxy (optional)
```sh
from spgmi_api_sdk.dataservices.model.sdk_proxy import SDKProxy
sdk_proxy_object = SDKProxy(proxy_username="", proxy_password="", proxy_host=None, proxy_port=None, proxy_domain="")
#usage of proxy in all function calls
#token_response = auth_services.get_token(username, password, proxy=sdk_proxy_object)
```

## Note:

Jupyter or Databricks Notebooks
To display the response in Jupyter or Databricks notebooks, use the following command:
```sh
display(response)
```
PyCharm or Other IDEs
To display the response in PyCharm or other IDEs, use the following command:
```sh
display(response.data)
```