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
import getpass
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def is_valid_password(password: str) -> bool:
    if len(password) < 6:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

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
        print("Пожалуйста, введите ваш пароль. Убедитесь, что он соответствует следующим требованиям:")
        print("- Пароль должен содержать минимум 6 символов.")
        print("- Пароль должен включать хотя бы одну заглавную букву.")
        print("- Пароль должен включать хотя бы одну строчную букву.")
        print("- Пароль должен содержать хотя бы одну цифру.")

        password = getpass.getpass("Введите ваш пароль для проверки на утечки: ")

        if not is_valid_password(password):
            print("Неверный формат пароля. Пожалуйста, убедитесь, что ваш пароль соответствует всем требованиям.")
            continue

        os.makedirs("result", exist_ok=True)

        driver = setup_driver()
        driver.minimize_window()

        try:
            driver.get('https://cybernews.com/password-leak-check/')

            input_field = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, 'checked-password'))
            )
            input_field.send_keys(password)

            submit_button = driver.find_element(
                By.CSS_SELECTOR, '.tool-block-button[data-js-password-leak-check="action"]'
            )
            submit_button.click()

            result_div = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '.personal-data-leak-checker-steps__header__subtitle_strong')
                )
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
