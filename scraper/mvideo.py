from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_price():
    # Скрываем управление автоматизированным ПО
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """)

    wait = WebDriverWait(driver, 15)

    # Переходим по ссылке, которая задаст необходимый город
    driver.get("https://www.mvideo.ru/?cityId=CityCZ_984")
    time.sleep(2)

    # Переходим по ссылке на необходимый товар
    driver.get("https://www.mvideo.ru/products/elektricheskii-duhovoi-shkaf-bosch-hbf534es0q-400177526")

    # Получаем цену и убираем лишние символы
    price = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.price__main-value"))
    ).text

    price = price.replace("₽", "").replace(" ", "")

    driver.quit()

    return price
