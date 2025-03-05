#from cryptography.hazmat.primitives import serialization
#import asyncio
# from weatheralgo.clients import  KalshiWebSocketClient
import logging
import pytz
from weatheralgo.model import weather_model
from weatheralgo import util_functions
from weatheralgo import scrape_functions
from weatheralgo import trade_functions
from weatheralgo.clients import client
from datetime import datetime, timedelta
import pytz
import time
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dateutil import tz

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
    

    
    #  model_inputs = inputs.model_input
    #  for i in inputs.locations:
    #     market, timezone, url, xml_url = model_inputs(i)
    #     # print(market)
    #     x =  scrape_functions.trade_today(market, timezone)
    #     # print(x)
    
    #     today = datetime.now(timezone)
    #     todays_date = today.strftime('%y%b%d').upper()
    #     event = f'{market}-{todays_date}'
    #     orders = client.get_orders(event_ticker=event)['orders']
    #     # print(orders)
        
        
    #     if len(orders) >= 1:
    #         order_list = [scrape_functions.iso_to_local_time(iso_string = i['created_time'], timezone=str(timezone)) for i in orders]
    #         # print(order_list)
    #         # print(today.date())
    #         if str(today.date()) in order_list:
    #             print(ru)
    #             print(market)
    #             print(today.date())
    #             print(order_list)
 
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


