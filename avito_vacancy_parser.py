import os
import random
import shutil
import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from sqlalchemy.exc import IntegrityError
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from db.models import session, Vacancy


class AvitoVacancy:

    def __init__(self, link):
        self.link = link

    def get_webdriver(self) -> webdriver:
        chrome_option = Options()
        chrome_option.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        chrome_option.add_argument("start_maximized")
        chrome_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; 64x) "
                                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.88 Safari/537.36")
        chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_option.add_experimental_option('useAutomationExtension', False)
        chrome_option.add_argument('disable-blink-features-AutomationControlled')  # скрывает работу через webdriver
        chrome_option.accept_insecure_certs = True

        seleniumwire_option = {
            "request_storage_base_dir": "cache"
        }

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  seleniumwire_options=seleniumwire_option, options=chrome_option)
        driver.implicitly_wait(10)

        return driver

    def get_first_page(self):
        driver = self.get_webdriver()
        try:
            driver.get(self.link)
        except TimeoutException:
            session.close()
            self.get_first_page()
        self.run_parsing(driver)

    def run_parsing(self, driver):

        key_words = ['python', 'питон', 'разработчик', 'programmer', 'программист',
                     'eml', 'data-engineer', 'parsing', 'парсинг']

        all_vacancies = driver.find_elements(By.XPATH, "//div[@data-marker='item']")

        for vacancy in all_vacancies:
            vacancy_dict = {}
            check_word = False
            title = vacancy.find_element(By.XPATH, ".//h3").text

            for word in key_words:
                if word in title.lower():
                    check_word = True

            if check_word:
                link = vacancy.find_element(By.XPATH, ".//a[contains(@class, 'iva-item-hide')]").get_attribute("href")
                check = self.check_link(link)

                if not check:
                    continue

                elif check:
                    driver.execute_script(f"window.open('{link}')")
                    driver.switch_to.window(driver.window_handles[1])

                    title = driver.find_element(By.XPATH, '//h1').text

                    salary_xpath = "//span[contains(@class, 'js-item-price style-item-price-text-_w822 " \
                                   "text-text-LurtD text-size-xxl-UPhmI')] "
                    address_xpath = "//span[contains(@class, 'style-item-address__string-wt61A')]"

                    terms_xpath = "//li[contains(@class, 'params-params')]"

                    description_xpath = "//div[contains(@class, 'style-item-view-block-SEFaY " \
                                        "style-item-view-description-k9US4 style-new-style-iX7zV')] "

                    try:
                        salary = driver.find_element(By.XPATH, salary_xpath).text
                    except NoSuchElementException:
                        salary = 'Не указана'

                    address = driver.find_element(By.XPATH, address_xpath).text

                    terms = driver.find_elements(By.XPATH, terms_xpath)

                    all_terms = ''
                    for term in terms:
                        all_terms += term.text + '\n'

                    description = driver.find_element(By.XPATH, description_xpath).text.replace('Описание', "")
                    vacancy_dict.update(title=title, link=link, address=address, terms=all_terms,
                                        salary=salary, description=description)

                    new_info = Vacancy(vacancy_dict)
                    try:
                        session.add(new_info)
                        session.commit()
                    except IntegrityError:
                        session.close()

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        if len(all_vacancies) == 50:
            driver.find_element(By.XPATH, "//span[contains(text(), 'След')]").click()
            self.run_parsing(driver)
        elif len(all_vacancies) < 50:
            driver.close()
            directory = os.getcwd() + f'/cache'

            if os.path.exists(directory):
                shutil.rmtree(directory)
            session.close()
            return print('parsing is done')

    def wait_element_xpath(self, driver: webdriver.Chrome, path: str):
        elem = WebDriverWait(driver, random.randint(8, 15)) \
            .until(expected_conditions.presence_of_element_located((By.XPATH, path)))
        return True

    def check_link(self, link: str):
        check = session.query(Vacancy.id).filter_by(link=link).first()
        if check is None:
            return True
        elif check is not None:
            return False
