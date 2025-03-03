
lr_length = 7
hour = 2
scraping_hours = [500,500]
yes_price = 1
count = 1

scrape_inputs = {
    'lr_length': lr_length,
    'hour': hour,
    'scraping_hours': scraping_hours,
    'yes_price': yes_price
        
                }

all_markets = {
            "DENVER": {
                "SERIES": "KXHIGHDEN",
                "TIMEZONE": "America/Denver",
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