
import pytz
from datetime import datetime
from weatheralgo import scrape_functions
import logging

lr_length = 5
hour = 2
scraping_hours = [60,60]
yes_price = 1
count = 1


all_markets = {
            "DENVER": {
                "SERIES": "KXHIGHDEN",
                "TIMEZONE": "US/Mountain",
                "URL": f"https://www.weather.gov/wrh/timeseries?site=KDEN&hours={hour}",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=39.8589&lon=-104.6733&FcstType=digitalDWML",
            },
            "CHICAGO": {
                "SERIES": "KXHIGHCHI",
                "TIMEZONE": "America/Chicago",
                "URL": f"https://www.weather.gov/wrh/timeseries?site=KMDW&hours={hour}",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=41.7842&lon=-87.7553&FcstType=digitalDWML",
            },
            "MIAMI": {
                "SERIES": "KXHIGHMIA",
                "TIMEZONE": "US/Eastern",
                "URL": f"https://www.weather.gov/wrh/timeseries?site=KMIA&hours={hour}",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=25.7934&lon=-80.2901&FcstType=digitalDWML",
            },
            "AUSTIN": {
                "SERIES": "KXHIGHAUS",
                "TIMEZONE": "US/Central",
                "URL": f"https://www.weather.gov/wrh/timeseries?site=KAUS&hours={hour}",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=30.1945&lon=-97.6699&FcstType=digitalDWML",
            },
            "PHILADELPHIA": {
                "SERIES": "KXHIGHPHIL",
                "TIMEZONE": "US/Eastern",
                "URL": f"https://www.weather.gov/wrh/timeseries?site=KPHL&hours={hour}",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=39.8721&lon=-75.2407&FcstType=digitalDWML",
            },
            "LOS ANGELES": {
                "SERIES": "KXHIGHLAX",
                "TIMEZONE": "America/Los_Angeles",
                "URL": f"https://www.weather.gov/wrh/timeseries?site=KLAX&hours={hour}",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=33.9425&lon=-118.409&FcstType=digitalDWML",
            }
        }

locations = all_markets.keys()
market_inputs = list(all_markets['DENVER'].keys())






# class InputLoop:
#     def __init__(self, lr_length, scraping_hours, count, yes_price):
#         self.lr_length = 6
#         self.scraping_hours = [60,60]
#         self.count = 1
#         self.yes_price = 85
    
#     def input_loop(self, markets, all_markets):
#         self.market = all_markets[markets]['SERIES']
#         self.timezone =  pytz.timezone(all_markets[markets]['TIMEZONE'])
#         self.url = all_markets[markets]['URL']
#         self.xml_url = all_markets[markets]['XML_URL']
        
        
def model_input(markets):
    try:
        market = all_markets[markets]['SERIES']
        timezone =  pytz.timezone(all_markets[markets]['TIMEZONE'])
        url = all_markets[markets]['URL']
        xml_url = all_markets[markets]['XML_URL']
        return market, timezone, url, xml_url
    
    except Exception as e:
        logging.error(f"model_input: {e}")



def forecasted_high_gate(market_dict, market, xml_url, timezone):
    
    try:
        current_timezone = datetime.now(timezone)

        if market_dict[market] != current_timezone.date():
            
            current_timezone = datetime.now(timezone)
            expected_high_date = scrape_functions.xml_scrape(xml_url, timezone)[0]

            
            return current_timezone, expected_high_date
        else:
            return False
    except Exception as e:
        logging.error(f"forecasted_high_gate: {e}")
    

scrape_inputs = {
    'lr_length': lr_length,
    'count': count,
    'scraping_hours': scraping_hours,
    'yes_price': yes_price,
    'locations': locations      
                }

