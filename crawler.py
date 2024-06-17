
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config.webdriver_config import get_chrome_driver
from config.logger_config import Logger
from helper.file_helper import save_to_csv
from helper.metadata_helper import extract_record_metadata

WEBSITE_URL = 'https://fondswelt.hansainvest.com/de/downloads-und-formulare/download-center'

driver = get_chrome_driver()

def crawl_records():
    try:
        driver.get(WEBSITE_URL)

        # Accept cookies
        accept_cookies_button = driver.find_element(By.XPATH, '//*[@id="disclaimer-modal-start"]/div/div/div[3]/button')
        time.sleep(5)
        Logger.info('Closing cookies page')
        accept_cookies_button.click()
        time.sleep(5)

        # Load 100 records per page
        display_records = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0_length"]/label/select/option[3]')
        Logger.info('Displaying 100 records per page')
        display_records.click()
        time.sleep(5)

        records = []
        for page in range(2):  # Loop through 2 pages to get 200 records
            Logger.info('Crawling records page: ' + str(page))
            content = BeautifulSoup(driver.page_source, 'html.parser')
            table_tbody = content.find('table', id='DataTables_Table_0').find('tbody')
            if table_tbody:
                table_trows = table_tbody.find_all('tr')
                for tr in table_trows:
                    isin_td = tr.find('td').find('a').text.strip().split('\n')

                    document_tds = tr.find_all('td')[1:]
                    for document_td in document_tds:
                        span = document_td.find('span')
                        if span:
                            record_metadata = extract_record_metadata(span, isin_td)
                            if record_metadata:  # Check if metadata is not None
                                records.append(record_metadata)

            # Click on the next page button if it's the first page
            if page == 0:
                driver.execute_script("window.scrollTo(0, 8400)")
                time.sleep(10)
                next_page_button = driver.find_element(By.CSS_SELECTOR, '#DataTables_Table_0_next > a')
                Logger.info(f'Loading next page: {page + 1}')
                next_page_button.click()
                time.sleep(10) 

        if records:
            Logger.info("Records extracted successfully.")
            save_to_csv(records, 'fundDatabase.csv')
        else:
            Logger.warning("No records extracted.")

        return records
    except Exception as e:
        Logger.error(f"An error occurred: {str(e)}")


def main():
    # "0 14 * * *" - runs every day at 14:00
    crawl_records()

if __name__ == "__main__":
    main()