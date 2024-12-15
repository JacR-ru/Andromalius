#!/usr/bin/env python3

#============================#
#        andromalius         #
#            ^_^             #
#============================#

banner = r"""
    
 $$$$$$\                $$\                                                 $$\$$\                   
$$  __$$\               $$ |                                                $$ \__|                  
$$ /  $$ $$$$$$$\  $$$$$$$ |$$$$$$\  $$$$$$\ $$\   $$\$$$$$$\$$$$\  $$$$$$\ $$ $$\$$\   $$\ $$$$$$$\ 
$$$$$$$$ $$  __$$\$$  __$$ $$  __$$\$$  __$$\$$ |  $$ $$  _$$  _$$\ \____$$\$$ $$ $$ |  $$ $$  _____|
$$  __$$ $$ |  $$ $$ /  $$ $$ |  \__$$ /  $$ $$ |  $$ $$ / $$ / $$ |$$$$$$$ $$ $$ $$ |  $$ \$$$$$$\  
$$ |  $$ $$ |  $$ $$ |  $$ $$ |     $$ |  $$ $$ |  $$ $$ | $$ | $$ $$  __$$ $$ $$ $$ |  $$ |\____$$\ 
$$ |  $$ $$ |  $$ \$$$$$$$ $$ |     \$$$$$$  \$$$$$$  $$ | $$ | $$ \$$$$$$$ $$ $$ \$$$$$$  $$$$$$$  |
\__|  \__\__|  \__|\_______\__|      \______/ \______/\__| \__| \__|\_______\__\__|\______/\_______/ 

                                                                                                 
"""

import re
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def is_valid_phone(phone: str) -> bool:
    phone_regex = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(phone_regex, phone))

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--ignore-certificate-errors') 
    chrome_options.add_argument('--disable-web-security') 
    chrome_options.add_argument('--allow-insecure-localhost') 
    return webdriver.Chrome(options=chrome_options)

def main():
    while True:
        print("Пожалуйста, введите ваш номер телефона. Убедитесь, что он соответствует следующим требованиям:")
        print("- Номер должен быть в международном формате, например, +1234567890.")
        print("- Он не должен содержать пробелов или недопустимых символов.")

        phone = input("Введите ваш номер телефона для проверки на утечки: ").strip()

        if not is_valid_phone(phone):
            print("Неверный формат номера телефона. Попробуйте снова.")
            continue

        os.makedirs("result", exist_ok=True)

        driver = setup_driver()
        driver.minimize_window()

        try:
            driver.get('https://cybernews.com/personal-data-leak-check/')

            input_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, 'email-or-phone'))
            )
            input_field.send_keys(phone)

            submit_button = driver.find_element(
                By.CSS_SELECTOR, '.personal-data-leak-checker-button[data-js-personal-data-leak-check="action"]'
            )
            submit_button.click()

            result_div = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.personal-data-leak-checker-steps__header__subtitle'))
            )
            result_message = result_div.text.strip()

            result_file_path = os.path.join("result", "leak_check_result.txt")
            with open(result_file_path, "w", encoding="utf-8") as file:
                file.write(result_message)

            os.system(f"echo | set /p nul={result_message} | clip")
            print(f"Результат скопирован в буфер обмена и сохранён в '{result_file_path}':", result_message)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            driver.quit()

        cont = input("Вернуться в начало? (да/нет): ").strip().lower()
        if cont != 'да':
            break

    subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    main()
