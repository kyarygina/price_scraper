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

    #Переходим на главную страницу сайта
    driver.get("https://www.citilink.ru")
    time.sleep(2)

    try:
        city_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-meta-name='CityChangeButton']"))
        )
        city_btn.click()

        input_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='search-city']"))
        )
        input_field.send_keys("Саратов")

        saratov = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Саратов')]"))
        )
        saratov.click()

        time.sleep(2)
    except:
        print("Попап выбора города не найден — используем город по умолчанию")

    # Переходим по ссылке на товар
    driver.get("https://www.citilink.ru/product/duhovoi-shkaf-bosch-hbf534es0q-nerzhaveyuschaya-stal-1854488/")
    time.sleep(2)

    # Получаем цену
    try:
        price = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-meta-name='PriceBlock__price'] span[data-meta-price]"))
        ).text
        price = price.replace("₽", "").replace(" ", "")
    except:
        price = None
        print("Цена не найдена")

    driver.quit()
    return price