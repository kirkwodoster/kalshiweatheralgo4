from fake_useragent import UserAgent
import logging
import numpy as np
import time
import random
from datetime import datetime, timedelta
import pytz

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from weatheralgo import trade_functions
from weatheralgo import scrape_functions
from weatheralgo import util_functions
from weatheralgo import inputs


# Initialize Selenium WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-data")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')
    ua = UserAgent()
    chrome_options.add_argument(f"user-agent={ua.random}")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)



# Main function to scrape and process data
def scrape_dynamic_table(driver, lr_length, count, scraping_hours, yes_price, locations):
    
    util_functions.logging_settings()
    temperatures = []
    
    restart_threshold = 20  # Restart WebDriver every 50 iterations
    loop_counter = 0

    rand = random.randint(2, 4)
    

    market_dict = {
        "KXHIGHDEN": [None,None],
        "KXHIGHCHI": [None,None],
        "KXHIGHMIA": [None,None],
        "KXHIGHAUS": [None,None],
        "KXHIGHPHIL": [None,None],
        "KXHIGHLAX": [None,None]
                }
    
    while True:
        
        # cali_time = datetime.now(pytz.timezone("America/Los_Angeles"))
        
        
        model_inputs = inputs.model_input
        print(market_dict)
        
        for i,j in zip(locations, market_dict.keys()):
            market, timezone, url, xml_url = model_inputs(i)
        
            forecasted_high = inputs.forecasted_high_gate(
                                                         market_dict=market_dict,
                                                         market=market,
                                                         xml_url=xml_url,
                                                         timezone=timezone
                                                        )
            
            # forecasted_high_date = scrape_functions.xml_scrape(xml_url, timezone)[0]
            if forecasted_high:
                current_timezone, forecasted_high_date = forecasted_high
                current_timezone = current_timezone.date()
                market_dict[market] = [current_timezone, forecasted_high_date]
                
            
            forecasted_high_date = market_dict[j][1]       

            permission_scrape = scrape_functions.permission_to_scrape(
                                                                    market=market, 
                                                                    timezone=timezone, 
                                                                    scraping_hours=scraping_hours, 
                                                                    expected_high_date=forecasted_high_date,
                                                                    )
            
            scrape = scrape_functions.scrape_temperature(driver=driver, url=url)
            
            print(f'forecasted_high_date {forecasted_high_date}')

            time.sleep(rand)
            try:
                print(f'Permission Scrape: {permission_scrape} market: {market}')
                if permission_scrape:

                    current_temp = scrape[1][-1]
                    temperatures = scrape[1]
                    
                    print(f'Market: {market}')
                    print(f'Current Temp: {current_temp}')
                    print(f'Temperature: {temperatures}')
                    print(f'expected high date {forecasted_high_date}')
                    
                    current_temp_is_max = trade_functions.if_temp_reaches_max(
                                                                              current_temp=current_temp, 
                                                                              market = market, 
                                                                              yes_price=yes_price,
                                                                              count=count,
                                                                              temperatures=temperatures,
                                                                              timezone=timezone
                                                                            )
                    
                    if current_temp_is_max:
                        logging.info('Max Temperature Reached')
                    
                    trade_criteria = trade_functions.trade_criteria_met(
                                                                        temperatures=temperatures, 
                                                                        lr_length=lr_length,
                                                                        market=market,
                                                                        yes_price=yes_price,
                                                                        count=count,
                                                                        timezone=timezone,
                                                                        
                                                                        )
                    
                    print(f'Max Temp {current_temp_is_max}')
                    print(f'Trade Criteria: {trade_criteria}')
                

                    if trade_criteria:
                        logging.info('Trade Criteria Met')
                    
                    else:
                        time.sleep(rand)    
                    
                    is_order_filled = util_functions.order_filled(market=market, timezone=timezone)
                    
                    if is_order_filled:
                        logging.info(f'Order filled and saved: {market}')
                    else:
                        continue
                
                else:
                    continue
            
            except Exception as e:
                logging.error(f"in main loop: {e}")

        loop_counter += 1
        if loop_counter >= restart_threshold:
            logging.info("Restarting WebDriver to prevent stale sessions...")
            driver.quit()
            driver = initialize_driver()
            loop_counter = 0  # Reset counter

        
        time.sleep(rand)
