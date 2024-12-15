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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def is_valid_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if not re.match(email_regex, email):
        return False
    
    if re.search(r'[^a-zA-Z0-9@._+-]', email):
        return False
    
    return True

print("Пожалуйста, введите ваш email. Убедитесь, что он соответствует следующим требованиям:")
print("- Электронная почта должна содержать символ '@'.")
print("- После символа '@' должно быть доменное имя (например, gmail.com).")
print("- Электронная почта не должна содержать запрещённые символы (например, пробелы, запятые и другие спецсимволы).")

email = input("Введите ваш email для проверки на утечки: ")

if not is_valid_email(email):
    print("Неверный формат email. Пожалуйста, убедитесь, что это правильный email и в нём нет запрещённых символов.")
    exit(1)

if not os.path.exists("result"):
    os.makedirs("result")

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-extensions") 
chrome_options.add_argument("--blink-settings=imagesEnabled=false") 
chrome_options.add_argument("--start-maximized")  


with webdriver.Chrome(options=chrome_options) as driver:
   
    driver.minimize_window()

    driver.get('https://cybernews.com/personal-data-leak-check/')

    
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, 'email-or-phone'))
    )
    input_field = driver.find_element(By.ID, 'email-or-phone')
    input_field.send_keys(email)
    submit_button = driver.find_element(By.CSS_SELECTOR, '.personal-data-leak-checker-button[data-js-personal-data-leak-check="action"]')
    submit_button.click()

    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.personal-data-leak-checker-steps__header__subtitle'))
    )
    result_div = driver.find_element(By.CSS_SELECTOR, '.personal-data-leak-checker-steps__header__subtitle')
    result_message = result_div.text.strip()

    result_file_path = os.path.join("result", "leak_check_result.txt")
    with open(result_file_path, "w", encoding="utf-8") as file:
        file.write(result_message)

    print(f"Результат сохранён в '{result_file_path}':", result_message)
