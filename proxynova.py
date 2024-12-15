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

import os
import json
import urllib3
import requests
import argparse
from tabulate import tabulate
from neotermcolor import colored
from requests import ConnectionError

urllib3.disable_warnings()

def find_leaks_proxynova(email, proxy, number):
    url = f"https://api.proxynova.com/comb?query={email}"
    headers = {'User-Agent': 'curl'}
    session = requests.session()

    if proxy:
        session.proxies = {'http': proxy, 'https': proxy}

    response = session.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        data = json.loads(response.text)
        total_results = data.get("count", 0)
        print(colored(f"[*] Найдено {total_results} записей в базе данных", "magenta"), end='')

        lines = data.get("lines", [])
        if number is not None:
            lines = lines[:number]
        return lines
    else:
        print(colored(f"[!] Не удалось получить результаты от ProxyNova. Код состояния: {response.status_code}\n", "red"))
        return []

def find_leaks_local_db(database, keyword, number):
    if not os.path.exists(database):
        print(colored(f"[!] Локальная база данных не найдена: {database}\n", "red"))
        exit(-1)

    results = []

    if database.endswith('.json'):
        with open(database, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
                lines = data.get("lines", [])
                for line in lines:
                    # Проверка на ключевое слово в строке
                    if keyword.lower() in line.lower():
                        results.append(line.strip())
            except json.JSONDecodeError as e:
                print(colored(f"[!] Ошибка: Не удалось разобрать локальную базу данных как JSON. Детали: {e}\n", "red"))
                exit(-1)
            except Exception as e:
                print(colored(f"[!] Ошибка при чтении файла: {e}\n", "red"))
                exit(-1)
    else:
        try:
            with open(database, 'r', encoding='utf-8') as file:
                for line in file:
                    # Проверка на ключевое слово в строке
                    if keyword.lower() in line.lower():
                        results.append(line.strip())

                    if number is not None and len(results) >= number:
                        break
        except KeyboardInterrupt:
            print(colored("\n[!] Завершение работы..\n", "red"))
            exit(-1)
        except Exception as e:
            print(colored(f"[!] Ошибка при чтении файла: {e}\n", "red"))
            exit(-1)

    return results[:number] if number is not None else results


def main(database, keyword, output=None, proxy=None, number=None):
    print(colored(f"[>] Поиск утечек для {keyword} в {database}..", "yellow"))

    if database.lower() == "proxynova":
        results = find_leaks_proxynova(keyword.strip(), proxy, number)
    else:
        results = find_leaks_local_db(database.strip(), keyword.strip(), number)

    if not results:
        print(colored(f"\n[!] Утечки в {database} не найдены!\n", "red"))
    else:
        print_results(results, output, number)


def print_results(results, output, number):
    print(colored(f"\n[-] Отбираются первые {len(results)} результатов..", "blue"))
    headers = ["Логин@Домен", "Пароль"]
    table_data = []

    for line in results:
        parts = line.split(":")
        if len(parts) == 2:
            username_domain, password = parts
            table_data.append([username_domain, password])

    os.makedirs("result_nova", exist_ok=True)

    if output is not None:
        output_path = os.path.join("result_nova", output)
        if output.endswith('.json'):
            with open(output_path, 'w') as json_file:
                json.dump({"lines": results}, json_file, indent=2)
                print(colored(f"[+] Данные успешно сохранены в {output_path}!\n", "green"))
        else:
            with open(output_path, 'w') as txt_file:
                txt_file.write(tabulate(table_data, headers, showindex="never"))
                print(colored(f"[+] Данные успешно сохранены в {output_path}!\n", "green"))
    else:
        print(colored("[+] Готово!\n", "green"))
        print(tabulate(table_data, headers, showindex="never"))
        print()

if __name__ == '__main__':
    print(colored(banner, "white"))
    print(colored("""
                    Использование:
                    Программа запросит параметры для поиска утечек.
                    
                    Вы можете ввести следующее:
                    - База данных для поиска (ProxyNova или путь к локальному файлу)
                    - Ключевое слово для поиска (обязательное поле)
                    - Количество результатов (по умолчанию 20)
                    - Выходной файл (json или txt)
                    - Прокси-сервер (например, http://localhost:8080)
                    """, "cyan"))

    database = input(colored("[!] Введите базу данных для поиска (ProxyNova или путь к локальному файлу): ", "yellow")).strip()
    keyword = input(colored("[!] Введите ключевое слово для поиска: ", "yellow")).strip()
    number = input(colored("[!] Введите количество результатов (по умолчанию 20): ", "yellow")).strip()
    number = int(number) if number else 20
    output = input(colored("[!] Введите имя файла для сохранения результатов (или нажмите Enter, чтобы пропустить): ", "yellow")).strip() or None
    proxy = input(colored("[!] Введите прокси-сервер (или нажмите Enter, чтобы пропустить): ", "yellow")).strip() or None

    try:
        main(database, keyword, output, proxy, number)

    except ConnectionError:
        print(colored("[!] Невозможно подключиться к сервису! Проверьте Ваше Интернет-соединение!\n", "red"))
    
    except KeyboardInterrupt:
        print(colored("\n[!] Завершение работы..\n", "red"))
        exit(-1)

    except Exception as e:
        print(colored(f"\n[!] Ошибка: {e}\n", "red"))
