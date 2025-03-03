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
def scrape_dynamic_table(driver):
    
    util_functions.logging_settings()
    temperatures = []
    
    restart_threshold = 20  # Restart WebDriver every 50 iterations
    loop_counter = 0

    rand = random.randint(2, 4)
    timezone =  pytz.timezone("America/Los_Angeles")
    

    today = datetime.now(timezone).date() + timedelta(hours=3)
    # expected_high_date = scrape_functions.xml_scrape(xml_url, timezone)[0]

    while True:
        
        lr_length = inputs.lr_length
        scraping_hours = inputs.scraping_hours
        count = inputs.count
        yes_price = inputs.yes_price

        current_local_date = datetime.now(timezone).date() + timedelta(hours=3)
        if today != current_local_date:
           today = current_local_date
           
           
        for i in inputs.locations:
            market = inputs.all_markets[i]['SERIES']
            timezone =  pytz.timezone(inputs.all_markets[i]['TIMEZONE'])
            url = inputs.all_markets[i]['URL']
            xml_url = inputs.all_markets[i]['XML_URL']   
           
            expected_high_date = scrape_functions.xml_scrape(xml_url, timezone)[0]
            

            permission_scrape = scrape_functions.permission_to_scrape(
                                                                    market=market, 
                                                                    timezone=timezone, 
                                                                    scraping_hours=scraping_hours, 
                                                                    expected_high_date=expected_high_date,
                                                                    )
            
            scrape = scrape_functions.scrape_temperature(driver=driver, url=url)

            time.sleep(rand)
            try:

                if permission_scrape:

                    current_temp = scrape[1][-1]
                    temperatures = scrape[1]
                    
                    print(market)
                    print(current_temp)
                    print(temperatures)
                    print(f'expected high date {expected_high_date}')
                    
                    current_temp_is_max = trade_functions.if_temp_reaches_max(
                                                                            current_temp=current_temp, 
                                                                            market = market, 
                                                                            yes_price=yes_price,
                                                                            count=count,
                                                                            temperatures=temperatures,
                                                                            )
                    
                    trade_criteria = trade_functions.trade_criteria_met(
                                                                        temperatures=temperatures, 
                                                                        lr_length=lr_length,
                                                                        market=market,
                                                                        yes_price=yes_price,
                                                                        count=count
                                                                        )
                    print(current_temp_is_max)
                    print(trade_criteria)
                    
                    if current_temp_is_max:
                        logging.info('Max Temperature Reached')

                    if trade_criteria:
                        logging.info('Trade Criteria Met')
                    
                    else:
                        time.sleep(rand)
                    
                    is_order_filled = util_functions.order_filled(market)
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
