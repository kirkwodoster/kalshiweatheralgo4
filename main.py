#from cryptography.hazmat.primitives import serialization
#import asyncio
# from weatheralgo.clients import  KalshiWebSocketClient
import logging
import pytz
from weatheralgo.model import weather_model
from weatheralgo import util_functions
from weatheralgo import scrape_functions
from weatheralgo import trade_functions
from weatheralgo.input_variables import Input
from weatheralgo.clients import client
from datetime import datetime, timedelta
import pytz
import time
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from weatheralgo import inputs
# from weatheralgo.clients import client



# Initialize the WebSocket client
# ws_client = KalshiWebSocketClient(
#     key_id=client.key_id,
#     private_key=client.private_key,
#     environment=client.environment
# )

# Connect via WebSocket
# asyncio.run(ws_client.connect())

if __name__ == "__main__":
    
    # xml_url = "https://forecast.weather.gov/MapClick.php?lat=33.9425&lon=-118.409&FcstType=digitalDWML"
    # scraping_hours = [60,60]
    # timezone = pytz.timezone("America/Los_Angeles")
    # expected_high_date = scrape_functions.xml_scrape(xml_url, timezone)[0]
    # today = datetime.now(timezone)
    # start_scrape = today >= expected_high_date - timedelta(minutes=scraping_hours[0])
    # end_scrape = today <= expected_high_date + timedelta(minutes=scraping_hours[1])
    
    # print(end_scrape)


    driver =  weather_model.initialize_driver()
    
    scraping_inputs = inputs.scrape_inputs
    
    util_functions.logging_settings()
    
    try:
       weather_model.scrape_dynamic_table(driver, **scraping_inputs)
        # scrape_functions.scrape_temperature(driver=driver,url=url)
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
    finally:
        driver.quit()
        logging.info("WebDriver closed.")


